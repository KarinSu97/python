import numpy

#创建一维数组
x=numpy.array([5, 2, 1, 4])

#创建二维数组
y=numpy.array([[13, 2, 3], [41, 51, 6], [17, 8, 19]])

#数组索引
x[1]
y[1][2]

#排序
x.sort()
x
y.sort()
y

#求最大值和最小值
x.max()
x.min()

#数组合并
##水平合并
z=numpy.hstack((y,y))
z=numpy.concatenate((y,y),axis=1)
##垂直合并
z=numpy.vstack((y,y))
z=numpy.concatenate((y,y),axis=0)
##深度合并
z=numpy.dstack((y,y))
##按列合并
z=numpy.column_stack((y,y))
##按行合并
z=numpy.row_stack((y,y))

#数组分割
a=numpy.arange(9).reshape((3,3))
##水平分割
numpy.hsplit(a,3)
numpy.split(a,3,axis=1)
##垂直分割
numpy.vsplit(a,3)
numpy.split(a,3,axis=0)
##深度分割
b=numpy.arange(27).reshape(3,3,3)
numpy.dsplit(b,3)

#数据扩展
numpy.tile([1,2,3,4],2)   #按行扩展为原来的两倍
numpy.tile([1,2,3,4],(2,1))   #按列扩展为原来的两倍

#自定义数据类型
t=numpy.dtype([('name','S10'),('age','int32'),('wage','float64')])
d=numpy.array([('lin',25,7500)],dtype=t)
d

#查看数组的属性
a=numpy.arange(27).reshape(3,3,3)
##数组的维度
a.ndim
##数组的元素个数
a.size
##数组一个元素的字节
a.itemsize
##数组的总字节
a.nbytes

#数组转化
a=numpy.arange(27).reshape(3,3,3)
##将数组扁平化
f=a.flat
f[2]
##将数组转化为list
a.tolist()
##将数组转化为字符串
a.tostring()
##将字符串转化为对应的类型
numpy.fromstring('12:00:00',sep=':',dtype=int)

#通用函数
a=numpy.arange(27).reshape(3,3,3)
##指数函数
numpy.exp(a)
##输出两个数组的最大值
x=numpy.random.randn(10)
y=numpy.random.randn(10)
numpy.maximum(x,y)
##条件函数
x=numpy.array([1,2,3,4,5])
y=numpy.array([-1,3,5,2,7])
c=numpy.array([True,False,False,True,True])
result=numpy.where(c,x,y)   #当c为真时，返回x,否则返回y

#常用统计量
a=numpy.arange(9).reshape(3,3)
##计算均值
a.mean()
a.mean(axis=1)   #按行求均值
##计算标准差
a.std()
##计算方差
a.var()
##求和
a.sum()
a.sum(axis=1)   #按行求和
##累积
a.prod()
a.prod(axis=1)
##累加和
a.cumsum()
##累积
a.cumprod()
##求最大值的索引
a.argmax()
##求最小值的索引
a.argmin()

#布尔型函数
a=numpy.array([True,False,True])
a.any()   #只要存在一个true则返回true
a.all()   #全为true才返回true

#剔除重复值
a=numpy.array(['Lin','Bob','Tom','Lin'])
numpy.unique(a)

#判断一个数组是否在另一个数组中
a=numpy.array([1,2,0,0,5,6])
b=numpy.array([1,2,3])
numpy.in1d(a,b)

#计算两个数组的交集
a=numpy.array([1,2,0,0,5,6])
b=numpy.array([1,2,3])
numpy.intersect1d(a,b)

#计算两个数组的并集
a=numpy.array([1,2,0,0,5,6])
b=numpy.array([1,2,3])
numpy.union1d(a,b)

#差集
a=numpy.array([1,2,0,0,5,6])
b=numpy.array([1,2,3])
numpy.setdiff1d(a,b)

#对称差
a=numpy.array([1,2,0,0,5,6])
b=numpy.array([1,2,3])
numpy.setxor1d(a,b)

#线性代数
from numpy.linalg import *
a=numpy.random.randn(5,5)
##逆矩阵
inv(a)
##矩阵乘积
a.dot(inv(a))
##qr分解
qr(a)
##奇异值分解
svd(a)
##对角线和
a.trace()
##对角线
a.diagonal()

#生成随机数
from numpy import random
##设定随机数种子
random.seed(123)
##将一个序列随机打散
a=[1,2,3]
random.shuffle(a)
a
##均匀分布,[0,1)
random.rand(10)
##生成指定范围的随机整数
random.randint(0,10,5)
##正态分布随机数
random.randn(10)   #均值为0，标准差为1
random.normal(2,1,10)   #均值为2，标准差为1
##二项分布
random.binomial(10,0.5,5)
