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

#创建RDD，可以是并行化当前程序中的一个集合，或者是从外部存储系统中引用一个数据集
#并行化集合
data=[1,2,3,4,5]
distdata=sc.parallelize(data)
#外部数据集
distfile=sc.textFile('hdfs://192.168.0.104:9000/test.txt')

'''
转化操作：转化操作后返回的还是一个RDD，常见的转化操作有map、filter等
'''
#map操作，对RDD中每个元素执行操作,collect是将RDD转为内存中的数据，如果数据量大的话一般不建议操作
map_result=distdata.map(lambda x:x**2).collect()
for line in map_result:
    print line

#filter操作，即过滤操作
filter_result=distfile.filter(lambda s:int(s)>=3)
filter_result.first()

#flatMap操作，将RDD中每个元素返回为多个元素
distdata=sc.parallelize(['hello world','hello'])
flatmap_result=distdata.flatMap(lambda x:x.split(" ")).collect()
for line in flatmap_result:
    print line

#去重操作,会对数据进行shuffle操作，开支较大
distdata=sc.parallelize([1,1,3,2])
distinct_result=distdata.distinct().collect()
for i in distinct_result:
    print i

#并集操作，合并后不会剔除重复项，而且合并时数据类型必须一致
distdata1=sc.parallelize([1,2,3,3])
distdata2=sc.parallelize([4,5,3,3])
union_result=distdata1.union(distdata2)
union_result.collect()

#交集操作
intersection_result=distdata1.intersection(distdata2)
intersection_result.collect()

#差集操作
subtract_result=distdata1.subtract(distdata2)
subtract_result.collect()

#笛卡儿积,即计算所有可能组合
cartesian_result=distdata1.cartesian(distdata2)
cartesian_result.collect()

#抽样,False表示不重复抽样
distdata=sc.parallelize(range(1,100))
sample_result=distdata.sample(False,0.5)
sample_result.collect()

'''
行动操作：行动操作返回的是一个真正计算后的结果
'''
#聚合操作，reduce
distdata=sc.parallelize([1,2,3,4,5])
reduce_result=distdata.reduce(lambda x,y:x+y)
reduce_result

#统计元素的个数
distfile.count()

#统计个元素出现的次数
distdata=sc.parallelize([1,1,3,3,5])
countByValue_result=distdata.countByValue()
countByValue_result

#显示第一个元素
distfile.first()

#显示前n个数字
distdata=sc.parallelize([1,1,3,3,5])
top_result=distdata.top(3)
top_result

#显示n个元素,用take操作
for line in distfile.take(10):
    print line

#抽样
distdata=sc.parallelize([1,2,3,4,5])
takeSample_result=distdata.takeSample(False,2)
takeSample_result

#foreach,对RDD中的每个元素使用指定的函数
distdata=sc.parallelize([1,2,3,4,5])
foreach_result=distdata.foreach(lambda x:x**2)
foreach_result

'''
其他操作
'''
#传递函数到spark
def isEven(s):
    s=int(s)
    return s%2==0
filter_EvenNumber=distfile.filter(isEven)
for line in filter_EvenNumber.collect():
    print line

#RDD持久化，即将RDD写入内存中，这样后续有多个行动操作时可以重复操作，而不用反复计算
filter_result.persist
filter_result.unpersist  #把持久化的RDD从缓存中移除

#获得RDD的分区数
filter_result.getNumPartitions()

#描述性统计
data=sc.parallelize([1,2,3,4])
data.stats()
data.mean()


#将spark关闭
sc.stop()
