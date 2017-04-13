#!/usr/bin/python
#-*- coding:utf-8 -*-

from export_eml import Gen_Emails
from filter_common import *
import traceback, time, threading, math
import hashlib,os,errno
from datetime import datetime

from cnn_filter import *
def train(app_config,train_data_list):
    try:
#         arithmetic_pattern_dict = ['syl','']
#         for i in arithmetic_pattern_dict:
#             mkdir_p(app_config.get("DB_DIR") + arithmetic_pattern_dict[i])
#         base_dir = app_config.get("DB_DIR") + "/syl"
        piece_count = 5
        total_count = len(train_data_list)

        if total_count < 10000:
            piece_count = 1
        each_piece_length = int(math.ceil(total_count/float(piece_count)))

        print "each_piece_length", each_piece_length
        thread_list = []
        for i in range(0, piece_count):
            t =threading.Thread(target=excute_train,args=(app_config,train_data_list[i*each_piece_length:(i+1)*each_piece_length]))
#             t.setDaemon(True)
            t.start()
            thread_list.append(t)
        for j in thread_list:
            j.join()
        return "True"
    except Exception, e:
        traceback.print_exc()
        return "False"
    
def excute_train(app_config,train_data_list):
    
    print "excute_train", train_data_list
    for train_data_record in train_data_list:
        untrain_dir = app_config.get("EMAIL_DIR") + get_md5_value(train_data_record["id"]) + "/untrain/" 
        training_dir = untrain_dir.replace("/untrain/","/training/")
        trained_dir = untrain_dir.replace("/untrain/","/trained/") + datetime.now().strftime('%Y%m%d%H%M%S%f')
        mkdir_p(training_dir)
        mkdir_p(trained_dir)
        db_dir = app_config.get("DB_DIR") + get_md5_value(train_data_record["id"])
        
        run_sys_command(("mv -f %s* %s" )%(untrain_dir, training_dir))
        
#         mkdir_p(db_dir + "/syl")
#         run_sys_command(("sylfilter -p %s/syl -j %sFALSE/*")%(db_dir, training_dir))
#         run_sys_command(("sylfilter -p %s/syl -c %sTRUE/*")%(db_dir, training_dir))
#           
#         mkdir_p(db_dir + "/bogo")
#         run_sys_command(("bogofilter -d %s/bogo -s -B %sFALSE/*")%(db_dir, training_dir))
#         run_sys_command(("bogofilter -d %s/bogo -n -B %sTRUE/*")%(db_dir, training_dir))
        
        mkdir_p(db_dir + "/syl")
        run_sys_command(("find %sFALSE/ -name \"*.eml\" | xargs -i sylfilter -p %s/syl -j {} ")%(training_dir, db_dir))
        run_sys_command(("find %sTRUE/ -name \"*.eml\" | xargs -i sylfilter -p %s/syl -c {} ")%(training_dir, db_dir))
          
        mkdir_p(db_dir + "/bogo")
        run_sys_command(("find %sFALSE/ -name \"*.eml\" | xargs -i bogofilter -d %s/bogo -s -B {} ")%(training_dir, db_dir))
        run_sys_command(("find %sTRUE/ -name \"*.eml\" | xargs -i bogofilter -d %s/bogo -n -B {} ")%(training_dir, db_dir))
        
        
        run_sys_command(("mv %s* %s/" )%(training_dir, trained_dir))
        
#         run_sys_command(("tar -zcvf %s.tar.gz %s --remove-files" )%(trained_dir, trained_dir))


def run_cnn_train(train_data_record):
    
    print "excute_train", train_data_record
    # Get the untrain file
    path_untrain_r = app_config.get("DATA_DIR") + get_md5_value(train_data_record["id"]) + "/TRUE/untrain" 
    path_untrain_w = app_config.get("DATA_DIR") + get_md5_value(train_data_record["id"]) + "/FALSE/untrain"
    # Split to training and never_trained
    split_text(path_untrain_r, path_untrain_w)
    # Generate the vocabulary for mapping, save in ID/vocab
    generate_vocab(path_untrain_r, path_untrain_w)
    # Get training file
    #path_training_r = app_config.get("DATA_DIR") + get_md5_value(train_data_record["id"]) + "/TRUE/training" 
    path_training_r = os.path.join(os.path.dirname(path_untrain_r), "training")
    #path_training_w = app_config.get("DATA_DIR") + get_md5_value(train_data_record["id"]) + "/FALSE/training" 
    path_training_w = os.path.join(os.path.dirname(path_untrain_w), "training")
    # Train and save model to id/runs/, save vocab to id/
    cnn_train(path_training_r, path_training_w)

    # Move the model to Model dir
    model_dir = app_config.get("MODEL_DIR") + get_md5_value(train_data_record["id"])
    if not os.path.exists(model_dir):
        mkdir_p(model_dir)
    runs_dir = app_config.get("DATA_DIR") + get_md5_value(train_data_record["id"]) + "/runs" 
    vocab_path = app_config.get("DATA_DIR") + get_md5_value(train_data_record["id"]) + "vocab" 
    run_sys_command(("mv %s %s")%(runs_dir, model_dir))
    run_sys_command(("mv %s %s")%(vocab_path, model_dir))

    # Append training to trained
    path_trained_r = path_training_r.replace("training","trained")
    path_trained_w = path_training_w.replace("training","trained")
    run_sys_command(("cat %s >> %s")%(path_training_r, path_trained_r))
    run_sys_command(("cat %s >> %s")%(path_training_w, path_trained_w))

    # Remove the untrain file
    run_sys_command(("rm %s %s")%(path_untrain_r, path_untrain_w))

 def run_cnn_retrain(train_data_record):
    
    print "excute_train", train_data_record
    # Get the untrain file
    path_untrain_r = app_config.get("DATA_DIR") + get_md5_value(train_data_record["id"]) + "/TRUE/untrain" 
    path_untrain_w = app_config.get("DATA_DIR") + get_md5_value(train_data_record["id"]) + "/FALSE/untrain"
    # Split to training and never_trained
    split_text(path_untrain_r, path_untrain_w)
    # Append the vocabulary for mapping, save in id/vocab
    model_dir = app_config.get("MODEL_DIR") + get_md5_value(train_data_record["id"])
    append_vocab(model_dir, path_untrain_r, path_untrain_w)
    # Get training file
    #path_training_r = app_config.get("DATA_DIR") + get_md5_value(train_data_record["id"]) + "/TRUE/training" 
    path_training_r = os.path.join(os.path.dirname(path_untrain_r), "training")
    #path_training_w = app_config.get("DATA_DIR") + get_md5_value(train_data_record["id"]) + "/FALSE/training" 
    path_training_w = os.path.join(os.path.dirname(path_untrain_w), "training")
    # Train and save model to id/runs/, save vocab to id/
    cnn_retrain(model_dir, path_training_r, path_training_w)

    # Append training to trained
    path_trained_r = path_training_r.replace("training","trained")
    path_trained_w = path_training_w.replace("training","trained")
    run_sys_command(("cat %s >> %s")%(path_training_r, path_trained_r))
    run_sys_command(("cat %s >> %s")%(path_training_w, path_trained_w))

    # Remove the untrain file
    run_sys_command(("rm %s %s")%(path_untrain_r, path_untrain_w))
        
 def excute_cnn_train(app_config,train_data_list):
     print train_data_list
     for train_data_record in train_data_list:
         model_dir = app_config.get("MODEL_DIR") + get_md5_value(train_data_record["id"])
         runs_dir = os.path.join(model_dir, "runs")
         vocab_path = os.path.join(model_dir, "vocab")
         if os.path.exists(runs_dir) and os.path.exists(vocab_path):
             run_cnn_retrain(train_data_record)
        else:
            run_cnn_train(train_data_record)
