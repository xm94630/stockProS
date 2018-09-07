#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#上面的注释是用来支持中文，没有就会出错

from __future__ import division
from pymongo import MongoClient
import pymongo
from bson.json_util import dumps   #这个用来解析mongo返回的数据为json
import Cookie
import argparse #用来获取命令行参数
import common

#连接数据库
client = MongoClient()
db = client.xm94630
coll = db.stocks
coll2 = db.timeInfo

#全局数据
sortByLastYear = False  #根据最近一年卖点占比排序

# 服务
from flask import Flask,request
app = Flask(__name__)

from jinja2 import Environment, PackageLoader, select_autoescape
env = Environment(
    #注意，这里的 "server" 是填的 server.py 这个服务本身的这个模块
    #'tpl'是模板所在的文件夹名字
    loader=PackageLoader('server', 'tpl'),
    autoescape=select_autoescape(['html', 'xml'])
)


#获取命令行参数
parser = argparse.ArgumentParser()
parser.add_argument('-PB', dest='sortByIndustryAndPB', action='store_true') #action 这个参数不能随便改，在我们的应用场景，就理解为不能改吧
parser.add_argument('-PE', dest='sortByIndustryAndPE', action='store_true')
args = parser.parse_args()


#排序类别确认
if args.sortByIndustryAndPB == True:
    # 第一级别按照行业排序，第二级别按照PB排序
    sortType = 2
elif args.sortByIndustryAndPE == True:
    # 第一级别按照行业排序，第二级别按照PE排序
    sortType = 3
else:
    #排序类型 默认按pb从低到高排序
    sortType = 1


#路由
@app.route("/",methods=["GET"])
def hello():

    #在函数中使用全局变量需要这里声明
    global sortType;
    
    #获取全部数据，并按照均值大小排序
    #注意，这部分一定要放在这里，不能在全局，否者的话，数据就为空，在页面中就看不到（也就是只有第一次才能有数据）。

    if sortType==2:
        #这里支持多个字段的排序
        #其实这个方式我一直就想到了，但是没有成功，因为字段对应的数据之前是字符串，导致的问题，现在已经转化为浮点数了！
        cursor = coll.find().sort([("industryId", pymongo.ASCENDING), ("info.pb", pymongo.ASCENDING)])
    elif sortType==3:
        cursor = coll.find().sort([("industryId", pymongo.ASCENDING), ("info.pe_ttm", pymongo.ASCENDING)])
    else:
        cursor = coll.find().sort([("info.pb", pymongo.ASCENDING), ("industryId", pymongo.ASCENDING)])




    #从数据库获取时间信息
    cursor2 = coll2.find({})

    #这个是用来看 cursor 字符串类型的内容的，方便查看
    #print dumps(cursor2)    #dumps后得到的类型是 <type 'str'>
    try:
        #正常的操作
        myTimeStr = cursor2[0]['timeStr']
    except:
        #发生异常，执行这块代码
        myTimeStr = u'还没有时间信息，运行 python index.py 获取时间'

    template = env.get_template('index.html');
    return  template.render(data=cursor,timeInfo=myTimeStr);




@app.route("/api/getStocks/",methods=["GET"])
def api():
    cursor = coll.find().sort([("percents.1", pymongo.ASCENDING)]);
    jsonStr = dumps(cursor);

    # 获取get参数的方法
    # a = request.args.get('a');
    # print(a);

    # jonp 的写法
    # 获取 callback 参数的方法
    # 这个“callback”可以在jquery的jonp方法中定义
    # 这个接口调用方法如下： http://127.0.0.1:5000/api/getStocks/?callback=xxx
    cb = request.args.get('callback');

    #这里是获取请求中带过来的cookie
    #这里增加了对cookie的要求，必须有带token为123456的cookie
    cookieStr = request.headers.get('Cookie') 
    if cookieStr:
        cookie = Cookie.SimpleCookie()
        cookie.load(cookieStr.encode('utf-8'))   # .encode('utf-8') 非常重要

        token =  cookie['token'].value
        if(token != '123456'):
            template = env.get_template('404.html');
            return  template.render();
        
        try:
            jsonStr = cb+'('+jsonStr+')'
            return jsonStr;
        except:
            return '接口使用方式有点问题哦'

    else:
        template = env.get_template('404.html');
        return  template.render();


#添加允许跨域头
# @app.after_request
# def add_header(response):
#     response.headers['Access-Control-Allow-Origin'] = '*'
#     return response

if __name__ == "__main__":
    #只能本机访问
    #app.run()
    
    #这样子写就可以支持LAN访问
    #注意，如果是服务不能访问，有可能的原因就是没有启动mongo数据库
    app.run('0.0.0.0')






