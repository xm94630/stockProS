#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#导出文件
import time
import datetime
from operator import itemgetter

time     = datetime.datetime.now().strftime("%Y%m%d")
fileName = "backups/stock_" + time + ".txt"

#数据范例
# exmple = [{
#     'symbol': u'XX000000', 
#     'name': u'XX股票', 
#     'info': {
#         'pb': u'1', 
#         'totalShares2': 10, 
#         'pe_ttm': u'20', 
#         'buyNum2': 100, 
#         'buyNum': 100, 
#         'buyPercent': 0.5, 
#         'pe_lyr': u'20', 
#         'totalShares': u'100000000', 
#         'close': u'10.0'
#     }, 
#     'percents': ['-'], 
#     'lows': [['-'],9],
#     'averagePrecent':0.8,
# },{
#     'symbol': u'XX000000', 
#     'name': u'XX股票', 
#     'info': {
#         'pb': u'1', 
#         'totalShares2': 10, 
#         'pe_ttm': u'20', 
#         'buyNum2': 100, 
#         'buyNum': 100, 
#         'buyPercent': 0.5, 
#         'pe_lyr': u'20', 
#         'totalShares': u'100000000', 
#         'close': u'10.0'
#     }, 
#     'percents': ['-'], 
#     'lows': [['-'],1],
#     'averagePrecent':0.5,
# }]


#清空旧数据
f=open(fileName,'w');
f.truncate();
f.close();

#把全部数据排序后存入txt
def save(stockList={}): 
    
    #排序
    stockListNew = sorted(stockList, key=itemgetter('averagePrecent'));

    #文本内容
    content='';

    for stock in stockListNew:
        #写入一条数据
        content += stock['name']+ '['+stock['symbol'] +'] '+ u'推荐购买' + str(stock['info']['buyNum'])+u'股\n' 
        content += '[PB/TTM/LYR] '+ stock['info']['pb']+' / '+stock['info']['pe_ttm']+' / '+stock['info']['pe_lyr']+'\n'
        content += u'[n年内低点] '+ str(stock['lows'])+'\n'
        content += u'[n年内卖点占比] '+ str(stock['percents'])+'\n'
        content += u'[总股本] '+ str(stock['info']['totalShares2']) + u'亿'+'\n'
        content += u'--------------------------------------------------------------------'+'\n'

    with open(fileName, "a") as f:
        f.write(content.encode('utf-8'))

    f.close();
    return  









