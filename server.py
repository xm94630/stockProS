#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#上面的注释是用来支持中文，没有就会出错

from __future__ import division
from pymongo import MongoClient
import pymongo
from bson.json_util import dumps   #这个用来解析mongo返回的数据为json
import Cookie
import argparse #用来获取命令行参数

#连接数据库
client = MongoClient()
db = client.xm94630
coll = db.stocks

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
parser.add_argument('-s', dest='sort', action='store_true') #action 这个参数不能随便改，在我们的应用场景，就理解为不能改吧
args = parser.parse_args()
sortByLastYear = args.sort


#路由
@app.route("/",methods=["GET"])
def hello():

    #在函数中使用全局变量需要这里声明
    global sortByLastYear;
    
    #获取全部数据，并按照均值大小排序
    #注意，这部分一定要放在这里，不能在全局，否者的话，数据就为空，在页面中就看不到（也就是只有第一次才能有数据）。

    if sortByLastYear:
        cursor = coll.find().sort([("lastPrecent", pymongo.ASCENDING)])
    else:
        cursor = coll.find().sort([("percents.1", pymongo.ASCENDING)])

    template = env.get_template('index.html');
    return  template.render(data=cursor);


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






