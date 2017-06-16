#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import smtplib
from email.mime.text import MIMEText
from email.header import Header

def send():
    password   = raw_input("I want to sent email to target email, need your keywords:\n> ") #密码

    sender     = 'xm94630@126.com'  #发信人地址
    receiver   = 'xm94630@126.com'  #收信人地址
    words      = '你好吗'            #邮件正文
    smtpserver = 'smtp.163.com'

    msg            = MIMEText(words, 'plain', 'utf-8') #中文需参数‘utf-8'，单字节字符不需要
    msg['Subject'] = Header('stocksInfo', 'utf-8')     #邮件标题
    msg['from']    = sender  
    msg['to']      = receiver 

    smtp = smtplib.SMTP()
    smtp.connect('smtp.126.com')
    smtp.login(sender, password)
    smtp.sendmail(sender, receiver, msg.as_string()) 
    smtp.quit()
    print "邮件发送成功!"

    return 


