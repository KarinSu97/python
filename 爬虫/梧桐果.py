import sys
sys.path.insert(0,'C:\\Users\\T\\Desktop\\youtu')
import TencentYoutuyun
import urllib.request
import re
import pandas as pd
import datetime
import numpy as np
import itchat

def xuanjianghui(datetype=1):
    #当天日期
    now=datetime.datetime.now()
    date='-'.join([np.str(now.year),np.str(now.month),np.str(now.day)])

    #爬取当日宣讲会信息
    url='http://www.wutongguo.com/xuanjianghui/r4001/?datetype=%d' % datetype
    data=urllib.request.urlopen(url).read()
    data=data.decode('gb2312','ignore')

    #获取公司名称
    pattern1='<a class="rmTitle".*>(.*?)</a>'
    company=re.compile(pattern1).findall(data)

    #获取宣讲学校
    pattern2=' <a target="_blank".*>(.*?)</a>'
    university=re.compile(pattern2).findall(data)

    #获取宣讲地点
    pattern3='<b style="font-weight:normal;" title="(.*?)">'
    address=re.compile(pattern3,re.S).findall(data)

    #获取举办时间
    pattern4='<span style="font-family:微软雅黑;font-size:14px; ">\r\n\t\t  \\((.*?)\\) <img src="(.*?)"  style='
    hold_time=re.compile(pattern4,re.S).findall(data)
    weeks=[]
    time_urls=[]
    for week,time_url in hold_time:
        weeks.append(week)
        time_urls.append(time_url)

    #使用腾讯优图识别时间
    appid = '10119599'
    secret_id = 'AKIDyWAh7LTHzWr0xp99WWQ9g2GJTehaql9L'
    secret_key = '84oz1rX1Jk386tofKn3GLEKSQIyRhr39'
    end_point = TencentYoutuyun.conf.API_YOUTU_END_POINT
    youtu = TencentYoutuyun.YouTu(appid, secret_id, secret_key, end_point)
    hold_time=[]
    for i in time_urls:
        time=youtu.generalocr(i,1)
        hold_time.append(''.join([i['character'] for i in time['items'][0]['words']]))

    #汇总数据
    data_all=pd.DataFrame()
    data_all['公司名称']=company
    data_all['日期']=np.repeat(date,len(company))
    data_all['时间']=hold_time
    data_all['学校']=university
    data_all['地点']=address
    return data_all

xuanjianghui()
