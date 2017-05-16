#!/usr/bin/python
#-*- coding:utf-8 -*-
import os
import re
def data_tranfor(data_dir):
    data_result_list = []
    for rt, dirs, files in os.walk(data_dir):
        for file in files:
            flag = ""
            if file.startswith("result2"):
                flag = "TRUE"
            elif file.startswith("result3"):
                flag = "FALSE"
            else:
                continue
            
            file_object = open(data_dir + file, 'rU')
            try:
                file_contents = file_object.read()

            finally:  
                file_object.close( ) 
            
#             print file_contents
            p1 = r'(<span style="padding-left:8px;" title=")(.*?)(">)'#这是我们写的正则表达式规则，你现在可以不理解啥意思
            pattern1 = re.compile(p1)#我们在编译这段正则表达式
            matcher1 = re.findall(pattern1,file_contents)#在源文本中搜索符合正则表达式的部分

            p2 = r'(<td>\s+<a href=".*target="_blank" title=")(.*?)(">)'
            pattern2 = re.compile(p2)#我们在编译这段正则表达式
            matcher2 = re.findall(pattern2,file_contents)#在源文本中搜索符合正则表达式的部分

            for i in range(0, len(matcher1)):
                tmp = {}
                tmp["id"] = matcher1[i][1]
                tmp["text"] = matcher2[i][1]
                tmp["result"] = flag
                data_result_list.append(tmp)
#             break
    data_result_list = sorted(data_result_list, key=lambda student : student["id"])
    
    file_name = data_dir.split("/")[len(data_dir.split("/")) - 2]
    print "file", file_name
    fileHandle = open (file_name  + '.txt', 'w' )
    old_data_record = {}
    for data_record in data_result_list:
        if data_record["id"] == old_data_record.get("id","") and data_record["result"] != old_data_record.get("result",""):
            print "has both result ****************************************",data_record
        old_data_record = data_record
        line = "{\"id\":\"%s\",\"text\":\"%s\",\"result\":\"%s\"}" %(data_record["id"],data_record["text"],data_record["result"])
#         print line
        fileHandle.write (line+ "\n")
    fileHandle.close()

if __name__=='__main__':
    data_tranfor('/home/vobile/vt_spider_data/11705204_4/')