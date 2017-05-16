#!/usr/bin/env python
#-*- coding:utf-8 -*-

import json, urllib2, getopt,sys, os,errno

local_config = {
                "EMAIL_DIR" : "/home/vobile/04Temp/EMAIL/",
                "DB_DIR" : "/home/vobile/04Temp/DB/",
                "TMP_EMAIL_DIR" : "/dev/shm/"
                }
        
def req(url, data):
    data = json.dumps(data)
    resp = urllib2.urlopen(url, data=data)
    return resp.read()

def usage():
    print 'filter_command.py usage:'
    print '-h: print help message.'
    print '-s: server address.calls local method by default.'
    print '-m: method,choices are query,submit,train.'
    print '-f: file_path.'
    print '-i: query id.'
    print '-t: query text.'
    
def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hs:m:f:i:t:")
    except getopt.GetoptError, err:
        usage()
        sys.exit(2)

    host = None
    method_name = None
    file_path = None
    param = None
    file_content_list = None
    query_dict = {}
    
    for op, value in opts:
        if op == "-s":
            host = value
        elif op == "-m":
            if value in ['query','submit','train']:
                method_name = value
            else:
                print 'unhandled method'
                sys.exit(3)
        elif op == "-f":
            file_path = value
            try:
                file_object = open(file_path,"rU")
                file_content_list = []
                lines = file_object.readlines()
                for line in lines:
                    print "line", line
                    file_content_list.append(json.loads(line.replace("\n","")))
            except Exception, e:
                print 'read file error',str(e)
                sys.exit(2)
            finally:
                 file_object.close()
        elif op == "-i":
            query_dict["id"] = value
        elif op == "-t":     
            query_dict["text"] = value       
        elif op == "-h":
            usage()
            sys.exit(1)
        else:
            print 'unhandled option'
            sys.exit(3)
    
    if (method_name in ['train','submit'] and not file_content_list) or (query_dict and file_content_list):
        print 'unhandled option'
        sys.exit(3)        
     
    if method_name == 'query':
        if file_content_list:
            param = file_content_list[0]
        else:
            param = query_dict
    else:
        param = file_content_list
        
#     print "param======================",param
    if host:
        res = req('http://' + host + '/api/' + method_name ,param )
        print method_name ,json.loads(res).get("result","")
    else:
        from method import query, submit, train
        mkdir_p(local_config.get("EMAIL_DIR"))
        mkdir_p(local_config.get("DB_DIR"))
        mkdir_p(local_config.get("TMP_EMAIL_DIR"))
        print method_name, eval(method_name)(local_config,param)
        
def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc: # Python >2.5 (except OSError, exc: for Python <2.5)
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else: raise
        
if __name__ == '__main__':  
    main()
