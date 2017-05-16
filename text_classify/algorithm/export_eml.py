#!/usr/bin/python
#-*- coding:utf-8 -*-

from email import generator
from email.mime.text import MIMEText

mailto_list = [] # 邮件接收方的邮件地址
mail_user = "filter_sender@vobile.cn" # 邮件发送方的邮箱账号

class Gen_Emails(object):
    def __init__(self):
        pass

    def EmailGen(self, outfile_name, sub, content=""):

        msg = MIMEText(content, _charset='utf-8')
        msg['Subject'] = sub  # 邮件主题
#         msg['From'] = mail_user
#         msg['To'] = ";".join(mailto_list)
        msg['From'] = ""
        msg['To'] = ""
        self.SaveToFile(msg, outfile_name)

    def SaveToFile(self,msg, outfile_name):
        with open(outfile_name, 'w') as outfile:
            gen = generator.Generator(outfile)
            gen.flatten(msg)
            
if __name__=='__main__':
    mail_object = Gen_Emails()
    mail_object.EmailGen("1.eml","Test Sub","Test Obj")
