#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#上面的注释是用来支持中文，没有就会出错

# 注意 本文件是根据 buy.py 复制修改的，另外也是用了 index.py 部分的功能

import requests
import json
import sys 
import getCookie
import argparse
import common

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




############################################################################################
#  这个部分是复制的 index.py 中获取年内低点的功能（START）
############################################################################################
#配置
import time
nowTime = str(int(time.time() * 1000));
config2  = [
    'period=1day',
    'type=before',
    '_='+nowTime,
];

#需要抓取的数据源
baseUrl      = 'https://xueqiu.com/stock';
stockAPI     = baseUrl+'/forchartk/stocklist.json';      #K

#解析json
class Payload(object):
    def __init__(self, j):
        self.__dict__ = json.loads(j)

#调整数据
#比如有数据为：[[18.91, 241], [18.91, 486], [11.11, 732], [10.51, 732], [9.68, 732], [9.68, 732]];
#从第4年开始数据长度就没有发生改变了，就说明不存在第四年的数据，后面的年份就更加不存在了，要调整数据为：
#调整目标数据为：[[18.91, 241], [18.91, 486], [11.11, 732], [-999, 732], [-999, 732], [-999, 732]]
#进一步提取为：[18.91, 18.91, 11.11, -999, -999, -999]
def modData(arr):

    #arr = [[18.91, 241], [18.91, 486], [11.11, 732], [10.51, 732], [9.68, 732], [9.68, 732]];
    newArr = [];
    length = len(arr);
    for i in range(0,length-1):
        if arr[i][1]==arr[i+1][1]:
            #不存在的年份用-999填空，为何不是0呢？因为0不好区分，这中情况可是正常存在的，包括出现 -4 这样子也是合理的（因为前赋权）
            arr[i+1][0] = -999;

    for i in range(0,length):
        newArr.append(arr[i][0]);

    #返回 低点价格数组
    return newArr

#某个股 N年内 每天价格集合
def getStockDetail(url,config,symbol,nYear):

    _year     = nYear;
    _interval = int(_year * 31536000 * 1000);
    _end      = int(time.time() * 1000);  #坑 一定要转成整数，否者后来都会是float类型
    _begin    = _end - _interval;

    _headers = {
        "User-Agent":userAgent,
        "Cookie":cookie
    }
    _params = "&".join(config);

    _params = _params+'&symbol='+symbol;
    _params = _params+'&end='+ str(_end);
    _params = _params+'&begin='+ str(_begin);

    #print(_params)

    #不要太频
    # print '接口2：K接口，休息一下（'+ str(nYear) +'年内价格处理）'
    # time.sleep(sleep2);

    try:
        #正常的操作
        res = requests.get(url=url,params=_params,headers=_headers)
    except:
        #发生异常，执行这块代码
        print '【xm】接口2有点问题哦'
        #print res

    return res.text;

#该股票第n年内的最低点
def getLowPrice(n,data):

    lows = []
    myLen=0

    _interval = int( (n+1)*31536000*1000 );
    _now      = int(time.time() * 1000);
    _begin    = _now - _interval;

    for one in data:
        # 时间的格式为
        # Mon Jun 19 00:00:00 +0800 2017
        mytime = one['time']
        timestamp = time.mktime( time.strptime(mytime, "%a %b %d %H:%M:%S %Y") )
        #扩大1000倍，并转化为整数，方便比较
        timestamp = int(timestamp * 1000);

        #只处理合理范围内的
        if timestamp>= _begin:
            low = one['low'];
            lows.append(low);
            myLen=myLen+1;

    if len(lows)==0:
        print "该年份没有数据（可能已经停牌了有一年多了...）"
        # 伪造一个数据，为了让程序跑通，后期会把价格中有-999的股票都会被过滤~
        lows = [-999]

    m = sorted(lows)[:1][0]

    #这里返回最低点、和总数据条数
    #总数据条数 会用来判断，这个股票是否不足六年（比如第4年和第3年数据一样多，说明其实不存在第四年的数据！）
    #[最低点，数据条数]
    return [m,myLen];

#获取最近连续上涨或下跌的天数(价格按照最近1天到最近第10天顺序)
def getContinuityDay(arr):

    #最近10天价格
    #print arr

    #首先确认是涨势还是跌势，用flag标记
    d1 = arr[0]
    d2 = arr[1]
    flag = 0 #0表示不变，1表示连续涨，-1表示连续跌
    if d1>d2:
        flag = 1
    elif d1<d2:
        flag = -1
    else:
        pass

    #统计连续的次数
    sum = 0
    for i,one in enumerate(arr):
        if i==0:
            pass
        elif flag==1 and arr[i]<arr[i-1]:
            sum=sum+1
        elif flag==-1 and arr[i]>arr[i-1]:
            sum=sum-1
        else:
            break

    return sum

#获取该股票 6年内每天价格数据
def getLowPriceArr(symbol,nYear):

    total = nYear

    # 获取六年内的全部
    # 之前这部分的实现是通过调用六次接口，这里为了减少接口访问频率，其他的年份就需要自己手动从这里提取
    stockInfo = getStockDetail(stockAPI,config2,symbol,nYear)

    #修改字符串中的数据（删除 '+0800 '）
    stockInfo = stockInfo.replace('+0800 ','')

    arr = Payload(stockInfo).chartlist

    #获取当天的涨跌幅
    upOrDownPercent = arr[-1]["percent"];

    #令最近一天的收盘价格作为最新价格，来分析用
    newClosePrice = arr[-1]["close"];

    #1年内~6(N)年内
    #把每个股票的低点和处理数据个数存到一个大数组中
    arr2 = []
    while nYear>0:
        low = getLowPrice( total-nYear , arr )
        nYear = nYear-1;
        arr2.append(low)

    arr3 = modData(arr2)


    #获取最近(这里只获取10天)连续上涨或下跌的天数
    
    #print(len(arr))

    if len(arr) < 10 :
        #发现数组长度只有2的情况...查找原因是一只昨天刚上市的新股...
        print('警告，这里数据有点问题！可能是一只新股')
        lastTenDays = [
            0,0,0,0,0,0,0,0,0,0,
        ]
    else:
        lastTenDays = [
            arr[-1]["close"],
            arr[-2]["close"],
            arr[-3]["close"],
            arr[-4]["close"],
            arr[-5]["close"],
            arr[-6]["close"],
            arr[-7]["close"],
            arr[-8]["close"],
            arr[-9]["close"],
            arr[-10]["close"],
        ]
    continueDays    = getContinuityDay(lastTenDays)
    continueDaysAbs = abs(continueDays) #绝对值

    #中文渲染
    continueDaysText = ''
    if continueDays>0:
        continueDaysText = u'涨'+str(continueDaysAbs)
    elif continueDays<0:
        continueDaysText = u'跌'+str(continueDaysAbs)
    else:
        continueDaysText = u'平'

    #获取连续的涨跌之和
    upOrDownContinuePercent = getUpOrDownPercent(arr,continueDaysAbs)

    #提炼数据
    return [ arr3, newClosePrice, continueDays,continueDaysText,upOrDownPercent,upOrDownContinuePercent]

#获取连续的涨跌之和
def getUpOrDownPercent(arr,continueDaysAbs):
    total = 0
    for index in range(continueDaysAbs):
        total = total + arr[-1*index-1]["percent"]
    return total
############################################################################################
#  这个部分是复制的 index.py 中获取年内低点的功能（END）
############################################################################################







print '============= 股票盈利卖出点位参考 ============='

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

    #获取最新价格
    oneStock['current'] = data[symbol]['current']

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

    #非常核心的数据提炼部分1
    lows = getLowPriceArr(symbol,6)
    oneStock['lows'] = lows

#导出信息(核心数据展示)
def printInfo(oneStock):

    #每股价格（当前价格）
    a1 = float(oneStock['current'])
    #每股价格（一年内低点）
    a2 = float(oneStock['lows'][0][0])
    #当前价格比低点涨幅
    a3 = round((a1-a2)/a2*100,1)

    #市值（当前）
    b1 = float(oneStock['current']) * oneStock['number']
    #市值（成本）
    b2 = float(oneStock['latestCost'])
    #当前市值比成本涨幅
    b3 = round((b1-b2)/b2*100,1)

    print(u"【"+oneStock['name']+u"】"+oneStock['symbol'] + "  ("+ str(oneStock['number']) + u"股)")
    print u"比低点涨了：" + str(a3) + "%" + u"，当前的价格：" + str(a1) + u"，一年低价格：" + str(a2)
    print u"市值涨幅：" + str(b3) + "% (" + str(int(b1-b2)) + ")" + u"，当前市值：" + str(b1) + u"，成本总计：" + str(b2) 

    n = int(a3/50)
    if(n>=1):
        print "'==============================================================================================================>恭喜，【第" + str(n) + "阶】卖点达成! " + str(n*50) +"%"


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


