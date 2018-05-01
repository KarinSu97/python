import tensorflow as tf
from tensorflow.contrib import layers

#定义计算图
g1=tf.Graph()

#变量定义和常量定义
with g1.as_default():
    # 在计算图上定义变量v，并初始化为0
    v=tf.Variable(tf.zeros([1]))
    #定义常量
    a=tf.constant([1.0,2.0],name="a")
    b=tf.constant([1.0,1.0],name="b")

#执行计算,定义会话
with tf.Session(graph=g1) as sess:
    #全局变量初始化
    tf.global_variables_initializer().run()
    #显示变量值
    print(sess.run(v))
    #add表示加法运算
    print(sess.run(tf.add(a,b)))

#也可以通过另一种方式来定义会话
sess=tf.Session(graph=g1)
with sess.as_default():
    print(a.eval())

#配置会话
#allow_soft_placement表示在以下任意一个条件成立时，GPU上的运算可以放到CPU上进行
#1.运算无法在GPU上执行
#2.没有GPU资源
#3.运算输入包含对CPU资源的调用
config=tf.ConfigProto(allow_soft_placement=True)
sess=tf.Session(config=config)

#获取张量的维度
a.get_shape()

#矩阵乘法
a=tf.constant([[1.0,2.0]])
b=tf.constant([[2.0],[3.0]])
result=tf.matmul(a,b)
with tf.Session() as sess:
    print(sess.run(result))

#变量初始化
weight=tf.Variable(tf.random_normal([2,3],mean=0,stddev=2,seed=1))   #用均值为0，标准差为2的正态分布产生2*3的矩阵
weight=tf.Variable(tf.truncated_normal([2,3],mean=0,stddev=2))  #也是正态分布，但是如果产生的值偏离均值超过2倍标准差，则会被重新赋值
weight=tf.Variable(tf.random_uniform([2,3],minval=0,maxval=2))  #均匀分布
weight=tf.Variable(tf.zeros([2,3]))   #常数初始化，这里全为0
weight=tf.Variable(tf.ones([2,3]))    #常数初始化，这里全为1
weight=tf.Variable(tf.fill([2,3],9))    #常数初始化，这里全为9
weight1=tf.Variable(weight.initialized_value())   #通过其他变量的初始化值来作为初始化

#获得全部的变量
tf.global_variables()

#获得全部需要优化的变量
tf.trainable_variables()

#tf.clip_by_value,限制数组的数值范围
a=tf.constant([1.0,2.0,3.0,4.0,5.0])
sess=tf.Session()
with sess.as_default():
    print(tf.clip_by_value(a,2.5,4.5).eval())

#计算矩阵的平均值
a=tf.constant([[1,2,3],[4,5,6]],dtype=tf.float32)
with tf.Session() as sess:
    print(sess.run(tf.reduce_mean(a)))

#损失函数
loss=tf.nn.softmax_cross_entropy_with_logits(labels=y,logits=output)   #带有softmax的交叉熵,主要是多分类情况
loss=tf.nn.sparse_softmax_cross_entropy_with_logits(labels=y,logits=output)  #功能同softmax_cross_entropy_with_logits，只不过是用在只有一个正确答案的情况，可以加速计算过程
mse=tf.reduce_mean(tf.square(y-output))  #均方误差，主要是回归问题

#带正则化的损失函数
x=tf.placeholder(dtype=tf.float32,shape=[None,2])
y=tf.placeholder(dtype=tf.float32,shape=[None,1])
w=tf.Variable(tf.random_normal([2,1],stddev=1))
output=tf.matmul(x,w)
loss=tf.reduce_mean(tf.square(y-output))+layers.l2_regularizer(0.1)(w)   #0.1表示正则话系数，L2正则化
loss=tf.reduce_mean(tf.square(y-output))+layers.l1_regularizer(0.1)(w)   #L1正则化

#比较两个张量元素的大小
a=tf.constant([1.0,2.0,4.0])
b=tf.constant([2.0,3.0,1.0])
with tf.Session() as sess:
    print(sess.run(tf.greater(a,b)))

#变量管理
#当变量还没存在时，不能用reuse=True
with tf.variable_scope('bar'):
    v=tf.get_variable("v",shape=[2,3],initializer=tf.random_normal_initializer(stddev=1.0))

#当变量已经存在时，如果想创建一个同名的变量，则必须设置reuse=True
with tf.variable_scope('bar',reuse=True):
    v1=tf.get_variable('v',shape=[2,3])

#直接引用其他命名空间的变量
with tf.variable_scope('var'):
    v2=tf.get_variable("bar/v",[2,3])
