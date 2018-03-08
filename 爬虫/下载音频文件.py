import urllib.request
import re
import os

url='https://weixin.tesoon.com/index.php?m=listen&c=show&id=372815'
data=urllib.request.urlopen(url).read()
data=data.decode('UTF-8','ignore')
pattern='<li><a href="(.*?)" >([0-9]{2}-【广东版】2017-2018中考45套配套听力)</a></li>'
url_list=re.compile(pattern).findall(data)

#获取mp3链接
mp3_url=[]
file_name=[]
for url,mp3_name in url_list[4:]:
    this_url = 'https://weixin.tesoon.com' + url
    data=urllib.request.urlopen(this_url).read()
    data = data.decode('UTF-8', 'ignore')
    pattern1='var mp3address="(.*?)"'
    mp3_url=re.compile(pattern1).findall(data)[0]
    #mp3_url.append(re.compile(pattern1).findall(data)[0])
    #file_name.append(mp3_name)
    print("start download:"+mp3_name)
    urllib.request.urlretrieve(mp3_url,os.path.join('C:\\Users\\T\\Desktop\\广东中考45套听力',mp3_name+'.mp3'))

