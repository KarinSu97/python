import urllib.request
import re
import json
from bypy import ByPy
import os

#视频链接，直接在优酷上对应电影的链接，这里以《神秘巨星》为例，电视剧也可以看，不过需要将链接中后缀"s=..."去掉，比如
#http://v.youku.com/v_show/id_XMzQwMjgyNjM4NA==.html?spm=a2h0j.11185381.listitem_page1.5!3~A&s=efbfbdefbfbdefbfbd1d需要
#变为http://v.youku.com/v_show/id_XMzQwMjgyNjM4NA==.html?spm=a2h0j.11185381.listitem_page1.5!3~A
source_url='http://v.youku.com/v_show/id_XMzQyMTYwMDgwOA==.html?spm=a2hmv.20009921.posterMovieGrid86981.5~5~5~1~3!2~A'

#定义获取视频函数
def get_video(source_url,filename=None):
    #解析网址，这里借用www.dianyingvip的解析网站
    parse_url = 'https://qqapi000o.duapp.com/2018/222.php?url='

    #封装表头
    headers1={
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0",
        #"Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        #"Accept-Language":"zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
        #"Accept-Encoding":"gzip, deflate, br"
        }
    req=urllib.request.Request(parse_url+source_url,None,headers1)
    data=urllib.request.urlopen(req).read()
    data=data.decode('utf-8','ignore')

    #获取key、type、url、time、referer、ckey1信息
    time=re.compile('"time":"(.*?)"').findall(data)
    key=re.compile('"key": "(.*?)"').findall(data)
    type=re.compile('"type": "(.*?)"').findall(data)
    ckey1=re.compile('"ckey1": (.*?)}').findall(data)
    referer="http://000o.cc/jx/ty.php?url="+source_url
    url=source_url

    #模拟post请求
    headers2={
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0",
        #"Accept": "application/json, text/javascript, */*; q=0.01",
        #"Accept-Language":"zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
        #"Accept-Encoding":"gzip, deflate, br",
        "Content-Type":"application/x-www-form-urlencoded; charset=UTF-8",
        "Referer": "https://qqapi000o.duapp.com/2018/222.php?url="+source_url
    }
    post_url = 'https://qqapi000o.duapp.com/2018/api.php'
    values = {'referer': referer, 'time': time[0], 'key':key[0],'url': url,'type':type[0],'ckey1':ckey1[0]}
    mydata = urllib.parse.urlencode(values).encode('utf-8')

    req = urllib.request.Request(post_url,mydata,headers2)
    response = urllib.request.urlopen(req).read()
    response=response.decode('utf-8','ignore')
    result_url=json.loads(response)['url']

    #显示电影链接，可以直接点击该链接在线观看
    print(result_url)

    #也可以自己下载到本地
    if filename is not None:
        urllib.request.urlretrieve(result_url,filename)

#查看电影链接
get_video(source_url)

def upload_video(dianshiju_url,remote_name='烈火如歌',init_index=9):
    #获取所有集的链接
    data=urllib.request.urlopen(dianshiju_url).read()
    data=data.decode('utf-8','ignore')
    pattern1='a class="sn" href="(.*?)s=[a-zA-Z0-9]*" data-from'
    all_url=re.compile(pattern1).findall(data)
    # 创建文件夹
    bp = ByPy()
    #bp.mkdir(remotepath='视频/%s' % remote_name)
    #下载所有剧集
    for i in range(init_index,len(all_url)):
        print("下载第%d集..." % (i+1))
        source_url='http:%sspm=a2h0j.11185381.listitem_page1.5!%d~A' % (all_url[i],i+1)
        if(not os.path.exists('C:\\Users\\T\\Downloads\\%s' % remote_name)):
            os.mkdir('C:\\Users\\T\\Downloads\\%s' % remote_name)
        filename='C:\\Users\\T\\Downloads\\%s\\%d.mp4' % (remote_name,i+1)
        get_video(source_url,filename=filename)
        bp.upload(localpath='C:\\Users\\T\\Downloads\\%s\\%d.mp4' % (remote_name,i+1),remotepath='/视频/%s' % remote_name,ondup='newcopy')
        print('上传第%d集完毕' % (i+1))

upload_video('http://v.youku.com/v_show/id_XMzQwNjg1MDc2MA==.html?spm=a2h0j.11185381.listitem_page1.5!11~A&s=efbfbdefbfbdefbfbd1d',
             remote_name='烈火如歌',init_index=15)



