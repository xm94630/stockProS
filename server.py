#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#上面的注释是用来支持中文，没有就会出错

from __future__ import division
from pymongo import MongoClient
import pymongo


#连接数据库
client = MongoClient()
db = client.xm94630
coll = db.stocks



# 服务
from flask import Flask
app = Flask(__name__)

from jinja2 import Environment, PackageLoader, select_autoescape
env = Environment(
    #注意，这里的 "server" 是填的 server.py 这个服务本身的这个模块
    #'tpl'是模板所在的文件夹名字
    loader=PackageLoader('server', 'tpl'),
    autoescape=select_autoescape(['html', 'xml'])
)

@app.route("/")
def hello():
    
    #获取全部数据，并按照均值大小排序
    #注意，这部分一定要放在这里，不能在全局，否者的话，数据就为空，在页面中就看不到（也就是只有第一次才能有数据）。
    cursor = coll.find().sort([("percents.1", pymongo.ASCENDING)])

    template = env.get_template('index.html');
    return  template.render(data=cursor);

if __name__ == "__main__":
    app.run()
