#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#导出文件
import time
import datetime
from operator import itemgetter
import os

#引入自定义模块
import dataBase

#数据范例
exmple = [{
    'symbol': u'XX000000', 
    'name': u'符合股票', 
    'info': {
        'pb': u'1', 
        'totalShares2': 10, 
        'pe_ttm': u'20', 
        'buyNum2': 100, 
        'buyNum': 100, 
        'buyPercent': 0.5, 
        'pe_lyr': u'20', 
        'totalShares': u'100000000', 
        'close': u'10.0'
    }, 
    'percents': [[.5,.5,.5,.5,.5,.5],.5], 
    'lows': [[5,5,5,5,5,4],10],
    'averagePrecent':0.8,
},{
    'symbol': u'XX000000', 
    'name': u'不符合股票', 
    'info': {
        'pb': u'1', 
        'totalShares2': 10, 
        'pe_ttm': u'20', 
        'buyNum2': 100, 
        'buyNum': 100, 
        'buyPercent': 0.5, 
        'pe_lyr': u'20', 
        'totalShares': u'100000000', 
        'close': u'10.0'
    }, 
    'percents': [[.5,.5,.5,.5,.5,.5],.5], 
    'lows': [[5,5,5,5,5,-999],10],#不符合
    'averagePrecent':0.5,
},{
    'symbol': u'XX000000', 
    'name': u'不符合股票', 
    'info': {
        'pb': u'1', 
        'totalShares2': 10, 
        'pe_ttm': u'20', 
        'buyNum2': 100, 
        'buyNum': 100, 
        'buyPercent': 0.5, 
        'pe_lyr': u'20', 
        'totalShares': u'100000000', 
        'close': u'10.0'
    }, 
    'percents': [[.5,.5,.5,.5,.5,.5],1.2],#不符合 
    'lows': [[5,5,5,5,5,4],10],
    'averagePrecent':0.8,
},]


#构建文件名字
def createFileName():
    #获取保存的时间戳，并格式化
    myTime   = dataBase.getTime()[0]['time']
    myTime   = time.strftime('%Y%m%d_%a_%H%M%S',  time.localtime(myTime))
    
    path     = "backups/"     
    name     = myTime + ".txt"
    fileName = path + name
    return fileName


#把全部数据排序后存入txt
def save(stockList={}): 

    fileName = createFileName()

    #清空旧数据
    f=open(fileName,'w');
    f.truncate();
    f.close();

    #排序
    stockListNew = sorted(stockList, key=itemgetter('averagePrecent'));

    #文本内容
    content='';

    for stock in stockListNew:

        #当数组中没有-999的时候处理：
        #~~将布尔值转为0（False）或者1（True），
        if ~~(-999 in stock['lows'][0])==0 :

            if stock['percents'][0][0]<=1 and stock['percents'][0][1]<=1 and stock['percents'][0][2]<=1 and stock['percents'][0][3]<=1 and stock['percents'][0][4]<=1 and stock['percents'][0][5]<=1 and stock['percents'][1]<=1 :
                
                #写入一条数
                content += stock['name']+ '['+stock['symbol'] +'] '+ u'推荐购买' + str(stock['info']['buyNum'])+u'股\n' 
                content += stock['continueDaysText']+ u'，合计涨/跌百分比：' + str(stock['upOrDownContinuePercent']) + '\n'
                content += '[PB/TTM/LYR] '+ str(stock['info']['pb'])+' / '+str(stock['info']['pe_ttm'])+' / '+str(stock['info']['pe_lyr'])+'\n'
                content += u'[n年内低点] '+ str(stock['lows'])+'\n'
                content += u'[n年内卖点占比] '+ str(stock['percents'])+'\n'
                content += u'[总股本] '+ str(stock['info']['totalShares2']) + u'亿'+'\n'
                content += u'--------------------------------------------------------------------'+'\n'

    with open(fileName, "a") as f:
        f.write(content.encode('utf-8'))

    f.close();
    return fileName;

#print save(exmple);


# 判断文件加是否存在
path = "backups/"
if not os.path.exists(path):
    print "新建 backups 文件夹，用来保存导出文本数据"
    os.makedirs(path)






