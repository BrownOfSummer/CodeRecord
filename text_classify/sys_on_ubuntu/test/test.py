#!/usr/bin/env python
#-*- coding:utf-8 -*-

import json, xlrd
import urllib2, uuid
import time, os
from data_spider import SDU_Spider

HOST = "54.222.142.39:8082"
HOST = "localhost:8082"
def req(url, data):
    data = json.dumps(data)
    resp = urllib2.urlopen(url, data=data)
    return resp.read()

def read_sample_url(search_titile, filename,result):
    print "reading file..."
    src_urls = []
    title_list = []
    bk = xlrd.open_workbook(filename)

    sh = bk.sheet_by_index(1)

    #获取行数
    nrows = sh.nrows

    #获取各行数据
    for i in range(1,nrows):
        src_url = str(sh.cell_value(i,1).encode("utf-8"))
        title = str(sh.cell_value(i,0).encode("utf-8"))
        
        if title == search_titile:
            src_urls.append({"id":search_titile,"text":src_url,"result":result})
    print "reading file end"
#     print src_urls
    return src_urls

def init_thread(test_title):
#     try:

    negative_file_list = read_sample_url(test_title,"/home/vobile/05SVN/FP.xlsx","FALSE")
    positive_file_list  = read_sample_url(test_title,"/home/vobile/05SVN/Infringing.xlsx","TRUE")

    result_file_content = []
    result = ""
    min_len = min([len(positive_file_list),len(negative_file_list)])
    print "min_len", min_len
#     min_len = 4
    for i in range(0, min_len/2):
        right_count = 0
        
        print 'training_prepare',req('http://' + HOST + '/api/training_prepare', [negative_file_list[i]])
        print 'training_prepare',req('http://' + HOST + '/api/training_prepare', [positive_file_list[i]])
        
        time.sleep(1)    
        print 'train_data',req('http://' + HOST + '/api/train_data', [{"id":test_title }])
            
        for j in range(min_len/2, min_len):
#             result = ""
#             param = negative_file_list[j]
#             result = req('http://' + HOST + '/api/search_train_data', param)
#             print "negative result++++++++++++++", result            
#             result = json.loads(result).get("result","")
#  
#             if result == "0" :
#                 right_count += 1
                  
            result = ""
#                 print "positive_file_list[j]",positive_file_list[j]
            param = positive_file_list[j]
            result = req('http://' + HOST + '/api/search_train_data', param)
            print "positive result++++++++++++++", result            
            result = json.loads(result).get("result","")
             
#             if result == "1" or result == "2" :
            if result == "1" :
                right_count += 1
             
        print "sample is ", i+1, "right count is ", right_count,"rate is ",right_count*100/(min_len/2)  
        result_file_content.append(str(i+1)+ " "+ str(right_count*100/(min_len/2))+"\n")    
         
                 
    print result_file_content
    result_file_dir = "/home/vobile/05SVN/"
    print result_file_dir + "result.txt"
    file_object = open(result_file_dir + "result.txt", 'w')
    file_object.writelines(result_file_content)
    file_object.close( )
     
    arr=[]
    arr.append("set terminal png size 800, 800 \n")
    arr.append("set output \""+result_file_dir+ "result.png"+"\"\n")
    arr.append("plot \""+result_file_dir+ "result.txt"+"\" using 1:2 with linespoints \n")
     
    gnuf = open(result_file_dir+'tmp.gnu', 'w')
    gnuf.writelines(arr)
    gnuf.close()
     
    os.system('gnuplot '+result_file_dir+'tmp.gnu')
    print "result_file_dir",result_file_dir+ "result.png"
    
def full_push(test_title):
#     try:

    negative_file_list = read_sample_url(test_title,"/home/vobile/05SVN/FP.xlsx","FALSE")
    positive_file_list  = read_sample_url(test_title,"/home/vobile/05SVN/Infringing.xlsx","TRUE")

    result_file_content = []
    result = ""
    min_len = min([len(positive_file_list),len(negative_file_list)])
    print "min_len", min_len
    min_len = 4
    for i in range(0, min_len):
        right_count = 0
        
        print 'training_prepare',req('http://' + HOST + '/api/training_prepare', [negative_file_list[i]])
        print 'training_prepare',req('http://' + HOST + '/api/training_prepare', [positive_file_list[i]])
        
#         time.sleep(1)    
#         print 'train_data',req('http://' + HOST + '/api/train_data', [{"id":test_title }])
#             
#         for j in range(0, min_len):
# #             result = ""
# #             param = negative_file_list[j]
# #             result = req('http://' + HOST + '/api/search_train_data', param)
# #             print "negative result++++++++++++++", result            
# #             result = json.loads(result).get("result","")
# #  
# #             if result == "0" :
# #                 right_count += 1
#                   
#             result = ""
# #                 print "positive_file_list[j]",positive_file_list[j]
#             param = positive_file_list[j]
#             result = req('http://' + HOST + '/api/search_train_data', param)
#             print "positive result++++++++++++++", result            
#             result = json.loads(result).get("result","")
#              
# #             if result == "1" or result == "2" :
#             if result == "1" :
#                 right_count += 1
#              
#         print "sample is ", i+1, "right count is ", right_count,"rate is ",right_count*100/(min_len/2)  
#         result_file_content.append(str(i+1)+ " "+ str(right_count*100/(min_len/2))+"\n")    
#          
#                  
#     print result_file_content
#     result_file_dir = "/home/vobile/05SVN/"
#     print result_file_dir + "result.txt"
#     file_object = open(result_file_dir + "result.txt", 'w')
#     file_object.writelines(result_file_content)
#     file_object.close( )
#      
#     arr=[]
#     arr.append("set terminal png size 800, 800 \n")
#     arr.append("set output \""+result_file_dir+ "result_full_push.png"+"\"\n")
#     arr.append("plot \""+result_file_dir+ "result.txt"+"\" using 1:2 with linespoints \n")
#      
#     gnuf = open(result_file_dir+'tmp.gnu', 'w')
#     gnuf.writelines(arr)
#     gnuf.close()
#      
#     os.system('gnuplot '+result_file_dir+'tmp.gnu')
#     print "result_file_dir",result_file_dir+ "result.png"
def import_data_from_text_train_only(test_file):
#     try:
    positive_file_list = []
    negative_file_list = []
    file_object = open(test_file, 'rU')
    try:
        file_contents = file_object.readlines()
        for line in file_contents:
            
            line = line.replace("\n","")
#             print line
            try:
                json_line = json.loads(line, strict=False)
                positive_file_list.append(json_line)
                test_id = json_line.get("id")
            except Exception, e:
                continue
    finally:  
        file_object.close( ) 
                
    print 'training_prepare',req('http://' + HOST + '/api/training_prepare', positive_file_list)
        
    time.sleep(1)    
    print 'train_data',req('http://' + HOST + '/api/train_data', [{"id":test_id }])

    
def import_data_from_text(test_file):
#     try:
    positive_file_list = []
    negative_file_list = []
    file_object = open(test_file, 'rU')
    try:
        file_contents = file_object.readlines()
        for line in file_contents:
            
            line = line.replace("\n","")
#             print line
            try:
                json_line = json.loads(line, strict=False)
                if json_line.get("result","") == "TRUE":
                    positive_file_list.append(json_line)
                else:
                    negative_file_list.append(json_line)
                test_id = json_line.get("id")
            except Exception, e:
                continue
    finally:  
        file_object.close( ) 
                
    result_file_content = []
    result = ""
    min_len = min([len(positive_file_list),len(negative_file_list)])
    print "min_len", min_len
#     min_len = 200
    for i in range(0, min_len/2):
        j_right_count = 0
        c_right_count = 0
        unknown_count = 0
        error_count = 0
        print 'training_prepare',req('http://' + HOST + '/api/training_prepare', [negative_file_list[i]])
        print 'training_prepare',req('http://' + HOST + '/api/training_prepare', [positive_file_list[i]])
        
        time.sleep(1)    
        print 'train_data',req('http://' + HOST + '/api/train_data', [{"id":test_id }])
            
        for j in range(min_len/2, min_len):
            result = ""
            param = negative_file_list[j]
            result = req('http://' + HOST + '/api/search_train_data', param)
            print "negative result++++++++++++++", result            
            result = json.loads(result).get("result","")
  
            if result == "0" :
                j_right_count += 1
            elif result == "2" :
                unknown_count +=1
            else:
                error_count +=1
                  
#             result = ""
# #                 print "positive_file_list[j]",positive_file_list[j]
#             param = positive_file_list[j]
#             result = req('http://' + HOST + '/api/search_train_data', param)
#             print "positive result++++++++++++++", result            
#             result = json.loads(result).get("result","")
#              
# #             if result == "1" or result == "2" :
#             if result == "1" :
#                 right_count += 1
             
        print "sample is ", i+1, "right count is ", j_right_count,"rate is ",j_right_count*100/(min_len/2)  
        result_file_content.append(str(i+1)+ " "+ str(j_right_count*100/(min_len/2))+ " "+ str(error_count*100/(min_len/2))+ " "+ str(unknown_count*100/(min_len/2))+"\n")    

    plot_png(test_file,result_file_content)

def import_data_from_diff_text(train_file,query_file):
#     try:
    positive_file_list = []
    negative_file_list = []
    query_positive_file_list = []
    query_negative_file_list = []
    
    file_object = open(train_file, 'rU')
    try:
        file_contents = file_object.readlines()
        for line in file_contents:
            
            line = line.replace("\n","")
#             print line
            try:
                json_line = json.loads(line, strict=False)
                if json_line.get("result","") == "TRUE":
                    positive_file_list.append(json_line)
                else:
                    negative_file_list.append(json_line)
                test_id = json_line.get("id")
            except Exception, e:
                continue
    finally:  
        file_object.close( ) 
    
    query_file_object = open(query_file, 'rU')
    try:
        query_file_contents = query_file_object.readlines()
        for line in query_file_contents:
            
            line = line.replace("\n","")
#             print line
            try:
                json_line = json.loads(line, strict=False)
                if json_line.get("result","") == "TRUE":
                    query_positive_file_list.append(json_line)
                else:
                    query_negative_file_list.append(json_line)
                query_test_id = json_line.get("id")
            except Exception, e:
                continue
    finally:  
        query_file_object.close( ) 
                
    result_file_content = []
    result = ""
    min_len = min([len(positive_file_list),len(negative_file_list)])
    print "min_len", min_len
    min_len = 200
    for i in range(0, min_len/2):
        j_right_count = 0
        c_right_count = 0
        unknown_count = 0
        error_count = 0
        print 'training_prepare',req('http://' + HOST + '/api/training_prepare', [negative_file_list[i]])
        print 'training_prepare',req('http://' + HOST + '/api/training_prepare', [positive_file_list[i]])
        
        time.sleep(1)    
        print 'train_data',req('http://' + HOST + '/api/train_data', [{"id":test_id }])
            
        for j in range(0, min_len/2):
            result = ""
            param = query_negative_file_list[j]
            result = req('http://' + HOST + '/api/search_train_data', param)
                   
            result = json.loads(result).get("result","")
            print param["text"], "----------", result     
            if result == "0" :
                j_right_count += 1
            elif result == "2" :
                unknown_count +=1
            else:
                error_count +=1
                  
#             result = ""
# #                 print "positive_file_list[j]",positive_file_list[j]
#             param = positive_file_list[j]
#             result = req('http://' + HOST + '/api/search_train_data', param)
#             print "positive result++++++++++++++", result            
#             result = json.loads(result).get("result","")
#              
# #             if result == "1" or result == "2" :
#             if result == "1" :
#                 right_count += 1
             
        print "sample is ", i+1, "right count is ", j_right_count,"rate is ",j_right_count*100/(min_len/2)  
        result_file_content.append(str(i+1)+ " "+ str(j_right_count*100/(min_len/2))+ " "+ str(error_count*100/(min_len/2))+ " "+ str(unknown_count*100/(min_len/2))+"\n")    
         
                 
    print result_file_content
    plot_png(query_file,result_file_content)

def plot_png(query_file,result_file_content):
    result_file_dir = "/home/vobile/05SVN/"
    png_path = result_file_dir + query_file+ "result.png"
    txt_path = result_file_dir  + query_file + "result.txt"
    print result_file_dir + query_file + "_result.txt"
    file_object = open(txt_path, 'w')
    file_object.writelines(result_file_content)
    file_object.close( )
     
    arr=[]
    arr.append("set terminal png size 800, 800 \n")
    arr.append("set output \""+png_path+"\"\n")
    arr.append("set grid \n")
    arr.append("plot \""+txt_path+"\" using 1:2 with linespoints title \"right count\" " +", \""+txt_path+"\" using 1:3 with linespoints title \"error count\" "+", \""+txt_path+"\" using 1:4 with linespoints  title \"unknown count\" \n")
     
    gnuf = open(result_file_dir+'tmp.gnu', 'w')
    gnuf.writelines(arr)
    gnuf.close()
     
    os.system('gnuplot '+result_file_dir+'tmp.gnu')
    print "result_file_dir",png_path
    
if __name__ == '__main__':
#     param = []
#     param.append({"id":"ABC" ,"text":"english","result":"TRUE"})
#     param.append({"id":"ABC" ,"text":"nihao","result":"FALSE"})
#     param.append({"id":"EFG" ,"text":"hello","result":"FALSE"})
#     param.append({"id":"EFG" ,"text":"hello two","result":"FALSE"})
#     
#     print 'training_prepare',req('http://localhost:8082/api/training_prepare', param)
#     
#     param = []
#     param.append({"id":"ABC"})
#     param.append({"id":"EFG" })
# 
#     print 'train_data',req('http://localhost:8082/api/train_data', param)
    
#     filter_title = "TEEN WOLF_S6_E605_TEEN WOLF"
#     filter_title = "At Midnight_S4_E4039_At Midnight"
# # #     init_thread(filter_title)
#     full_push(filter_title)
#     print 'train_data',req('http://' + HOST + '/api/train_data', [{"id":filter_title }])
    
# #     param = {u'text': u'download file', u'id': u'TEEN WOLF_S6_E605_TEEN WOLF', u'result': u'False'}
#     param = {"id":"At Midnight_S4_E4039_At Midnight" ,"text":"Midnight Express 1978 BDRip&hellip;rar"}
#     param = {"id":"At Midnight_S4_E4039_At Midnight" ,"text":"at midnight 2017 01 09 hdtv x264-crooks mkv"}
#     param = {"id":"At Midnight_S4_E4039_At Midnight" ,"text":"mkv"}
# # # #     
# #     param = {"id":"ABC" ,"text":"english"}
#     print 'search_train_data',req('http://' + HOST + '/api/search_train_data', param)

#     mySpider = SDU_Spider()
#     search_title_id = '11494275_8'
#     mySpider.sdu_init(search_title_id,20)
#     import_data_from_text(search_title_id + '.txt')
#     import_data_from_text('11705204_4.txt')
    
    import_data_from_text_train_only('11221433_10.txt')
    
#     import_data_from_diff_text('11494275_8.txt', "/home/vobile/05SVN/keyword_filter_api/lib/keyword_filter_api/method/11494275_8_TextOnly.txt")
