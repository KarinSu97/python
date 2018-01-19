import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt

#生成数据，构造线性回归模型y=0.1x+0.3
x=np.random.normal(2,4,1000)
e=np.random.randn(1000)
y=0.1*x+0.3+e

#给w和b赋予初始值
w=tf.Variable([1.0],tf.float32,name='w')
b=tf.Variable([1.0],tf.float32,name='b')
y_pred=w*x+b

#定义损失函数
loss=tf.reduce_mean(tf.square(y-y_pred),name='loss')

#定义优化函数，使用梯度下降法，学习率设置为0.1
optimizer=tf.train.GradientDescentOptimizer(0.01)

#定义目标函数
train=optimizer.minimize(loss,name='train')

#进行训练

with tf.Session() as sess:
    sess.run(tf.global_variables_initializer())
    for i in range(200):
        sess.run(train)
        if i%20==0:
            print("w=",sess.run(w),",b=",sess.run(b),",loss=",sess.run(loss))
    plt.scatter(x, y)
    plt.plot(x,sess.run(w)*x+sess.run(b))