import tensorflow as tf

#定义变量
w=tf.Variable([[2.0,1.0]])
x=tf.Variable([[0.5],[1.0]])
y=tf.matmul(w,x)

#生成零矩阵和全1矩阵
tf.zeros([3,4],tf.float32)
tensor=[[1,2,3],[1,2,3]]
tf.zeros_like(tensor,tf.float32)
tf.ones([3,4],tf.float32)
tf.ones_like(tensor,tf.float32)

#定义常量
tensor=tf.constant([1,2,3,4,5,6])
tensor=tf.constant(-1.0,shape=[2,3])

#生成等差数列
tf.linspace(10.0,12.0,3,name='linspace')
tf.range(1,10,2)

#生成正态随机数
tf.random_normal([2,3],mean=0.0,stddev=1.0)

#打乱操作
c=tf.constant([[1,2],[3,4],[5,6]])
c=tf.random_shuffle(c)

#初始化全局变量
init_op=tf.global_variables_initializer()

#定义session会话,这样才能执行变量计算操作
with tf.Session() as sess:
    sess.run(init_op)
    #打印y的值
    print(y.eval())

#赋值操作
state=tf.Variable(0)
#将state+1
new_value=tf.add(state,tf.constant(1))
#将new_value赋值给state
update=tf.assign(state,new_value)
with tf.Session() as sess:
    sess.run(tf.global_variables_initializer())
    print(state.eval())
    for i in range(3):
        sess.run(update)
        print(state.eval())

#保存操作
w=tf.Variable([[2.0,1.0]])
x=tf.Variable([[0.5],[1.0]])
y=tf.matmul(w,x)
init_op=tf.global_variables_initializer()
saver=tf.train.Saver()
with tf.Session() as sess:
    sess.run(init_op)
    saver.save(sess,r'C:\Users\T\Desktop\python视频')

#将numpy格式的数据转化为tensoflow对应格式的数据
import numpy as np
a=np.zeros([2,3])
b=tf.convert_to_tensor(a)
with tf.Session() as sess:
    print(sess.run(b))

#占位符
input1=tf.placeholder(tf.float32)
input2=tf.placeholder(tf.float32)
output=tf.multiply(input1,input2)
with tf.Session() as sess:
    #通过feed_dict进行赋值操作
    print(sess.run([output],feed_dict={input1:[2.0],input2:[3.0]}))