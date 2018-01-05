import datetime

#显示当前日期
print(datetime.date.today())
print(datetime.datetime.now())

#转化为日期格式
print(datetime.date(2016,1,1))
print(datetime.time(12,00))

#计算时间差
today=datetime.date.today()
tomorrow=today-datetime.timedelta(days=1)
print(tomorrow)

import time
#显示当前日期
time.time()   #距离1970年1月1日的时间，单位为妙
t=time.localtime(time.time())
t.tm_year   #年
t.tm_mon   #月
t.tm_mday   #日
t.tm_hour  #小时
t.tm_min   #分钟
t.tm_sec   #秒
t.tm_wday  #星期
t.tm_yday  #一年的第几天

#解析日期
from dateutil.parser import parse
parse('2017-12-26')
parse('6/12/2017',dayfirst=True)

#生成时间序列
import pandas as pd
pd.date_range(start='2017-10-1',periods=20)   #从2017-10-1日开始产生20天的时间序列
pd.date_range(end='2017-10-1',periods=20)
pd.date_range('2017-1-1','2018-1-1',freq='BM')   #产生2017年每个月的最后一个工作日
pd.date_range('2017-1-1',periods=10,freq='1h30min')
pd.date_range('2017-12-25 17:00:59',periods=5,normalize=True)   #normalize=True会自动将时间调整为00:00:00

#时间位移
import numpy as np
import pandas as pd
ts=pd.Series(np.random.randn(10),pd.date_range('2017-1-1',periods=10))
ts.shift(1)   #数据往前移一位
ts.shift(-1)   #数据往后移一位
ts.shift(1,freq='M')   #往后挪一个月
ts/ts.shift(1)-1   #计算环比

#时间加减
from pandas.tseries.offsets import Hour,Minute,Day,MonthEnd
from datetime import datetime
datetime(2017,1,1,10,0,0)+Hour(1)
datetime(2017,1,1)+3*Day()