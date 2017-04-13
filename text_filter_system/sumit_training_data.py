#!/usr/bin/python
#-*- coding:utf-8 -*-

#from export_eml import Gen_Emails
from filter_common import *
import traceback
from datetime import datetime

def submit(app_config,train_data_list):
    try:
        
        file_path_list = {}
        mail_object = Gen_Emails()
        i = 0
        for train_data_record in train_data_list:
            file_path = get_md5_value(train_data_record["id"]) + "/untrain"  + SPLIT_STR + (train_data_record["result"]) + SPLIT_STR
            file_dir = app_config.get('EMAIL_DIR') + file_path
            if not file_path_list.get(file_path,None):
                mkdir_p(file_dir)
                file_path_list[file_path] = "already make dir"
            final_file_path = file_dir + get_file_name(i)
            mail_object.EmailGen(final_file_path, train_data_record["text"])
            i += 1

        return "True"
    except Exception as e:
        traceback.print_exc()
        return "False"

def cnn_submit(app_config,train_data_list):
    try: 
        file_path_list = {}
        for train_data_record in train_data_list:
            file_path = get_md5_value(train_data_record["id"]) + SPLIT_STR + (train_data_record["result"]) + SPLIT_STR
            #file_dir = app_config.get('DATA_DIR') + file_path
            DATA_DIR = "/tmp/data_dir/"
            file_dir = DATA_DIR + file_path
            if not file_path_list.get(file_path,None):
                mkdir_p(file_dir)
                file_path_list[file_path] = "already make dir"
            #time_file = datetime.now().strftime('%Y%m%d%H%M%S%f')
            final_file_path = file_dir + "untrain"
            with open(final_file_path, "a") as fp:
                fp.write("%s\n" % train_data_record["text"].strip())
        return "True"
    except Exception as e:
        traceback.print_exc()
        return "False"
