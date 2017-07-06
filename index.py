#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#上面的注释是用来支持中文，没有就会出错


from __future__ import division

#这个需要先 pip install requests
import requests
import json
import math
import time
import argparse #用来获取命令行参数

#导入自己写的
import dataBase
import exportFile
import getCookie
import myEmail


#头信息
#cookie = 'aliyungf_tc=AQAAAPmR3X3Y0QwAopuP2+mfwa3X68B9; xq_a_token=876f2519b10cea9dc131b87db2e5318e5d4ea64f; xq_a_token.sig=dfyKV8R29cG1dbHpcWXqSX6_5BE; xq_r_token=709abdc1ccb40ac956166989385ffd603ad6ab6f; xq_r_token.sig=dBkYRMW0CNWbgJ3X2wIkqMbKy1M; u=571496720504862; s=f811dxbvsv; Hm_lvt_1db88642e346389874251b5a1eded6e3=1495547353,1496562578,1496717217,1496718108; Hm_lpvt_1db88642e346389874251b5a1eded6e3=1496806200; __utma=1.1590213924.1496727484.1496757368.1496806200.6; __utmc=1; __utmz=1.1496727484.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none)';
#20170613 更新
#cookie = 's=f811dxbvsv; aliyungf_tc=AQAAAFAqgS6SyAYA4Ah6ey0pwRiXjXtN; device_id=a0ff6c142e7ace69832875472cd91de6; __utma=1.1590213924.1496727484.1497109649.1497115287.13; __utmc=1; __utmz=1.1497115287.13.2.utmcsr=localhost:5000|utmccn=(referral)|utmcmd=referral|utmcct=/; xq_a_token=445b4b15f59fa37c8bd8133949f910e7297a52ef; xq_a_token.sig=5qsKG3NMR_Go5O8QjcKxalfFwhM; xq_r_token=132b2ba19b0053bc7f04401788b6e0d24f35d365; xq_r_token.sig=1w18Bj12xS0s6jGzDJnEQgA8IGo; u=961497324207636; Hm_lvt_1db88642e346389874251b5a1eded6e3=1497115461,1497115500,1497115551,1497115634; Hm_lpvt_1db88642e346389874251b5a1eded6e3=1497324738';
#20170614 更新
cookieByJS = 'aliyungf_tc=AQAAAFxDNmN7/wkAtQF6e1QFKSdh4y9K; u=921498661946832; device_id=73b08e95a2f0360b3f8c6bd62ed028f7; Hm_lvt_1db88642e346389874251b5a1eded6e3=1498552370,1498552425,1498552545,1498660709; Hm_lpvt_1db88642e346389874251b5a1eded6e3=1498661948'
cookie = cookieByJS+getCookie.getCookie('https://xueqiu.com/');
userAgent  = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36';


#配置
nowTime = str(int(time.time() * 1000));
config = [
    'category=SH',
    'exchange=',
    'areacode=',
    'indcode=',
    'orderby=symbol',
    'order=desc',
    'current=ALL',
    'pct=ALL',
    'pb=1_2',           #PB
    'pettm=0_20',       #PE/TTM
    'pelyr=0_20',       #PE/LYR
    '_='+nowTime,
];
config2  = [
    'period=1day',
    'type=before',
    '_='+nowTime,
];
config3  = [
    '_='+nowTime,
];
#行业配置多少钱
industryPrice = 10000;
#接口sleep时间(单位秒)
sleep1 = 0;
sleep2 = 1;
sleep3 = 1;


#需要抓取的数据源
baseUrl      = 'https://xueqiu.com/stock';
screenerAPI  = baseUrl+'/screener/screen.json';          #检索
stockAPI     = baseUrl+'/forchartk/stocklist.json';      #K
stockInfoAPI = 'https://xueqiu.com/v4/stock/quote.json'; #详细


#所有的数据列表
stockArr = []
#处理完成的条数，用来提示进度
dealNum = 0
#是否需要清空数据库重新抓取
isClearOld = False

#获取命令行参数
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-n', dest='new', action='store_true')
    #parser.add_argument('-o', '--output')
    args = parser.parse_args()
    isClearOld = args.new


#是否清除旧数据
dataBase.clearOldDatabase(isClearOld);


#股票类
def Stock(name=0, symbol=1,lows=[],percents=[],info={},averagePrecent=0,continueDays=0,continueDaysText='',upOrDownPercent=0,upOrDownContinuePercent=0):
    return{
        "name"     : name,
        "symbol"   : symbol,
        "lows"     : lows,
        "percents" : percents,
        "info"     : info,
        "averagePrecent"   : averagePrecent,
        "continueDays"     : continueDays,
        "continueDaysText" : continueDaysText,
        "upOrDownPercent"         : upOrDownPercent,
        "upOrDownContinuePercent" : upOrDownContinuePercent,
    }

#解析json
class Payload(object):
    def __init__(self, j):
        self.__dict__ = json.loads(j)


#获取第N页数据
def getScreenerData(url,config,page):
    _headers = {
        "User-Agent":userAgent,
        "Cookie":cookie
    }
    _params = "&".join(config);
    _params = _params + '&page=' + str(page);

    #不要太频
    # print '接口1：检索接口，休息一下'
    # time.sleep(sleep1);
    
    res = requests.get(url=url,params=_params,headers=_headers)
    
    return res.text;


#递归获取全部数据
def getAllData(page=0,stockArr=[]):

    json = getScreenerData(screenerAPI,config,page);    #这里使用第1个接口

    try:
        #正常的操作
        data = Payload(json);
    except:
        #发生异常，执行这块代码
        print '【xm】股票筛选接口崩坏！'
        print json

    if(~~hasattr(data,'list')==0):
        print('获取数据的接口似乎有点问题哦=================> 请尝试更新cookie!');
    
    arr  = data.list;

    #在函数中使用全局变量需要这里声明
    global dealNum;

    # 股票总条数
    count = data.count;
    totalPages = int(math.ceil(count/30)) 
    if page == 0:
        page = 1;
    else:
        page = page+1;
        #处理一页中，各个股票的数据
        for one in arr:

            #用来统计进度
            dealNum = dealNum + 1;
            perc = round((dealNum/count),3)*100;

            name = one['name']; 
            symbol = one['symbol']; 

            #判断股票是否存在
            cursor = dataBase.getStock(symbol);
            if cursor.count()>=1:
                for document in cursor:     
                    oneStock = document
                print(name+u' 已经存在数据库中，不再处理')
                print('--------------------------------------------------------------------------------------------------------------- '+str(perc)+'%')
                stockArr.append(oneStock);
                continue


            #非常核心的数据提炼部分1
            lows     = getLowPriceArr(symbol,6);                      #这里使用第2个接口
            #提炼低点占比
            percents = getSellPercent(lows);
            #提炼低点占比
            continueDays     = lows[2];
            continueDaysText = lows[3];
            #提炼最近一天涨跌百分比 和 连续几天的涨跌百分比
            upOrDownPercent         = lows[4];
            upOrDownContinuePercent = lows[5];

            #非常核心的数据提炼部分2
            info     = getStockInfoData(stockInfoAPI,config3,symbol); #这里使用第3个接口

            #需要再增加一个key,用来排序
            averagePrecent = percents[1];

            #完成一个完整的股票分析
            oneStock = Stock(name,symbol,lows,percents,info,averagePrecent,continueDays,continueDaysText,upOrDownPercent,upOrDownContinuePercent);

            #屏幕输出
            print(oneStock['name'])
            print(oneStock['info'])
            print(oneStock['lows'])
            print(oneStock['percents'])
            print(oneStock['continueDaysText'] + u'，合计涨/跌百分比：' + str(oneStock['upOrDownContinuePercent']) )
            print('--------------------------------------------------------------------------------------------------------------- '+str(perc)+'%')

            #保存到数据库
            dataBase.save(oneStock);
            
            #并保存到全局对象中（这个其实没啥用呢）
            #补充，现在有用了，最后的时候，用来作为全部数据导出到txt
            #为什么不是和数据库存入一样，在每一次中完成，而选择了最后一次性处理
            #因为主要是为了解决排序的问题
            stockArr.append(oneStock);
       
    if page<=totalPages:
        getAllData(page,stockArr);

    return stockArr;


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
    print arr
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



#获取 各年份卖点占比、平均卖点占比
def getSellPercent(arr):

    #低点价格数组
    lowArr   = arr[0];
    #最近一天的收盘价格
    price = arr[1];

    percentArr  = [
        round( price/(lowArr[0]*2  ),3),
        round( price/(lowArr[1]*2.4),3),
        round( price/(lowArr[2]*2.8),3),
        round( price/(lowArr[3]*3.2),3),
        round( price/(lowArr[4]*3.6),3),
        round( price/(lowArr[5]*4  ),3)
    ]
    avg = round( (percentArr[0]+percentArr[1]+percentArr[2]+percentArr[3]+percentArr[4]+percentArr[5])/6 , 3);

    #最终输出的最要数据
    return [percentArr,avg];


#获取股票的信息（市净率等）
def getStockInfoData(url,config,symbol):
    _headers = {
        "User-Agent":userAgent,
        "Cookie":cookie
    }
    _params = "&".join(config);
    _params = _params + '&code=' + symbol;

    #不要太频
    # print '接口3：详细接口，休息一下'
    # time.sleep(sleep3);

    res = requests.get(url=url,params=_params,headers=_headers)
    
    data = json.loads(res.text);
    pe_ttm = data[symbol]['pe_ttm'];
    pe_lyr = data[symbol]['pe_lyr'];
    pb = data[symbol]['pb'];
    totalShares = data[symbol]['totalShares'];
    close = data[symbol]['close'];

    #购买推荐
    buyPercent  = round ( (-2*float(pb) + 5)/3 ,3);
    buyNum      = int(round ( industryPrice*buyPercent/float(close) ,0));
    buyNum2     = int(round ( buyNum/100 ,0) * 100);


    return {
        "pe_ttm":pe_ttm,
        "pe_lyr":pe_lyr,
        "pb":pb,
        "totalShares":totalShares,
        "totalShares2":round(int(totalShares)/100000000,1),
        #新增几个
        "buyPercent":buyPercent,
        "buyNum":buyNum,
        "buyNum2":buyNum2,
        "close":close,
    };


#获取所有处理完毕的数据
stockArr = getAllData();
print(len(stockArr))
print(u'SUCCESS! 完成数据库存储');

#保存到文件
fileName = exportFile.save(stockArr);
print(u'SUCCESS! 完成txt导出');

#发送到目标邮箱
with open(fileName, 'r') as myfile:
    data=myfile.read()
    myEmail.send(data)
myfile.close();
print(u'=== END ===');


















