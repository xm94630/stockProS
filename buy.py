#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#上面的注释是用来支持中文，没有就会出错

import requests
import json
import sys 
import getCookie
import argparse
import common
import FA

if __name__ == '__main__':
    try:
        argArr   = sys.argv
        if(len(argArr)>=2):
            fileName = argArr[1]
    except:
        sys.exit(0)

#引入配置
conf = common.loadJsonFile('./config.json')
#头信息
#cookie    = getCookie.getCookie('https://xueqiu.com/');
cookie     = conf['cookie']
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

    #根据 latestCost 的初始值，反推pb
    #注意latestCost的初始值，指的是最初的买的时候的钱
    #print(round((5.0-oneStock["latestCost"]*3.0/10000.0)/2.0,2))

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

    try:
        #正常的操作#获取最新价格
        oneStock['current'] = data[symbol]['current']
    except:
        #发生异常，执行这块代码
        print '数据解析出错，可能是cookie问题，请尝试更新'

    #获取股票的近季度的利润情况
    oneStock['profit'] = FA.parseIncstatementData(symbol)

    #获取pe
    oneStock['pe_lyr'] = data[symbol]['pe_lyr']
    oneStock['pe_ttm'] = data[symbol]['pe_ttm']

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
        oneStock['nowCanUse'] = 0
        oneStock['nowCanBuyStockNumber'] = 0
        oneStock['nowCanBuyStockNumber2'] = 0

#导出信息(核心数据展示)
def printInfo(oneStock):
    #注意：这里字符串拼接的时候不要使用'【'，好像会出错，原因就不找了
    # 20180604  u'【中文**】' 这样子就可以哦

    kui = '';
    if oneStock['profit'][1]<0:
        kui += u'【亏】';

    printStr  = kui + oneStock['name'] + ' ['+oneStock['symbol']+'] ' + u' ，已经加仓['+ str(oneStock['jiacang'])+u']'
    printStr2 = '总配/已配/可用：' + str(int(oneStock['canUseMoney'])) +'/'+str(int(oneStock['latestCost']))+'/'+str(int(oneStock['nowCanUse']))
    chengben  = int(oneStock['nowCanBuyStockNumber2']) * float(oneStock['current']);

    if float(oneStock['latestPB'])<1:
        print(printStr+ u'，[破净]')
    else:
        print(printStr)

    # 20190103 新增
    print('PB / TTM / LYR ：'+ str(oneStock['latestPB']) +'/'+ str(oneStock['pe_ttm'])+'/'+ str(oneStock['pe_lyr']))
    
    if oneStock['nowCanBuyStockNumber']==0:
        print printStr2 + '，配置充裕'
    else:
        if oneStock['nowCanBuyStockNumber2']==0:
            print printStr2 + '，等待下跌'
        else:
            print printStr2 + '，推荐买入 '+ str(int(oneStock['nowCanBuyStockNumber2'])) + ' ('+str(int(oneStock['nowCanBuyStockNumber'])) +') 成本为：' + str(chengben)

    percent = exportPriceInfo(oneStock)
    prompt(percent)


#导出价格相关信息
def exportPriceInfo(oneStock):
    sPrice0 = oneStock['sPrice']
    sPrice1 = round(sPrice0*0.8,2)
    sPrice2 = round(sPrice1*0.8,2)
    sPrice3 = round(sPrice2*0.8,2)
    percent = round(float(oneStock['current'])/sPrice0,3);
    percentStr  = str(percent*100)+'%'
    percentStr2 = str(percent*100-100)+'%'
    print(percentStr+' / '+percentStr2+' / ['+str(sPrice0)+','+str(sPrice1)+','+str(sPrice2)+','+str(sPrice3)+ u'] / 当前股价：'+oneStock['current']);
    return percent

#根据下跌百分比，来提示处于哪个阶段的补仓
def prompt(percent):

    restInfo = '';

    if oneStock['profit'][1]<0:
        restInfo += '[亏]';

    if ((oneStock['nowCanBuyStockNumber']==0) or (oneStock['nowCanBuyStockNumber2']==0)):
        restInfo += '[不用处理：已经配置很充分啦(或者可以配置不足1手)]'
    elif (int(oneStock['nowCanUse'])<2000 and int(oneStock['nowCanUse'])>=1000):
        restInfo += '[不用处理：可用小于2000的不用处理]'
    elif int(oneStock['nowCanUse'])<1000:
        restInfo += '[不用处理：可用小于1000的不用处理]'

    if percent<=0.8:
        if percent<=0.64:
            if percent<=0.512:
                if percent>0:
                    print '===============================================================================================================>【第3阶】'+restInfo
            else:
                print '===============================================================================================================>【第2阶】'+restInfo
        else:
            print '===============================================================================================================>【第1阶】'+restInfo

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