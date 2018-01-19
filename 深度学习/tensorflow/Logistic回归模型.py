'''
###################################
Logistic回归模型对MNIST数据进行分类
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

#定义变量
x=tf.placeholder('float',[None,784])
y=tf.placeholder('float',[None,10])
w=tf.Variable(tf.zeros([784,10]))
b=tf.Variable(tf.zeros([10]))

#定义损失函数
actv=tf.nn.softmax(tf.matmul(x,w)+b)
loss=tf.reduce_mean(-tf.reduce_sum(y*tf.log(actv),1))

#定义优化器
optimizer=tf.train.GradientDescentOptimizer(0.01)
train=optimizer.minimize(loss)

#计算准确率，tf.cast是将bool值转化为数字形式
acc=tf.reduce_mean(tf.cast(tf.equal(tf.argmax(actv,1),tf.argmax(y,1)),"float"))

#训练,迭代50次,每5次输出结果(损失值，训练集准确率、测试集准确率)
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
        if i%5==0:
            train_acc=sess.run(acc,feed_dict={x:mnist.train.images,y:mnist.train.labels})
            test_acc=sess.run(acc,feed_dict={x:mnist.test.images,y:mnist.test.labels})
            print("第%d次迭代的损失值为%.5f，训练集准确率为%.5f，测试集的准确率为%.5f" % (i,avg_loss,train_acc,test_acc))
