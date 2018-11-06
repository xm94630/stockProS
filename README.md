# stockProSuper
stockProSuper

# python 模块（pip install）
requests  requests模块
pymongo   数据库
Flask     web服务
jinja     模板
email     邮件
smtplib   SMTP协议 （这个应该默认就有）
retrying  重复执行的装饰器 （使用 v1.0.0版本！）

# index.py 参数说明
无参数:在旧数据上追加
-n:清空旧数据 

# server.py 参数说明
无参数:默认按照pb排序
-PB:按照行业排序，再按照pb排序
-PE:按照行业排序，再按照pe（ttm）排序

# buy.py 
python buy.py [xxx.json]

# show.py
python show.py [SZ000001]

#注意
1) 不要忘记开数据库服务(20180829 又犯了错误)
2) 在盘中，运行本程序，可能会导致极少部分的不能显示出来
3) 190914 发现运行index.py的时候，会停止，也不报错。我排查之后，是接口的超时问题（各个调用requests.get都有可能出现）。以前是没有这个现象的。不过重新执行 index.py 的时候，还是可以继续的，但是没多久又出现同样的问题。所以我需要解决这个问题。方法有2：一是重新执行index.py本身，二是在接口请求的时候，一旦超时就重新请求，并log出重复的次数，方便追踪问题。
4) 注意这里的模块安装用 pip 而不是pip3
   安装组件用 pip install retrying，不行的话，加上sudo
5) pip install --upgrade pip 用这个升级失败（9.0.1->18.0）坑了好久，下面这这个可以解决：
   pip curl https://bootstrap.pypa.io/get-pip.py | sudo python
6）pip install retrying==1.0.0 （retrying版本要指定，后面的几个有问题）
7) @retry 修饰过的函数中，出了错误会被忽略，一定要记住，不要被坑了
8) 坑：我更新cookie配置的时候，不小心把它复制到 userAgent 中，导致了我后续一顿排查。当然也有些收获：
   a)首先报错是403错误，其实后端对 userAgent 是必须要的。
   b)我以为是ip被封，其实不是，电脑浏览器可以访问就说明没有。
   c)我复制请求头的时候，某字段的内容前不小心留下一个空格，也会被检测。





#行业索引（按照我常用的排序）

###
K70: 房地产业（110）福星股份

###
C36: 汽车制造业（117，汽车零件、汽车整车）长安汽车

### 金融
J66: 货币金融服务（27，银行）华夏银行
J67: 资本市场服务（31 证券）海通
J68: 保险业（4）
L71: 租赁业（2，非银金融）渤海金控
J69: 其他金融业（3，信托）

### 运输、物流
G54: 道路运输业（36，高速公路）贛澳高速
G56: 航空运输业（12，机场、航空运输）海航、国航
G53: 铁路运输业（3）大秦铁路
G55: 水上运输业（29，港口、航运）天津港、重庆港九
G59: 仓储业（9，物流）中储
G58: 装卸搬运和运输代理业（4，物流）
G60: 邮政业（1）德邦股份

### 商业贸易
F52: 零售业（82，一般零售）供销大集、鄂武商、王府井
L72: 商务服务业（30，旅游，商业经营）中青旅、轻纺城
F51: 批发业（共62，贸易、医药商业、零售、多元金融） 广东明珠、厦门国贸、浙江东方
### 食品饮料
C15: 酒、饮料和精制茶制造业（39，饮料，包括酒）茅台、青岛啤酒
C14: 食品制造业（39，食品加工）皇氏集团、梅花生物（味精）、榨菜
C13: 农副食品加工业（47，饲料，食品加工，农产品加工）唐人神
### 纺织服饰
C17: 纺织业（40，纺织制造）黑牡丹
C18: 纺织服装、服饰业（35，服装） 七匹狼、森马、九牧王
C19: 皮革、毛皮、羽毛及其制品和制鞋业（11 服装）天创时尚、红蜻蜓
### 家用轻工
C21: 家具制造业（22，家用轻工）宜华生活、喜临门、欧派家具
C22: 造纸和纸制品业（28）华泰股份
C24: 文教、工美、体育和娱乐用品制造业（13，家用轻工）晨光文具、扑克
C41: 其他制造业（18，珠宝、家用轻工）金洲慈航、老凤祥

### 建筑、工程
E48: 土木工程建筑业（53 基础建设）浦东建设
E50: 建筑装饰和其他建筑业（23，装修装饰）瑞和股份（建筑节能）、江河集团
C30: 非金属矿物制品业（80，建材、水泥）
M74: 专业技术服务业（39，基础建设、工程）设计总院、建研院

### 计算机、互联网
I64: 互联网和相关服务（21，互联网传媒）人民网、新华网
I65: 软件和信息技术服务业（164，计算机设备、计算机应用） 同方
C39: 计算机、通信和其他电子设备制造业（313，电子、计算机设备、视听）中科曙光、同方、海信
### 传媒
R85: 新闻和出版业（21，文化传媒）时代出版
I63: 电信、广播电视和卫星传输服务（14，文化传媒、通讯设备）歌华有限、中国联通、东方明珠、宜通世纪
R86: 广播、电视、电影和影视录音制作业（16，文化传媒）湖北广电、光线传媒

### 钢铁、煤炭
C31: 黑色金属冶炼和压延加工业（32，钢铁）河钢、首钢
B06: 煤炭开采和洗选业（24，煤炭开采）上海能源、中国神华、兰花科创
C32: 有色金属冶炼和压延加工业（62，工业金属：铝、铜、铅、钨、合金）利源精制、南山铝业
B09: 有色金属矿采选业（15，矿业、黄金）
B11: 开采辅助活动（8，采掘）
B08: 黑色金属矿采选业（3，矿业）
B10: 非金属矿采选业（1）
### 石油、化工
B07: 石油和天然气开采业（2，石油化工）中国石化
C25: 石油加工、炼焦和核燃料加工业（16，石油化工）沈阳化工
C28: 化学纤维制造业（21，化学纤维）华西股份
C26: 化学原料和化学制品制造业（218，化学制品）辉丰股份、鲁西化工、新疆天业、史丹利
### 熟料橡胶
C29: 橡胶和塑料制品业（74，塑料橡胶）三角轮胎

### 电力水力、环境
D44: 电力、热力生产和供应业（62，公共事业、电力） 韶能、湖北能源
D45: 燃气生产和供应业（11，燃气）
D46: 水的生产和供应业（14，水务）武汉控股、中山公用、瀚蓝环境、兴蓉环境
N77: 生态保护和环境治理业（18，环保）清新环境、碧水源

### 各种设备，主要关注家电
C38: 电气机械和器材制造业（213，白色家电、高低压设备、电气设备）平高电气、许继电气；格力、特变
C34: 通用设备制造业（123，通用设备）华意压缩、广日股份
C33: 金属制品业（55，电子、高压设备、通用机械）这个类别中比较杂
C37: 铁路、船舶、航空航天和其他运输设备制造业（38，船舶制造、海控设备）中国重工、航天科技、海特高新
C35: 专用设备制造业（38，医疗机械）天地科技、欧普康视
C40: 仪器仪表制造业（44，机械设备、电气设备）林洋能源（电气）、远方信息、先锋电子

###
C27: 医药制造业（194，医药生物）振东制药
M73: 研究和试验发展（4，医疗服务）药明康德
Q83: 卫生（1，医疗服务）爱尔眼科

### 不关注
N78: 公共设施管理业（16，旅游）桂林旅游 
A01: 农业（14，种植）北大荒
S90: 综合（13 物流）分类很杂，不关注  宁波联合、广汇物流
C23: 印刷和记录媒介复制业（12，包装印刷）
A03: 畜牧业（12，养殖）圣农发展、新五丰
A04: 渔业（8）开创国际、东方海洋
C20: 木材加工和木、竹、藤、棕、草制品业（7，建材）兔宝宝
H61: 住宿业（6，酒店）
R87: 文化艺术业（4）
A02: 林业（4）
H62: 餐饮业（3）全聚德
C42: 废弃资源综合利用业（1）
E47: 房屋建筑业（1，基础建设）重庆建工、上海建工
O80: 机动车、电子产品和日用产品修理业（1）
P82: 教育（1）东方时尚
E49: 建筑安装业（1）
A05: 农、林、牧、渔服务业（1）
R88: 体育（1）
M75: 科技推广和应用服务业（0）
G57: 管道运输业（0）


找不到对应上面的分类：
五矿资本 pb 0.89
厦门象屿 pb 0.98 (交通运输、物流)
东湖高新 pb 1.11（建筑装饰）

电气：是电能的生产传输等



#行业配置表

这个同上面的顺序基本保持一致，行业和对应id如下：

1 房地产 福星股份           ---------------> 福星股份
2 汽车                    ---------------> 长安汽车
3 银行                    ---------------> 华夏银行
4 证券、多元金融、保险       ---------------> 海通证券
5 交通                    ---------------> 赣粤高速、海航控股
6 贸易、零售               ---------------> 供销大集
7 饲料、食品               ---------------> 
8 家用轻工（造纸、家具...）  ---------------> 华泰股份、宜华生活、金洲慈航
9 纺织                    ---------------> 新野纺织
10 服装                   ---------------> 七匹狼
11 建筑、建筑材料（玻璃、水泥...）      -----> 浦东建设
12 计算机                 ---------------> 
13 传媒                  ---------------> 天神娱乐
14 钢铁                  ---------------> 河钢股份
15 金属、非金属           ---------------> 利源精制
16 煤炭                  ---------------> 冀中能源
17 石油、化工             ---------------> 华锦股份、中泰股份
18 电力                  ---------------> 申能股份
19 水务、环境             ---------------> 武汉控股
20 燃气                  ---------------> 金鸿控股
21 家用电器               ---------------> （海信电器）
22 各种设备（机械设备、专用设备、通信设备） --> 
23 电气设备 (电源、电气)   ---------------> 特变电工
24 电子                  ---------------> 
25 医药                  ---------------> 振东医药
26 综合                  ---------------> 宁波联合
27 旅游                  ---------------> 





### ================================== 选股新法 =======================================
【选股新法】
之前的方法都是关注，最低pb、pe，除此之外我也尝试：
注意下述2种方法，还需要的前提是：当天大市最好是大跌状态，而个股当天必须是下跌的，幅度越大越好（或者个股只是小跌，但是近天内的跌幅也到达到了10%，又或者当前价是历史最低位）。之前几天没有大涨的情况，价格若处于支撑位附近更好。
【1】高股息率、高roe、相对较低（或行业中等水平）的pb、pe
【2】高roe，较好股息率、历史图形上看处于低谷（或者相对较低的位置），保证在pb2之内即可：
### 注意
房地产（钢铁）相对于其他行业，roe都比较高，所以股息率的作用可以看的大些。当然还是要满足pbpe最优这些基础上。


