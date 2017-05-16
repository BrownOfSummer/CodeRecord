#!/usr/bin/python
#-*- coding:utf-8 -*-

import urllib  
import urllib2
import cookielib
import re,os,errno
import string
from data_tranfor import data_tranfor

enable_proxy = False
proxy = "http://192.168.12.222:3128"
proxy_handler = urllib2.ProxyHandler({"http" : proxy})
none_proxy_handler = urllib2.ProxyHandler({})
# PF = None

def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc: # Python >2.5 (except OSError, exc: for Python <2.5)
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else: raise
        
class SDU_Spider:  
    # 申明相关的属性  
    def __init__(self):    
        self.cookieJar = cookielib.CookieJar()
        self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cookieJar))
        
        self.cookie_support= urllib2.HTTPCookieProcessor(cookielib.CookieJar())
        self.loginUrl = 'http://sso.vobile.net/signon/login.do?josso_back_to=http://vt-admin.vobile.net/josso_security_check&josso_partnerapp_id=VTAdmin'
        self.loginAction = 'http://sso.vobile.net/signon/usernamePasswordLogin.do'   # 登录的url
        self.login_post_data = urllib.urlencode({
                                        'josso_cmd':'login',
                                        'josso_back_to':'http://vt-admin.vobile.net/josso_security_check',
                                        'josso_username':'qi_haibin',
                                        'josso_password':'vobile-qhb',
                                        'localeSelected':'en_US',
                                        'submit':'Login',
                                        })
        self.resultUrl = 'http://vt-admin.vobile.net/pageDetail.action' # match confirm page
        self.result_post_data={
                                        'orderBy':'1',
                                        'order':'up',
                                        'oldStatus':'5',
                                        'idList':'11704942_55',
                                        'collapseFlag':'0',
                                        'videoId':'0',
                                        'companyIds':'',
                                        'trackingListIdForSelector':'0',
                                        'searchKeyForSelector':'',
                                        'pageSelector':'',
                                        'videoTitleId':'#3',
                                        'metaType':'0',
                                        'videoTitle':'',
                                        'searchKey':'',
                                        'searchType':'1',
                                        'websiteId':'1',
                                        'matchStatusSelect':'1',
                                        'status':'3',
                                        'matchType':'0',
                                        'matchDurationStart':'',
                                        'matchDurationEnd':'',
                                        'metaOffsetStart':'',
                                        'metaOffsetEnd':'',
                                        'clipDurationStart':'',
                                        'clipDurationEnd':'',
                                        'contributor':'0',
                                        'postDate':'0',
                                        'confirmBy':'0',
                                        'startDate':'2016-01-01',
                                        'endDate':'',
                                        'safeMode':'0',
                                        'confirmRuleId':'0',
                                        'page':'1',
                                        'detail':'1'
                                        }     # POST的数据

        if (enable_proxy):
            self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cookieJar),proxy_handler)
        else:
            self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cookieJar),none_proxy_handler)
        
    def sdu_init(self,idList,pages):
        # 初始化链接并且获取cookie
        result = self.opener.open(self.loginUrl)            # 访问登录页面，获取到必须的cookie的值
#         print "login page----------------------------",result.read()
         
        myRequest = urllib2.Request(url = self.loginAction,data = self.login_post_data)   # 自定义一个请求
        result = self.opener.open(myRequest)            # 访问登录页面，获取到必须的cookie的值
#         print "loginAction----------------------------",result.read()
        self.result_post_data['idList'] = idList
        file_dir = "/home/vobile/vt_spider_data/" + idList + "/"
        mkdir_p(file_dir)
        for i in range(1,pages):
            self.result_post_data['page'] = str(i)
            for j in range(2,4):
                self.result_post_data['status'] = str(j)
                print "reading page start", "status",j, "page",i
                result = self.opener.open(self.resultUrl, data=urllib.urlencode(self.result_post_data),timeout=300)       # 访问成绩页面，获得成绩的数据
                # 打印返回的内容
                html = result.read()
                file_object = open(file_dir +"/result" + str(j) + "_" + str(i) + ".txt", 'w')
                file_object.writelines(html)
                file_object.close()
                print "reading page end", "status",j, "page",i
#         print "result page----------------------------",html
#         soup = BeautifulSoup("".join(html))
#         rt['keyword'] = getKWfunc(soup, html, rurl)

        data_tranfor(file_dir)
        
    def find_title(self):
        title = soup.findAll("h1", class_="movie-title")[0].span.string.strip()
        rt.append(title)
#         result = urllib2.urlopen(self.loginUrl)  
#         print "login page----------------------------",result.read()
#         
#         result = urllib2.urlopen(url = self.loginAction,data = self.login_post_data)   # 自定义一个请求
#         print "loginAction----------------------------",result.read()
#         
#         result = urllib2.urlopen(self.resultUrl)       # 访问成绩页面，获得成绩的数据
#         # 打印返回的内容
#         print "result page----------------------------",result.read()
        

if __name__=='__main__':
    mySpider = SDU_Spider()  
    mySpider.sdu_init('11494275_8',2)
