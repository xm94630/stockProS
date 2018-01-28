#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#上面的注释是用来支持中文，没有就会出错

import requests
import json
import sys 
import getCookie
import argparse

import common

if __name__ == '__main__':
    try:
        fileName = sys.argv[1]
    except:
        sys.exit(0)

#引入配置
conf = common.loadJsonFile('./config.json')
#头信息
cookie = getCookie.getCookie('https://xueqiu.com/');
userAgent  = conf['userAgent']
# 每只股票最大可配置额度
maxMoneyPerStock = conf['maxMoneyPerStock']

# 定义
myStockArr = []

#需要抓取的数据源
stockInfoAPI = 'https://xueqiu.com/v4/stock/quote.json'; #详细


print '============= 股票加仓提示 ============='

#获取股票详情
def getStockInfoData(url,oneStock):
    symbol = oneStock["symbol"]
    _headers = {
        "User-Agent":userAgent,
        "Cookie":cookie
    }
    _params = '&code=' + symbol;
    res = requests.get(url=url,params=_params,headers=_headers)
    data = json.loads(res.text);
    return data;


# 根据pb获取配置额度
def getMoney(pb):
    money = (5-2*float(pb))* (maxMoneyPerStock/3)
    return money

# 解析一只股票
def parseStock(oneStock):
    symbol = oneStock["symbol"]
    data = getStockInfoData(stockInfoAPI,oneStock)
    #获取最新pb
    latestPB = data[symbol]['pb']
    oneStock['latestPB'] = latestPB
    #根据pb获取配置额度
    money = getMoney(latestPB)
    oneStock['canUseMoney'] = money
    #是否可以继续配置
    if money - oneStock['latestCost']>0:
        canContinueBuy = True
        oneStock['canContinueBuy'] = canContinueBuy
    else:
        canContinueBuy = False
        oneStock['canContinueBuy'] = canContinueBuy
    #如果可以配置的话，还能配置多少股
    if canContinueBuy:
        nowCanUse = money - oneStock['latestCost']
        nowCanBuyStockNumber = nowCanUse / float(data[symbol]['current'])
        nowCanBuyStockNumber = int(round(nowCanBuyStockNumber,0))
        nowCanBuyStockNumber2 = int(round(nowCanBuyStockNumber/100))*100
        oneStock['nowCanUse'] = nowCanUse
        oneStock['nowCanBuyStockNumber'] = nowCanBuyStockNumber
        oneStock['nowCanBuyStockNumber2'] = nowCanBuyStockNumber2
    else:
        oneStock['nowCanUse'] = -1
        oneStock['nowCanBuyStockNumber'] = -1
        oneStock['nowCanBuyStockNumber2'] = -1

#导出信息(核心数据展示)
def printInfo(oneStock):
    #注意：这里字符串拼接的时候不要使用'【'，好像会出错，原因就不找了
    print(oneStock['name'] + ' ['+oneStock['symbol']+'] (pb:' + str(oneStock['latestPB']) +')')
    if float(oneStock['latestPB'])<1:
        print '提示：该股票已经破净'
    if oneStock['canContinueBuy']:
        print('总配/已配/可用：' + str(int(oneStock['canUseMoney'])) +'/'+str(int(oneStock['latestCost']))+'/'+str(int(oneStock['nowCanUse'])))
        if int(oneStock['nowCanBuyStockNumber2'])!=0:
            print('推荐买入 '+ str(int(oneStock['nowCanBuyStockNumber2'])) + ' ('+str(int(oneStock['nowCanBuyStockNumber'])) +') ')
        else:
            print '建议等待下跌'

#导出信息(全部数据展示)
def printInfo2(oneStock):
    print(oneStock['name'] + ' ['+oneStock['symbol']+'] (pb:' + str(oneStock['latestPB']) +')')
    if float(oneStock['latestPB'])<1:
        print '提示：该股票已经破净'
    print('总配/已配/可用：' + str(int(oneStock['canUseMoney'])) +'/'+str(int(oneStock['latestCost']))+'/'+str(int(oneStock['nowCanUse'])))
    print('推荐买入 '+ str(int(oneStock['nowCanBuyStockNumber2'])) + ' ('+str(int(oneStock['nowCanBuyStockNumber'])) +') ')


# 初始
if __name__ == "__main__":
    myStockArr = common.loadJsonFile(fileName)
    for oneStock in myStockArr:
        #解析计算
        parseStock(oneStock)
        #导出信息
        printInfo(oneStock)
        #分割线
        print('--------------------------------------------------------------------------------------------------------------- ')