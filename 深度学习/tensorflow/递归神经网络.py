'''
###################################
递归神经网络(LSTM)对MNIST数据进行分类
###################################
'''

import tensorflow as tf
from tensorflow.examples.tutorials.mnist import input_data
from tensorflow.contrib import rnn

#加载MNIST数据集
file_path=r'C:\Users\T\Desktop\TensorFlow\MNIST_data'
mnist=input_data.read_data_sets(file_path,one_hot=True)

#显示数据维度
print(mnist.train.images.shape)
print(mnist.train.labels.shape)

#初始化参数
batch_size=50
n_batch=mnist.train.num_examples//batch_size
n_inputs=28
max_time=28
lstm_size=100
n_classes=10

#设置占位符
x=tf.placeholder(tf.float32,[None,784])
y=tf.placeholder(tf.float32,[None,10])

#初始化权重和偏置值
weights=tf.Variable(tf.truncated_normal([lstm_size,n_classes],stddev=0.1))
bias=tf.Variable(tf.constant(0.1,shape=[n_classes]))

#定义RNN函数
def RNN(X,weights,bias):
    inputs=tf.reshape(X,[-1,max_time,n_inputs])
    lstm_cell=tf.contrib.rnn.BasicLSTMCell(lstm_size)
    outputs,final_stat=tf.nn.dynamic_rnn(lstm_cell,inputs,dtype=tf.float32)
    results=tf.nn.softmax(tf.matmul(final_stat[1],weights)+bias)
    return results

#预测值
prediction=RNN(x,weights,bias)

#损失函数
loss=tf.nn.softmax_cross_entropy_with_logits(labels=y,logits=prediction)

#优化器
train=tf.train.AdamOptimizer(1e-4).minimize(loss)

#准确率
correct_prediction=tf.equal(tf.argmax(y,1),tf.argmax(prediction,1))
accuracy=tf.reduce_mean(tf.cast(correct_prediction,tf.float32))

#定义会话
with tf.Session() as sess:
    sess.run(tf.global_variables_initializer())
    for i in range(6):
        for j in range(n_batch):
            batch_xs,batch_ys=mnist.train.next_batch(batch_size)
            sess.run(train,feed_dict={x:batch_xs,y:batch_ys})
        acc=sess.run(accuracy,feed_dict={x:mnist.test.images,y:mnist.test.labels})
        print(str(i)+":"+str(acc))


'''
#定义变量
n_steps=28   #序列长度
n_input=28   #输入序列的维度
n_hidden=128   #隐藏层的维度
n_output=10   #输出序列的维度
x=tf.placeholder('float',[None,n_steps,n_input])
y=tf.placeholder('float',[None,n_output])
weights={
    'hidden':tf.Variable(tf.random_normal([n_input,n_hidden])),
    'out':tf.Variable(tf.random_normal([n_hidden,n_output]))
}
biases={
    'hidden':tf.Variable(tf.random_normal([n_hidden])),
    'out':tf.Variable(tf.random_normal([n_output]))
}

#定义前向计算函数
def RNN_basic(x,weights,biases,n_steps):
    #对x进行变形，将[batch_size,n_steps,n_input]变换为[n_steps,batch_size,n_input]
    x=tf.transpose(x,[1,0,2])
    #对x进行降维，变为[n_steps*batch_size,n_input]
    x=tf.reshape(x,[-1,n_input])
    #计算第一层输入
    h=tf.matmul(x,weights['hidden'])+biases['hidden']
    #对计算结果进行切片，切为[n_steps,batch_size,n_input]形式
    h_split=tf.split(h,n_steps,0)
    #定义LSTM
    #输出还是n_hidden的维度，第一次不做忘记
    lstm_fw_cell=rnn.BasicLSTMCell(n_hidden,forget_bias=1.0)
    lstm_bw_cell = rnn.BasicLSTMCell(n_hidden, forget_bias=1.0)
    #LSTM_O为lstm的输出，LSTM_S为当前的中间结果，用于下一次计算
    LSTM_O,_,_=rnn.static_bidirectional_rnn(lstm_fw_cell,lstm_bw_cell,h_split,dtype=tf.float32)
    out=tf.matmul(LSTM_O[-1],weights['out'])+biases['out']
    return out

#执行前向计算
output=RNN_basic(x,weights,biases,n_steps)

#定义损失函数
loss=tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits=output,labels=y))

#定义优化器
optimizer=tf.train.GradientDescentOptimizer(0.01)
train=optimizer.minimize(loss)

#计算准确率
acc=tf.reduce_mean(tf.cast(tf.equal(tf.argmax(output,1),tf.argmax(y,1)),'float'))

#执行迭代
n_epoch=20
batch_size=16
with tf.Session() as sess:
    sess.run(tf.global_variables_initializer())
    for i in range(n_epoch):
        num_batch=int(mnist.train.num_examples/batch_size)
        avg_loss=0
        for j in range(num_batch):
            batch_x,batch_y=mnist.train.next_batch(batch_size)
            batch_x=tf.reshape(batch_x,[batch_size,n_steps,n_input])
            sess.run(train,feed_dict={x:batch_x,y:batch_y})
            avg_loss+=sess.run(loss,feed_dict={x:batch_x,y:batch_y})/num_batch
            train_acc=sess.run(acc,feed_dict={x:batch_x,y:batch_y})
        #ntest=mnist.test.num_examples
        #test_acc=sess.run(acc,feed_dict={x:mnist.test.images.reshape([ntest,n_steps,n_input])})
        #print("第%d次迭代的损失值为%.5f，训练集准确率为%.5f，测试集准确率为%.5f" % (i+1,avg_loss,train_acc,test_acc))
'''