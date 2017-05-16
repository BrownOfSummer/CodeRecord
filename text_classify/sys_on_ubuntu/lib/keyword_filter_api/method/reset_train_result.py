#!/usr/bin/python
#-*- coding:utf-8 -*-

from export_eml import Gen_Emails
from filter_common import *
import traceback, time, threading, math
import hashlib,os,errno
from datetime import datetime

def reset(app_config,train_data_list):
    try:
        piece_count = 5
        total_count = len(train_data_list)

        if total_count < 10000:
            piece_count = 1
        each_piece_length = int(math.ceil(total_count/float(piece_count)))

        thread_list = []
        for i in range(0, piece_count):
            t =threading.Thread(target=excute_reset,args=(app_config,train_data_list[i*each_piece_length:(i+1)*each_piece_length]))
#             t.setDaemon(True)
            t.start()
            thread_list.append(t)
        for j in thread_list:
            j.join()
        return "True"
    except Exception, e:
        traceback.print_exc()
        return "False"
    
def excute_reset(app_config,train_data_list):

    for train_data_record in train_data_list:

        db_dir = app_config.get("DB_DIR") + get_md5_value(train_data_record["id"])
        
        run_sys_command(("rm -rf %s " )%(db_dir))
        