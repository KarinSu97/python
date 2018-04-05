import urllib.request
import re
import json
from bypy import ByPy
import os
import pandas as pd
import jieba
import jieba.analyse

def get_sina_news(page):
    data=pd.DataFrame()
    #搜索链接
    url1 = 'http://search.sina.com.cn/?c=news&from=chanel2&q=%C4%A6%B0%DD&col=&range=&source=&country=&size=&time=&a=&page={0}&pf=2131425450&ps=2134309112&dpc=1'.format(page)
    #封装表头
    headers1={
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0",
        }
    #获取新闻列表
    req1=urllib.request.Request(url1,None,headers1)
    data1=urllib.request.urlopen(req1).read()
    data1=data1.decode('gb2312','ignore')
    pattern1='<h2><a href="(.*?)" target="_blank">(.*?)</a> <span class="fgray_time">.* (.*? .*?)</span></h2>'
    news_list=re.compile(pattern1).findall(data1)
    #print(news_list)
    #获取每条新闻的关键词
    for url,title,date in news_list:
        try:
            data3=urllib.request.urlopen(url).read()
            data3=data3.decode('utf-8','ignore')
            pattern2='<!-- 原?始?正文 ?start -->(.*?)<!-- 原?始?正文 ?end -->'
            ariticle=re.compile(pattern2,re.S).findall(data3)
            if len(ariticle)>0:
                ariticle=re.sub('<.*?>|\\t|\\n','',ariticle[0])
            else:
                pattern2='<!-- edu_web_article_uptg -->(.*?)<!-- edu_web_article_xgtg -->'
                ariticle = re.compile(pattern2, re.S).findall(data3)
                if len(ariticle)==0:
                    #print(url)
                    continue
            key_word1=jieba.analyse.extract_tags(ariticle,5)
            pattern3='<meta name="keywords" content="(.*?)" />'
            key_word2=re.compile(pattern3).findall(data3)
            if len(key_word2)>0:
                key_word2=key_word2[0].split(',')
            else:
                key_word2=[]
            key_word1.extend(key_word2)
            key_word1=list(set(key_word1))
            data2=pd.DataFrame({'url':url,"title":re.sub('<span style="color:#C03">|</span>','',title),'date':date,"keyword":','.join(key_word1)},index=[0])
            data=data.append(data2,ignore_index=True)
        except:
            continue
    return data

data_all=pd.DataFrame()
for page in range(1,650):
    data = get_sina_news(page=page)
    data_all=data_all.append(data,ignore_index=True)
    print('获取第%d页结束...' % page)
    print(data_all.shape)

data_all.to_csv('C:\\Users\\T\\Desktop\\xina_news1.csv')

# for i in range(len(data_all['keyword'])):
#     word=data_all['keyword'][i].split(',')
#     word=[x for x in word if not (len(re.match('[0-9a-zA-z]',x).group())>0 and x!='ofo' or x!='Ofo' or x!='OFO')]
#     word=list(set(word))
#     data_all['keyword'][i]=','.join(word)
#     print(i)
