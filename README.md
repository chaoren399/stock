# stock
zzy 交易系统

只看 看涨做涨

command + d   复制一行

-------------

d9,110031,易方达恒生国企ETF联结A,1.16,,,重点-别墅- 近3年定投收益5%(不能定投了),,3年4星，5年3星,15亿,2012
e6,160212,国泰估值优势股票,,,,失败-近3年的定投收益率-14%(不能定投了),,3年2星，5年4星,24亿,2010

d8,270048,广发纯债债券A,1.2,,, 近3年定投收益 4%,,3年3星， 5年5星,5亿,2012


兴全趋势投资混合(LOF) (媳妇蛋卷定投 100 2019年05月27日)


———mac

1 . workon evn3-stock  (更改了工作虚拟空间)
2 .  cd /Users/zzy/PycharmProjects/python-workspace/stock
3 .  python manage.py runserver 8087

服务器 独立 IP 启动为  :python   manage.py runserver 0.0.0.0:8000
每次保存完 csv 格式,必须用 notpad++ 转换成 utf-8的编码
/fundold/  显示基金所有的趋势图  如果不显示, 说明 是 数据有错误, 请查看 data /先每个文件是否对


添加新基金的时候, 先 在基金池里 添加, 然后 get_fund_old_data  下载 2016-2019 的历史数据.
然后在运行界面上的 下载所有数据, 跟新 2019 到最新的数据,就可以了.(也可以单独下载 最新的数据 get_fund_old_data/get_urls())

2021年07月07日  迁移到服务器

pycharm 同步:pycharm 远程部署 Django 详细步骤    http://www.huamaodashu.com/5778.html

服务器 独立 IP 启动为  :python   manage.py runserver 0.0.0.0:8000
用的 宝塔面板中的 Python 项目管理,  uswgi 启动方式 ,非常好用.
宝塔面板用python 项目管理器 部署Django 程序 : http://www.huamaodashu.com/5796.html





2019年4月4日




1.
https://blog.csdn.net/github_26672553/article/details/78662563

http://fund.eastmoney.com/f10/F10DataApi.aspx?type=lsjz&code=000001&page=1&per=1

http://data.funds.hexun.com/outxml/detail/openfundnetvalue.aspx?fundcode=519688&startdate=2016-11-21&enddate=2018-12-08


天天基金网数据接口
https://blog.csdn.net/weizhixiang/article/details/51445054


'http://fundgz.1234567.com.cn/js/001186.js'
返回数据格式
jsonpgz (
{
"fundcode": "519983",
"name": "富国文体健康股票",
"jzrq": "2019-04-03",(净值日期-取这个,数据延迟因为要晚一天)
"dwjz": "1.4550", (单位净值--取这个 任何基金最初的净值都是1元. 每天晚上8点30 更新当日净值)
"gsz": "1.4662", (净值估算)
"gszzl": "0.77",(估算涨幅)
"gztime": "2019-04-04 15:00" (估算日期)
}
)


1. 定投投资收益计算器

http://99fund.com/main/planning/jjgjx/dttz/index.shtml

2. 晨星 排名
http://cn.morningstar.com/quicktake/F000000416?place=qq



3. 基金历史数据

http://data.funds.hexun.com/outxml/detail/openfundnetvalue.aspx?fundcode=519688&startdate=2018-11-21&enddate=2019-07-08


使用的是 百度的 echars echarts.min.js
就用了一个简单的 ui . 数据是从 views 传过去的
get_fund_old_data.py 是负责把历史数据 下载下来的. 不知道为什么到 2019年07月15日 只能更新 7 月 04 号的数据.
这个数据需要重新搞一份.
4.  python 相对路径

https://www.cnblogs.com/chaoren399/p/11224934.html

5. 前台后台 交互:

https://www.cnblogs.com/chaoren399/p/11156175.html

ajax  实时更新后台数据

https://www.cnblogs.com/xibuhaohao/p/10192052.html
6. python 学习目录
file:///Volumes/apple-sd/doc-apple-sd/doc/python-课件和资料/zzy_all_index.html


7. echarts标题（title）配置
https://blog.csdn.net/zhang__ao/article/details/80745873

https://www.echartsjs.com/examples/zh/index.html


------------------

2021年06月27日   基金定投策略 回测程序

定投策略: 每周定投, 收益率为负 , 加码定投 累计金额的 1/5 (资金量小,如果多可以设置为 1/3)
收益率为正 15% 或者 大于 1000 的时候止盈 (主要是测试方法)


回测 1-3 年的数据,以沪深 300 和上证 50 位主

涉及的参数:

T  周期 : 周定投 week ,月定投 : month


收益率 : 没定投一次计算一下 收益率  onerate =  总市值 / 总投入 = (基金份额 X 基金净值) / 总投入

总市值:  marketvalue

忽略手续费







































































































