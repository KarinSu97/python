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

#创建键值对
data=['hello lin',"hello lucy","hello ben"]
distdata=sc.parallelize(data)
word=distdata.flatMap(lambda x:x.split(" "))
wordPair=word.map(lambda x:(x,1))
wordPair.collect()

'''
键值对转化操作
'''
#reduceByKey,合并具有相同键的值
reduceByKey_result=wordPair.reduceByKey(lambda x,y:x+y)
reduceByKey_result.collect()

#groupByKey,对具有相同键的值进行分组
reduceByKey_result1=reduceByKey_result.map(lambda x:(x[1],x[0]))
groupByKey_result=reduceByKey_result1.groupByKey()
groupByKey_result.collect()

#mapValues,对每个键值对的值进行操作
mapVaules_result=reduceByKey_result.mapValues(lambda x:x+1)
mapVaules_result.collect()

#flatMapValues,对每个键值对的值进行操作，返回多个元素
pairRDD=sc.parallelize([(1,2),(3,4),(4,5)])
flatMapValues_result=pairRDD.flatMapValues(lambda x:range(x,6))
flatMapValues_result.collect()

#keys,返回只含有键的RDD
keys_result=pairRDD.keys()
keys_result.collect()

#values,返回只含有值的RDD
values_result=pairRDD.values()
values_result.collect()

#sortByKey,根据键排序
sortByKey_result=reduceByKey_result.sortByKey()
sortByKey_result.collect()

#subtractByKey,根据键求差集
pairRDD1=sc.parallelize([(1,2),(2,3),(4,5)])
pairRDD2=sc.parallelize([(2,3),(4,5),(5,6)])
subtractByKey_result=pairRDD1.subtractByKey(pairRDD2)
subtractByKey_result.collect()

#join，内连接,类似的还有rightOuterJoin,leftOuterJoin
join_result=pairRDD1.join(pairRDD2)
join_result.collect()

#cogroup,对两个pairRDD中有相同键的对进行分组
cogroup_result=pairRDD1.cogroup(pairRDD2)
cogroup_result.collect()

'''
行动操作
'''
#countByKey,按照键进行计数
data=['hello lin',"hello lucy","hello ben"]
distdata=sc.parallelize(data)
word=distdata.flatMap(lambda x:x.split(" "))
wordRDD=word.map(lambda x:(x,1))
countByKey_result=wordRDD.countByKey()
countByKey_result

#lookup,查看指定键对应的值
wordRDD.lookup('lin')
