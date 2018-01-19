'''
神经网络可视化，以二次函数为例
'''
import tensorflow as tf
import numpy as np

#生成模拟数据
x_data=np.linspace(-1,1,300)[:,np.newaxis]
noise=np.random.normal(0,0.05,x_data.shape)
y_data=np.square(x_data)-0.5+noise

#定义添加网络层的函数
def add_layer(inputs,in_size,out_size,n_layer,activation_function=None):
    layer_name="layer%s" % n_layer
    #定义层的名字
    with tf.name_scope(layer_name):
        #定义权重的名字
        with tf.name_scope("weights"):
            Weights=tf.Variable(tf.random_normal([in_size,out_size]),name='W')
            #记录权重的变动
            tf.summary.histogram(layer_name+"/weights",Weights)
        #定义偏置值的名字
        with tf.name_scope('biases'):
            biases=tf.Variable(tf.random_normal([1,out_size]),name='b')
            #记录偏置值的变动
            tf.summary.histogram(layer_name+'/biases',biases)
        #定义Wx_plus_b名字
        with tf.name_scope('Wx_plus_b'):
            Wx_plus_b=tf.add(tf.matmul(inputs,Weights),biases)
        if activation_function is not None:
            outputs=activation_function(Wx_plus_b)
        else:
            outputs=Wx_plus_b
        #记录outputs的变动
        tf.summary.histogram(layer_name+'/outputs',outputs)
        return outputs

#定义输入变量
with tf.name_scope('inputs'):
    x=tf.placeholder(tf.float32,[None,1],name='x_inputs')
    y=tf.placeholder(tf.float32,[None,1],name='y_inputs')

#定义神经网络结构
layer1=add_layer(x,in_size=1,out_size=10,n_layer=1,activation_function=tf.nn.relu)
pred=add_layer(layer1,in_size=10,out_size=1,n_layer=2,activation_function=None)

#定义损失函数
with tf.name_scope("loss"):
    loss=tf.reduce_mean(tf.reduce_sum(tf.square(pred-y),reduction_indices=[1]))
    #记录损失函数的变动，因为是标量，所以用scalar
    tf.summary.scalar("loss",loss)

#定义优化器
with tf.name_scope('train'):
    train=tf.train.GradientDescentOptimizer(0.01).minimize(loss)

#定义会话
sess=tf.Session()

#将所有的summary进行合并
merged=tf.summary.merge_all()
writer=tf.summary.FileWriter('C:/Users/T/Desktop/logs/',sess.graph)

#初始化变量
sess.run(tf.global_variables_initializer())

#进行迭代
for i in range(1000):
    sess.run(train,feed_dict={x:x_data,y:y_data})
    #每50次保存一次summary
    if i % 50 ==0:
        print(sess.run(loss,feed_dict={x:x_data,y:y_data}))
        result=sess.run(merged,feed_dict={x:x_data,y:y_data})
        writer.add_summary(result,i)

#运行结束在cmd中输入:tensorboard --logdir=C:/Users/T/Desktop/logs/,记得路径不能带引号