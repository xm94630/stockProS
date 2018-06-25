#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# 【财务分析】

# 现金流表
# https://xueqiu.com/stock/f10/cfstatement.json?symbol=SH601088&page=1&size=4&_=1522730045413
# mananetr       经营活动产生的现金流量
# invnetcashflow 投资活动产生的现金流量
# finnetcflow    筹资活动产生的现金流量
# 返回数据格式
# {
# 	"list": [{
#       "mananetr": 1.181E10,
# 		"invnetcashflow": -2.179E9,
#       "finnetcflow": -4.66E9,
# 	}],
# 	"name": "中国神华"
# }

# 利润表
# https://xueqiu.com/stock/f10/incstatement.json?symbol=SH601088&page=1&size=4&_=1522730476614
# parenetp 净利润

# 资产负债表
# https://xueqiu.com/stock/f10/balsheet.json?symbol=SH601088&page=1&size=4&_=1522730522067

import requests
import common
import json

#引入配置
conf = common.loadJsonFile('./config.json')
#头信息
cookie     = conf['cookie']
userAgent  = conf['userAgent']

#解析json
class Payload(object):
    def __init__(self, j):
        self.__dict__ = json.loads(j)

# url
cfstatementUrl  = 'https://xueqiu.com/stock/f10/cfstatement.json'
incstatementUrl = 'https://xueqiu.com/stock/f10/incstatement.json'

# 获取 现金流表 数据
def getCfstatementData(cfstatementUrl,symbol):
    _headers = {
        "User-Agent":userAgent,
        "Cookie":cookie
    }
    _params = '&symbol=' + symbol
    res = requests.get(url=cfstatementUrl,params=_params,headers=_headers)
    return res.text

# 获取 利润表 数据
def getIncstatementData(incstatementUrl,symbol):
    _headers = {
        "User-Agent":userAgent,
        "Cookie":cookie
    }
    _params = '&symbol=' + symbol
    res = requests.get(url=incstatementUrl,params=_params,headers=_headers)
    return res.text


# 利润
def parseCfstatementData(symbol):
    json = getCfstatementData(cfstatementUrl,symbol)
    try:
        #正常的操作
        data = Payload(json)
    except:
        #发生异常，执行这块代码
        print '【xm】接口崩坏！'
        print json
    
    arr = data.list

    str1 = ''
    str2 = ''
    str3 = ''
    
    for one in arr:
        if one['mananetr']>=0:
           str1 = str1+'■'
        else:
           str1 = str1+'□'
        
        if one['invnetcashflow']>=0:
           str2 = str2+'■'
        else:
           str2 = str2+'□'

        if one['finnetcflow']>=0:
           str3 = str3+'■'
        else:
           str3 = str3+'□'

    r = [str1,str2,str3]
    
    # print r[0]
    # print r[1]
    # print r[2]
    
    return r

# 现金流
def parseIncstatementData(symbol):
    json = getIncstatementData(incstatementUrl,symbol)
    try:
        #正常的操作
        data = Payload(json)
    except:
        #发生异常，执行这块代码
        print '【xm】接口崩坏！'
        print json
    
    arr = data.list

    str4 = ''
    newInc = 0
    
    if len(arr)!=0:
        for one in arr:
            if one.has_key('parenetp'):
                if one['parenetp']>=0:
                    str4 = str4+'+'
                else:
                    str4 = str4+'-'
            else:
                str4 = str4+'?'
        if arr[0].has_key('parenetp'):
            newInc =  round(arr[0]['parenetp']/100000000,2)
    else:
        str4 = '?'
        newInc = 0
    

    # 历史正负数据，和最近季度的净利润（单位：亿）
    r = [str4,newInc]
    
    #print r[0]
    #print r[1]
    
    return r

#parseCfstatementData('SH601088')
#parseCfstatementData('SH600585')
#parseCfstatementData('SH600340')
#parseCfstatementData('SZ000651')
#parseCfstatementData('SH600519')

#parseIncstatementData('SZ300118')






