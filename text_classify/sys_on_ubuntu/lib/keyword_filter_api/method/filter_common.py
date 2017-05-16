#!/usr/bin/python
#-*- coding:utf-8 -*-

import os, errno, hashlib, datetime,traceback
SPLIT_STR = "/"

def get_md5_value(src):
    try:
        src = src.encode("utf-8")
        myMd5 = hashlib.md5()

        myMd5.update(src)

        myMd5_Digest = myMd5.hexdigest()

        return str(myMd5_Digest)
    except Exception, e:
        print "get_md5_value error: ", src
        traceback.print_exc()
        return src

def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc: # Python >2.5 (except OSError, exc: for Python <2.5)
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else: raise
        
def check_dir_exist(path):
    try:
        pass
    except OSError as exc: # Python >2.5 (except OSError, exc: for Python <2.5)
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else: raise
           
def get_file_name(index=None):
    return datetime.datetime.now().strftime('%Y%m%d%H%M%S%f') + ".eml"

def run_sys_command(command_str,output_type=""):
    print "command_str", command_str
    import subprocess
    
    if output_type == "FILE":
#         fdout = open("/tmp/tmpSysCommand.out", 'w')
        fderr = open("/tmp/tmpSysCommand.err", 'w')
    else:
        fderr = subprocess.PIPE
     
    p = subprocess.Popen(command_str, shell=True, stdout=subprocess.PIPE, stderr=fderr)  
    p.wait()
    stdout,stderr = p.communicate()
    print 'stdout : ',stdout
    print 'stderr : ',stderr

    return stdout
