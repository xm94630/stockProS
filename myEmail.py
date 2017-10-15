#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import smtplib
from email.mime.text import MIMEText
from email.header import Header

def send(words):
    password   = raw_input("I want to sent email to target email('163邮箱'), need your keywords:\n> ") #密码

    sender     = 'xm94630@163.com'  #发信人地址
    receiver   = 'xm94630@163.com'  #收信人地址
    smtpserver = 'smtp.163.com'

    msg            = MIMEText(words, 'plain', 'utf-8') #中文需参数‘utf-8'，单字节字符不需要
    msg['Subject'] = Header('stocksInfo', 'utf-8')     #邮件标题
    msg['from']    = sender  
    msg['to']      = receiver 

    smtp = smtplib.SMTP()
    smtp.connect(smtpserver)
    smtp.login(sender, password)
    smtp.sendmail(sender, receiver, msg.as_string()) 
    smtp.quit()
    print "SUCCESS! 完成邮件发送!"

    return 


