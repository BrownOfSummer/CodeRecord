#!/usr/bin/python
#-*- coding:utf-8 -*-

from export_eml import Gen_Emails
from filter_common import *
import traceback,os,re
from datetime import datetime

from cnn_filter_utils import single_cnn_query
def query(app_config,train_data_record):
    try:
        tmp_file_path = app_config.get("TMP_EMAIL_DIR") + get_file_name()
        db_dir = app_config.get("DB_DIR") + get_md5_value(train_data_record["id"])
          
        mail_object = Gen_Emails()
        mail_object.EmailGen(tmp_file_path, train_data_record["text"])
        
        query_pattern = train_data_record.get("query_pattern",app_config.get("ARITHMETIC"))
        method_name = "query_%sfilter" %(query_pattern)
        result, prob = eval(method_name)(db_dir, tmp_file_path)
        #print result
        os.remove(tmp_file_path)
        
        return {"result":result,"prob":prob}
    
    except Exception as e:
        traceback.print_exc()
        raise e
    
def query_bogofilter(db_dir, tmp_file_path):
    return_mapping= {"Spam":"FALSE","Ham":"TRUE","Unsure":"UNKNOWN"}
    result = ""
    result_command_str = "bogofilter -d %s/bogo -v < %s -o 0.999990" %(db_dir, tmp_file_path)
    result = run_sys_command(result_command_str)
    
    p1 = r'(X-Bogosity: )(.*)(, test)'
    pattern1 = re.compile(p1)
    matcher1 = re.findall(pattern1,result)
    
    p2 = r'(spamicity=)(.*)(,)'
    pattern2 = re.compile(p2)
    matcher2 = re.findall(pattern2,result)
    
    #print matcher1, matcher2
    if len(matcher1) > 0:
        return return_mapping[matcher1[0][1]], matcher2[0][1]
    else:
        return "UNKNOWN","0.50000"
    
def query_sylfilter(db_dir, tmp_file_path):
    return_mapping= {"0":"FALSE","1":"TRUE","2":"UNKNOWN"}
    result = ""
    result_command_str = "sylfilter -p %s/syl -v %s" %(db_dir, tmp_file_path)
    result = run_sys_command(result_command_str)
    
    p1 = r'(return value: )(.*)'
    pattern1 = re.compile(p1)
    matcher1 = re.findall(pattern1,result)
    
    p2 = r'(probability = )(.*)'
    pattern2 = re.compile(p2)
    matcher2 = re.findall(pattern2,result)
    
    if len(matcher1) > 0:
        return return_mapping[matcher1[0][1]], matcher2[0][1]
    else:
        return "UNKNOWN","0.50000"

def query_cnnfilter(app_config, train_data_record):
   tmp_file_path = "/tmp/" + datetime.now().strftime('%Y%m%d%H%M%S%f') + ".query"
   model_dir = app_config.get("MODEL_DIR") + get_md5_value(train_data_record["id"])
   with open(tmp_file_path,"w") as fp:
       fp.write("%s\n" % train_data_record["text"])
   pred, prob = single_cnn_query(model_dir, tmp_file_path)
   os.remove(tmp_file_path)
   if pred > 0:
       return "TRUE", prob
   else:
       return "FALSE", prob
