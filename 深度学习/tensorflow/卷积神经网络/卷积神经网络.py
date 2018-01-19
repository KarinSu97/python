'''
###################################
卷积神经网络对MNIST数据进行分类
###################################
'''

import tensorflow as tf
from tensorflow.examples.tutorials.mnist import input_data

#加载MNIST数据集
file_path=r'C:\Users\T\Desktop\TensorFlow\MNIST_data'
mnist=input_data.read_data_sets(file_path,one_hot=True)

#显示数据维度
print(mnist.train.images.shape)
print(mnist.train.labels.shape)

#定义变量，这里采用卷积-池化-卷积-池化-隐藏层-输出层的形式
n_input=784
n_output=10
x=tf.placeholder('float',[None,n_input])
y=tf.placeholder('float',[None,n_output])
keepratio=tf.placeholder('float')
weights={
    #第一层卷积层有32个filter,每个filter为3*3的矩阵，深度为1
    'wc1':tf.Variable(tf.random_normal([3,3,1,32],stddev=0.1)),
    #第二层卷积层有64个filter,每个filter为3*3的矩阵，深度为1
    'wc2':tf.Variable(tf.random_normal([3,3,32,64],stddev=0.1)),
    #第一个全连接层的权重
    'wd1':tf.Variable(tf.random_normal([7*7*64,128],stddev=0.1)),
    #第二个全连接层的权重
    'wd2':tf.Variable(tf.random_normal([128,n_output],stddev=10))
}
biases={
    #第一个卷积层偏置值
    'bc1':tf.Variable(tf.random_normal([32],stddev=0.1)),
    #第二个卷积层偏置值
    'bc2':tf.Variable(tf.random_normal([64],stddev=0.1)),
    #第一个全连接层偏置值
    'bd1':tf.Variable(tf.random_normal([128],stddev=0.1)),
    #第二个全连接层偏置值
    'bd2':tf.Variable(tf.random_normal([n_output],stddev=0.1))
}

#定义前向计算函数
def conv_basic(x,weights,biases,keepratio):
    #将输入转化为tensorflow对应的形式,-1表示自动识别batch大小，这里将输入转化为为28*28*1的形式
    input=tf.reshape(x,[-1,28,28,1])
    #第一次卷积，strides表示步伐，分别表示batch、h、w、channel的步伐大小,padding一般取SAME，表示对不足的窗口补0
    conv1=tf.nn.conv2d(input,weights['wc1'],strides=[1,1,1,1],padding='SAME')
    conv1=tf.nn.relu(tf.nn.bias_add(conv1,biases['bc1']))
    #第一次池化操作,采用2*2的池化操作,步伐为2
    pool1=tf.nn.max_pool(conv1,ksize=[1,2,2,1],strides=[1,2,2,1],padding='SAME')
    #dropout操作
    pool1_dr=tf.nn.dropout(pool1,keepratio)
    #第二次卷积
    conv2=tf.nn.conv2d(pool1_dr,weights['wc2'],strides=[1,1,1,1],padding='SAME')
    conv2=tf.nn.relu(tf.nn.bias_add(conv2,biases['bc2']))
    #第二次池化
    pool2=tf.nn.max_pool(conv2,ksize=[1,2,2,1],strides=[1,2,2,1],padding='SAME')
    #dropout操作
    pool2_dr=tf.nn.dropout(pool2,keepratio)
    #第一个全连接层
    input2=tf.reshape(pool2_dr,shape=[-1,weights['wd1'].get_shape().as_list()[0]])
    fc1=tf.nn.relu(tf.add(tf.matmul(input2,weights['wd1']),biases['bd1']))
    #dropout操作
    fc1_dr=tf.nn.dropout(fc1,keepratio)
    #第二个全连接层
    out=tf.add(tf.matmul(fc1_dr,weights['wd2']),biases['bd2'])
    return out

#执行前向计算
output=conv_basic(x,weights,biases,keepratio)

#定义损失函数
loss=tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits=output,labels=y))

#定义优化器
optimizer=tf.train.AdamOptimizer(0.01)
train=optimizer.minimize(loss)

#计算准确率
acc=tf.reduce_mean(tf.cast(tf.equal(tf.argmax(output,1),tf.argmax(y,1)),'float'))

#进行迭代
n_epoch=50
batch_size=100
with tf.Session() as sess:
    sess.run(tf.global_variables_initializer())
    for i in range(n_epoch):
        num_batch=int(mnist.train.num_examples/batch_size)
        #num_batch=10
        avg_loss=0
        for j in range(num_batch):
            batch_x,batch_y=mnist.train.next_batch(batch_size)
            sess.run(train,feed_dict={x:batch_x,y:batch_y,keepratio:0.7})
            avg_loss+=sess.run(loss,feed_dict={x:batch_x,y:batch_y,keepratio:0.7})/num_batch
        batch_x, batch_y = mnist.train.next_batch(batch_size)
        train_acc=sess.run(acc,feed_dict={x:batch_x,y:batch_y,keepratio:0.7})
        test_acc=sess.run(acc,feed_dict={x:mnist.test.images[0:100,],y:mnist.test.labels[0:100],keepratio:0.7})
        print("第%d次运行的损失值为%.5f，训练集准确率为%.5f，测试集准确率为%.5f" % (i + 1, avg_loss, train_acc, test_acc))


