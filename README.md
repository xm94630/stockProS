# stockProSuper
stockProSuper

# python 模块
requests requests模块
pymongo 数据库
Flask   web服务
jinja   模板
email   邮件
smtplib SMTP协议 （这个应该默认就有）

# index.py 参数说明
无参数:在旧数据上追加
-n:清空旧数据 

# server.py 参数说明
无参数:默认数据以低点平均百分比增序(现在已经改成按照pb排序)
-s:数据以最近一年低点平均百分比增序

# buy.py 
python buy.py [xxx.json]

# show.py
python show.py [SZ000001]

#注意
不要忘记开数据库服务
