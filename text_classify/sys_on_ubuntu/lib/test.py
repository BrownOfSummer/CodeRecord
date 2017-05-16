#!/usr/bin/env python
#-*- coding:utf-8 -*-
import json, urllib2, random

HOST = "54.223.221.196:82/keyword_filter_api"
HOST = "35.161.90.127:88/keyword_filter_api"
#HOST = "localhost:8082"
def req(url, data):
    data = json.dumps(data)
    resp = urllib2.urlopen(url, data=data)
    return resp.read()

import csv
from csv import QUOTE_NONE
def csv_table_byindex(filecontents):
    list_of_all_the_lines = csv.reader(open(filecontents,'rb'), delimiter='\t')
#     file_object = open(filecontents, 'rU') 
#     list_of_all_the_lines = file_object.readlines( )

    return_list_0 = []
    return_list_1 = []
    i = 0
    mapping = {}
    for line in list_of_all_the_lines:
#         if (line.find("\n")) > -1:
#             print "this row have ",line
#         line = line.replace("\n","").split("\t")
        if mapping.get(line[0],None) is None:
            mapping[line[0]] = []
#         mapping[line[0]].append("\t".join(line) + "\n")
        mapping[line[0]].append(line)
        i+=1
    
    print "i",i
    write_line = 0
    
    file_name = "random_3"
    
    file_t =  open(file_name+"_t_w.csv", 'ab') 
    file_q = open(file_name+"_q_w.csv", 'ab')
#     print mapping
    for k in mapping:
        total_count = int(len(mapping[k])/2)
        print "total count ", len(mapping[k])
        print "total count ", len(mapping[k])
#         print mapping[k][0]
        random.shuffle(mapping[k])
#         print mapping[k][0]
        file_name = k.split("\t")[0]
        
        writer = csv.writer(file_t, delimiter='\t')
        for i in range(0,total_count):
            if (" ".join(mapping[k][i]).find("\n")) > -1:
                print "have 1", " ".join(mapping[k][i]).replace("\n", "**********")
            writer.writerow(mapping[k][i])
            write_line +=1

        writer_q = csv.writer(file_q, delimiter='\t')
        for j in range(total_count,len(mapping[k])):
            if (" ".join(mapping[k][j]).find("\n")) > -1:
                print "have 2", " ".join(mapping[k][j]).replace("\n", "**********")
            writer_q.writerow(mapping[k][j])
            write_line +=1
    file_t.close()
    file_q.close
    print "total write line,", write_line
    
import codecs
def save_csv_file(filecontents, result_list, web_prefix):
    print len(result_list)
    file_name = datetime.datetime.now().strftime('%Y%m%d%H%M%S%f') + ".csv"
    
    with open(file_name, 'wb') as csvfile:
        csvfile.write(codecs.BOM_UTF8)
        writer = csv.writer(csvfile, delimiter='\t')
        data = csv.reader(filecontents, delimiter='\t')
        i = 0
        for line in data:
#             print "row", i
            line.append(result_list[i][0])
            line.append(result_list[i][1])
            writer.writerow(line)
            i += 1
    
    return web_prefix + '/static/csv/' + file_name

def distinc_csv_file(filecontents):
    file_name = filecontents + "_distinc.csv"
    url_list = []
    with open(file_name, 'wb') as csvfile:
        csvfile.write(codecs.BOM_UTF8)
        writer = csv.writer(csvfile, delimiter='\t')
        data = csv.reader(open(filecontents,"rU"), delimiter='\t')
        i = 0
        for line in data:
#             print "row", i
            if line[0] not in url_list:
                writer.writerow(line)
                url_list.append(line[0])
                print "write" 
#             else:
#                 print "have this url already", line[0]
            i += 1
            

if __name__=='__main__':
    param = []
    param.append({"id":"ABC" ,"text":"english","result":"TRUE"})
    param.append({"id":"ABC" ,"text":"nihao","result":"FALSE"})
    param.append({"id":"EFG" ,"text":"hello","result":"FALSE"})
    param.append({"id":"EFG" ,"text":"hello two","result":"FALSE"})
    param.append({"id":"EFG" ,"text":"two","result":"TRUE"})
        
    print 'training_prepare',req('http://' + HOST + '/api/submit', param)
            
    param = []
    param.append({"id":"ABC"})
    param.append({"id":"ABC2"})
    param.append({"id":"ABC3"})
    param.append({"id":"ABC4"})
    param.append({"id":"ABC5"})
    param.append({"id":"ABC6"})
    param.append({"id":"ABC7"})
    param.append({"id":"EFG" })
        
    print 'training_data',req('http://' + HOST + '/api/train', param)
           
    param = {"id":"ABC" ,"text":"english"}
            
    print 'query',req('http://' + HOST + '/api/query', param)
          
         
    param = {'text': "hello", 'id': "EFG"}
          
    print 'query',req('http://' + HOST + '/api/query', param)
# 
# #-----------------------add reset api------------------------------------------------------- 
#     param = []
#     param.append({"id":"ABC"})
#     param.append({"id":"EFG" })
#       
#     print 'reset data',req('http://' + HOST + '/api/reset', param)
#     
#     param = {"id":"ABC" ,"text":"english"}
#            
#     print 'query',req('http://' + HOST + '/api/query', param)
#          
#         
#     param = {'text': "hello", 'id': "EFG"}
#          
#     print 'query',req('http://' + HOST + '/api/query', param)

#     csv_table_byindex("/home/vobile/youtubeTestData/RT40593_result_02.csv")

#     distinc_csv_file("/home/vobile/link_content_qi.csv")
