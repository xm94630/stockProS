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

#清除旧的数据
def clearOldDatabase(bool=False):
    if bool:
        #删除全部原有数据
        print('清空全部旧数据')
        result = coll.delete_many({})
    else:
        print('在旧数据上追加')

#把抓取的一条数据，保存到 mongo 数据库
def save(data={}):  
    #插入一条数据
    result = coll.insert_one(data)
    return  

#某股票数据是否已经在数据库中存在
def getStock(symbol):
    cursor = coll.find({"symbol": symbol})
    return cursor



