#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#上面的注释是用来支持中文，没有就会出错

from __future__ import division
from pymongo import MongoClient

#前提
#1)开启数据库服务器
#2)已经创建好相应的数据库
#mongoimport --db xm94630 --collection stocks --drop --file ~/desktop/null.json
client = MongoClient()
db = client.xm94630
coll = db.stocks

#删除全部原有数据
#result = coll.delete_many({})

#把抓取的一条数据，保存到 mongo 数据库
def save(data={}):  
    #插入一条数据
    result = coll.insert_one(data)
    return  

