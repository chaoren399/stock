#encoding=utf-8
from django.db import models

# Create your models here.

class StockInfo(models.Model):
    #code,name,lowprice,upprice,order,tar_value,now_price,jiazhilv,date
    code = models.CharField(max_length=20)

    name = models.CharField(max_length=50)
    lowprice= models.CharField(max_length=50)
    upprice= models.CharField(max_length=50)
    order = models.CharField(max_length=20)
    tar_value = models.CharField(max_length=20, default='0') # 低于的目标值
    now_price = models.CharField(max_length=20, default='0') #现价
    jiazhilv = models.CharField(max_length=20, default='0')  #价值率
    date = models.CharField(max_length=20, default='0')  # 抓取 日期







    #
    def showName(self):
        return self.name

    # class Meta:
    #     db_table='stockinfo'

    def __str__(self):
        return self.name.encode('utf-8')


class FundInfo(models.Model):
    order=models.CharField(max_length=20)
    code=models.CharField(max_length=20)
    name=models.CharField(max_length=200)
    tar_value=models.CharField(max_length=20) #目标基金值
    net_value=models.CharField(max_length=20) #最新净值
    jzrq=models.CharField(max_length=40) #净值日期

    zhongdian = models.CharField(max_length=20, default='0')  # 重点关注的基金
    url = models.CharField(max_length=200, default='0')  # 天天基金URL

    jiazhilv = models.CharField(max_length=20, default='0')  # 价值率
    pingji = models.CharField(max_length=20, default='0')  # 星辰评级

 #
    def showName(self):
        return self.name


    # def __str__(self):
    #     return self.name.encode('utf-8')