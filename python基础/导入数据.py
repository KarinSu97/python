import pandas as pd

#导入csv数据
file_path='C:/Users/T/Desktop/知识付费爬虫/知乎live/live/知乎live数据.csv'
df=pd.read_csv(file_path,encoding='utf-8')

#对于不规整的数据，可以采用以下方式读取
import csv
f=open(file_path)
data=csv.reader(f)

#导入excel数据
file_path='C:/Users/T/Desktop/知识付费爬虫/知乎live/书店/一小时数据.xlsx'
df=pd.read_excel(file_path,sheetname='Sheet1')

#导入mysql数据
import pymysql
conn=pymysql.connect(host='localhost',user='root',passwd='123456',db='spiders',charset='utf8mb4')
sql='select * from jingdong'
df=pd.read_sql(sql,conn)

#导入html数据，读取网页中的表格数据
url='http://shuju.wdzj.com/'
df=pd.read_html(url,encoding='UTF-8')

#导入txt数据
file_path='C:/Users/T/Desktop/研究生毕业论文/数据/方案一/colnames.txt'
df=pd.read_table(file_path,encoding='gbk',sep=',')

#json数据
import json
data='''
{"a":[1,2,3],"b":[4,5,6]}
'''
##将字符串转化为json数据格式
a=json.loads(data)
##将数据重新转化为字符串格式
json.dumps(a)
