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

#定义累加器,这里用来统计空白行的数量，赋予初始值为0
blankLines=sc.accumulator(0)
doc=sc.textFile('file:///usr/local/test_data/spark_doc.txt')
def extractCallSigns(line):
    global blankLines
    if line=='':
        blankLines+=1
    return line.split(" ")
word=doc.flatMap(extractCallSigns)
print blankLines

#广播变量，定义为广播变量后，变量只会传递到各节点一次,并且只作为只读值
num=sc.broadcast([1,2,3])
num.value
