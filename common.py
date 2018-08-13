#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#上面的注释是用来支持中文，没有就会出错

import json
import sys

# 保存json数据
def storeJsonFile(fileAddress,data):
    with open(fileAddress, 'w') as json_file:
        json_file.write(json.dumps(data))

# 读取json数据
def loadJsonFile(fileAddress):
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


