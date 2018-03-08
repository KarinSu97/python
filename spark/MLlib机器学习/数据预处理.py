# coding: utf-8
import os
import sys
import pyspark
from pyspark import SparkContext,SparkConf
from pyspark.mllib.linalg import Vectors
import numpy as np

#指定spark_home和pysparkhome
os.environ['SPARK_HOME'] = "/usr/local/spark-1.5.1-bin-hadoop2.4"
sys.path.append("/usr/local/spark-1.5.1-bin-hadoop2.4/python")

#初始化spark,appName参数是在集群UI上显示的你的应用的名称。master是一个Spark、Mesos或YARN集群的URL,
# 如果你在本地运行那么这个参数应该是特殊的”local”字符串
conf=SparkConf().setAppName('test').setMaster('local')
sc=SparkContext(conf=conf)

#将数据转化为稠密向量
denseVec1=np.array([1.0,2.0,3.0])   #可以直接将array数组传递给mllib
denseVec2=Vectors.dense([1.0,2.0,3.0])   #也可以通过dense构建

#将数据转化为稀疏向量,原始数据为[1.0,0.0,2.0,0.0],另外需要指定数据的维度，此时只记录了非0位置的数据
sparseVec1=Vectors.sparse(4,{0:1.0,2:2.0})

#计算TF-IDF
from pyspark.mllib.feature import HashingTF,IDF
# 将若干文本文件读取为TF向量
rdd = sc.wholeTextFiles("data").map(lambda (name, text): text.split())
tf = HashingTF()
tfVectors = tf.transform(rdd).cache()
# 计算IDF，然后计算TF-IDF向量
idf = IDF()
idfModel = idf.fit(tfVectors)
tfIdfVectors = idfModel.transform(tfVectors)

#数据标准化
from pyspark.mllib.feature import StandardScaler
vectors=[Vectors.dense([-2.0, 5.0, 1.0]),Vectors.dense([2.0, 0.0, 1.0])]
dataset=sc.parallelize(vectors)
scaler=StandardScaler(withMean=True,withStd=True)
model=scaler.fit(dataset)
result=model.transform(dataset)
result.collect()

#简单描述统计
from pyspark.mllib.stat import Statistics
describe_data=Statistics.colStats(result)

#相关系数矩阵,可选用pearson或spearman
Statistics.corr(result,method='pearson')

