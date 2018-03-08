# coding: utf-8
import os
import sys
import pyspark
from pyspark import SparkContext,SparkConf
from pyspark.sql import HiveContext,Row
from pyspark.sql import types

#指定spark_home和pysparkhome
os.environ['SPARK_HOME'] = "/usr/local/spark-1.5.1-bin-hadoop2.4"
sys.path.append("/usr/local/spark-1.5.1-bin-hadoop2.4/python")

#初始化spark,appName参数是在集群UI上显示的你的应用的名称。master是一个Spark、Mesos或YARN集群的URL,
# 如果你在本地运行那么这个参数应该是特殊的”local”字符串
conf=SparkConf().setAppName('test').setMaster('local')
sc=SparkContext(conf=conf)

#创建SQL上下文环境
hiveCtx=HiveContext(sc)

#使用sparkSQL读取json文件
rows=hiveCtx.jsonFile('file:///usr/local/test_data/json')
rows.registerTempTable('rows')
result=hiveCtx.sql("select * from rows")
result.first()
result_data=result.map(lambda x:x.data)   #获取data字段
result_data.collect()
result.printSchema()   #输出结构信息

#数据缓存
hiveCtx.cacheTable('rows')

#读取hive数据库的数据
score_data=hiveCtx.sql('select name,score from testdb.score')
score=score_data.map(lambda x:x[1])
score.collect()

#读取parquet文件
parquet_data=hiveCtx.parquetFile('hdfs://192.168.0.104:9000/users')
parquet_data.first()
gender=parquet_data.map(lambda x:x.gender)
gender.collect()
parquet_data.registerTempTable('users')
male_data=hiveCtx.sql("select * from users where gender='male'")
male_data.collect()

#将RDD转化为SchemaRDD
happyPeopleRDD=sc.parallelize([Row(name='lin',age=25)])
happyPeopleSchemaRDD=hiveCtx.inferSchema(happyPeopleRDD)
happyPeopleSchemaRDD.registerTempTable('happyPeople')
result=hiveCtx.sql('select name from happyPeople')
result.collect()

#用户自定义函数
hiveCtx.registerFunction('strLen',lambda x:len(x),types.IntegerType())
name_len=hiveCtx.sql('select strLen(name) from users')
name_len.collect()
