'''
###################################
BP神经网络对MNIST数据进行分类
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

#定义变量,这里采用含有两层隐含层的神经网络，第一层隐含层有256个节点，第二层隐含层有128个节点
n_input=784
n_hidden_1=256
n_hidden_2=128
n_output=10

x=tf.placeholder('float',[None,n_input])
y=tf.placeholder('float',[None,n_output])
weights={
    'w1':tf.Variable(tf.random_normal([n_input,n_hidden_1])),
    'w2':tf.Variable(tf.random_normal([n_hidden_1,n_hidden_2])),
    'w3':tf.Variable(tf.random_normal([n_hidden_2,n_output]))
}
biases={
    'b1':tf.Variable(tf.zeros([n_hidden_1])),
    'b2':tf.Variable(tf.zeros([n_hidden_2])),
    'b3':tf.Variable(tf.zeros([n_output]))
}

#前向计算
layer_1 = tf.nn.sigmoid(tf.add(tf.matmul(x, weights['w1']), biases['b1']))
layer_2 = tf.nn.sigmoid(tf.add(tf.matmul(layer_1, weights['w2']), biases['b2']))
pred=tf.matmul(layer_2, weights['w3']) + biases['b3']


#定义损失函数
loss=tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits=pred,labels=y))

#定义优化器
optimizer=tf.train.GradientDescentOptimizer(0.01)
train=optimizer.minimize(loss)

#定义准确率函数
acc=tf.reduce_mean(tf.cast(tf.equal(tf.argmax(pred,1),tf.argmax(y,1)),'float'))

#进行迭代
n_epoch=50
batch_size=100
with tf.Session() as sess:
    sess.run(tf.global_variables_initializer())
    for i in range(n_epoch):
        num_batch=int(mnist.train.num_examples/batch_size)
        avg_loss=0
        for j in range(num_batch):
            batch_x,batch_y=mnist.train.next_batch(batch_size)
            sess.run(train,feed_dict={x:batch_x,y:batch_y})
            avg_loss+=sess.run(loss,feed_dict={x:batch_x,y:batch_y})/num_batch
        if (i+1)%5==0:
            train_acc=sess.run(acc,feed_dict={x:mnist.train.images,y:mnist.train.labels})
            test_acc=sess.run(acc,feed_dict={x:mnist.test.images,y:mnist.test.labels})
            print("第%d次运行的损失值为%.5f，训练集准确率为%.5f，测试集准确率为%.5f" % (i+1,avg_loss,train_acc,test_acc))