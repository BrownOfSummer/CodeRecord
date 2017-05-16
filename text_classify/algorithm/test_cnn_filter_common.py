import os
import numpy as np
from cnn_filter_common import *

DATA_DIR = "/tmp/data_dir/"
MODEL_DIR = "/tmp/model_dir/"
#path_untrain_r = DATA_DIR + "/id2" + "/TRUE/untrain1"
#path_untrain_w = DATA_DIR + "/id2" + "/FALSE/untrain1"

query_right = "../random_data/new_split/q_R2.csv"
query_wrong = "../random_data/new_split/q_W2.csv"
def run_sys_command(command_str,output_type=""):
    print("command_str", command_str)
    import subprocess
    
    if output_type == "FILE":
#         fdout = open("/tmp/tmpSysCommand.out", 'w')
        fderr = open("/tmp/tmpSysCommand.err", 'w')
    else:
        fderr = subprocess.PIPE
     
    p = subprocess.Popen(command_str, shell=True, stdout=subprocess.PIPE, stderr=fderr)  
    p.wait()
    stdout,stderr = p.communicate()
    print('stdout : ',stdout)
    print('stderr : ',stderr)
    return stdout

def run_retrain(path_untrain_r, path_untrain_w):
    print("\nDo the retrain step...\n")
    model_dir = MODEL_DIR + "/id2"
    split_text(path_untrain_r, path_untrain_w)
    append_vocab(model_dir, path_untrain_r, path_untrain_w)
    training_r = os.path.join(os.path.dirname(path_untrain_r), "training")
    training_w = os.path.join(os.path.dirname(path_untrain_w), "training")
    cnn_retrain(model_dir, training_r, training_w)

    """Append the training to trained"""
    trained_r = training_r.replace("training","trained")
    trained_w = training_w.replace("training","trained")
    run_sys_command(("cat %s >> %s")%(training_r, trained_r))
    run_sys_command(("cat %s >> %s")%(training_w, trained_w))

    """Remove the untrain file"""
    run_sys_command(("rm %s %s")%(path_untrain_r, path_untrain_w))

def run_train(path_untrain_r, path_untrain_w):
    print("\nDo the train step...\n")
    split_text(path_untrain_r, path_untrain_w)
    generate_vocab(path_untrain_r, path_untrain_w)
    training_r = os.path.join(os.path.dirname(path_untrain_r), "training")
    training_w = os.path.join(os.path.dirname(path_untrain_w), "training")
    cnn_train(training_r, training_w)
    """Move to MODEL_DIR"""
    model_dir = os.path.join(os.path.dirname(training_r),"..")
    runs_dir = os.path.join(model_dir, "runs")
    vocab_path = os.path.join(model_dir, "vocab")
    run_sys_command(("mv %s %s")%(runs_dir, MODEL_DIR+"/id2"))
    run_sys_command(("mv %s %s")%(vocab_path, MODEL_DIR+"/id2"))

    """Append the training to trained"""
    trained_r = training_r.replace("training","trained")
    trained_w = training_w.replace("training","trained")
    run_sys_command(("cat %s >> %s")%(training_r, trained_r))
    run_sys_command(("cat %s >> %s")%(training_w, trained_w))

    """Remove the untrain file"""
    run_sys_command(("rm %s %s")%(path_untrain_r, path_untrain_w))

for text in ["untrain1", "untrain2", "untrain3"]:
    path_untrain_r = DATA_DIR + "/id2/TRUE/" + text
    path_untrain_w = DATA_DIR + "/id2/FALSE/" + text
    if os.path.exists(MODEL_DIR + "/id2/runs"):
        run_retrain(path_untrain_r, path_untrain_w)
    else:
        run_train(path_untrain_r, path_untrain_w)

    cnn_query(MODEL_DIR+"/id2", query_right)
    print("query split ====================")
    cnn_query(MODEL_DIR+"/id2", query_wrong)
