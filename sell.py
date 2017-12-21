#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#上面的注释是用来支持中文，没有就会出错

import requests
import json
import sys 
import getCookie
import argparse

if __name__ == '__main__':
    try:
        fileName = sys.argv[1]
    except:
        sys.exit(0)

# 重要配置
# 每只股票最大可配置额度
maxMoneyPerStock = 10000 

# 定义
myStockArr = []

#需要抓取的数据源
stockInfoAPI = 'https://xueqiu.com/v4/stock/quote.json'; #详细

#头信息
cookieByJS = 'device_id=1a598ee68fd9ab4a9a0de8480363df28; __utma=1.61397162.1511428575.1512459192.1512555561.5; __utmz=1.1512555561.5.5.utmcsr=localhost:5000|utmccn=(referral)|utmcmd=referral|utmcct=/; xq_a_token=95b69ccb71a54ebf3d7060a84a72b45015fead7f; xq_a_token.sig=r7RhUAkpd9FiBmPDlOV3F-V8LFo; xq_r_token=6589f21e3e52d21c4d3de00d3135b3920fa8a52f; xq_r_token.sig=Ho5fiQYDNIITpBXlltLZVADXRSI; u=911513824494184; Hm_lvt_1db88642e346389874251b5a1eded6e3=1512555561,1512555672,1512555678,1513824495; Hm_lpvt_1db88642e346389874251b5a1eded6e3=1513824495'
cookie = cookieByJS+getCookie.getCookie('https://xueqiu.com/');
userAgent  = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36';


print '============= 股票加仓提示 ============='

# 保存json数据
def store(fileAddress,data):
    with open(fileAddress, 'w') as json_file:
        json_file.write(json.dumps(data))

# 读取json数据
def load(fileAddress):
    with open(fileAddress) as json_file:
        try:
            #正常读取
            data = json.load(json_file)
            return data
        except:
            #发生异常
            print '警告：json格式有误！请重新编辑你的股票配置'
            print '============= 程序已经中断 ============='
            sys.exit(0) 

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
    myStockArr = load(fileName)
    for oneStock in myStockArr:
        #解析计算
        parseStock(oneStock)
        #导出信息
        printInfo(oneStock)
        #分割线
        print('--------------------------------------------------------------------------------------------------------------- ')