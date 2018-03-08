import urllib.request
import re
import pandas as pd
import numpy as np

#添加表头
headers=("User-Agent","Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36")
opener=urllib.request.build_opener()
opener.addheaders=[headers]
urllib.request.install_opener(opener)   #将opener设置为全局变量，这样urllib.request下面的函数也可以使用

#获取平台名单、好评率
plat_url='http://www.p2peye.com/platform/all/p1/'
page=opener.open(plat_url).read()
page=page.decode('gbk','ignore')
pattern=['<a href="(.*?)" class="ui-result-pname" title="(.*?)" target="_blank">',
         '<p class="ui-result-text">用户评价 ：(.*?)<span class="ui-color-blue">(.*?)%</span>好评度， <span class="ui-color-blue">(.*?)</span>人点评</p>']
a=re.compile(pattern[0]).findall(page)
b=re.compile(pattern[1],re.S).findall(page)
data=np.concatenate((a,b),axis=1)

for i in range(2,210):
    plat_url='http://www.p2peye.com/platform/all/p%s/' % i
    page=opener.open(plat_url).read()
    page=page.decode('gbk','ignore')
    pattern=['<a href="(.*?)" class="ui-result-pname" title="(.*?)" target="_blank">',
             '<p class="ui-result-text">用户评价 ：(.*?)<span class="ui-color-blue">(.*?)%</span>好评度， <span class="ui-color-blue">(.*?)</span>人点评</p>']
    a=re.compile(pattern[0]).findall(page)
    b=re.compile(pattern[1],re.S).findall(page)
    c=np.concatenate((a,b),axis=1)
    data=np.concatenate((data,c),axis=0)
    print('finish'+str(i))

data1=pd.DataFrame(data,columns=['链接','平台名称','网友评价','好评率','点评人数'])
data1.to_csv(r'C:\Users\T\Desktop\研究生毕业论文\数据\网贷天眼\所有平台名单.csv',index=False)