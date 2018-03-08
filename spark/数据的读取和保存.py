# coding: utf-8
import os
import sys
import pyspark
from pyspark import SparkContext,SparkConf

#指定spark_home和pysparkhome
os.environ['SPARK_HOME'] = "/usr/local/spark-1.5.1-bin-hadoop2.4"
sys.path.append("/usr/local/spark-1.5.1-bin-hadoop2.4/python")

#初始化spark,appName参数是在集群UI上显示的你的应用的名称。master是一个Spark、Mesos或YARN集群的URL,
# 如果你在本地运行那么这个参数应该是特殊的”local”字符串
conf=SparkConf().setAppName('test').setMaster('local')
sc=SparkContext(conf=conf)

#读取文本文件
input=sc.textFile('file:///usr/local/test.txt')
input.collect()

#读取一个目录下的所有文本文件，此时，文件名作为key
input=sc.wholeTextFiles('file:///usr/local/test_data')
input.collect()

#保存为文本文件,保存为一个文件夹
data=["hello world","hello"]
distdata=sc.parallelize(data)
distdata.saveAsTextFile('file:///usr/local/test_data/test3')

#读取json文件
import json
from json import loads
import pandas as pd
input=sc.wholeTextFiles('file:///usr/local/test_data/json')
data=input.values().first()
data=loads(data)
data=pd.DataFrame(data[u'data'])

#保存为json文件
input=sc.wholeTextFiles('file:///usr/local/test_data/json')
data=input.values()
data=data.map(lambda x:loads(x))
data=data.map(lambda x:json.dumps(x)).saveAsTextFile('file:///usr/local/test_data/test4')

#读取csv文件
import csv
import StringIO
data=sc.textFile('file:///usr/local/test_data/score.csv')
def LoadRecord(line):
    input=StringIO.StringIO(line)
    reader=csv.DictReader(input,fieldnames=['name','score'])
    return reader.next()
result=data.map(LoadRecord)

#读取hdfs文件系统
distfile=sc.textFile('hdfs://192.168.0.104:9000/test.txt')

#使用sparkSQL读取hive数据
from pyspark.sql import HiveContext
hiveCtx=HiveContext(sc)
rows=hiveCtx.sql('select name,score from testdb.score')
first_row=rows.first()
print first_row.name

#使用sparkSQL读取json文件
rows=hiveCtx.jsonFile('file:///usr/local/test_data/json')
rows.registerTempTable('rows')
result=hiveCtx.sql("select * from rows")
result.first()