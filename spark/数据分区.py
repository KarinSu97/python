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

#对数据进行分区,这样在后续进行join或其他操作时，可以免去洗牌操作，从而减少网络传输，提高速度
data=[(1,1),(2,2),(3,4),(9,10)]
pairRDD1=sc.parallelize(data).partitionBy(2).persist()

#对分区进行合并
pairRDD1=pairRDD1.coalesce(5)