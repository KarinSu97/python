import tensorflow as tf
import matplotlib.pyplot as plt
from tensorflow.examples.tutorials.mnist import input_data
import numpy as np

#下载mnist数据集
mnist=input_data.read_data_sets(r'C:\Users\T\Desktop\TensorFlow\MNIST_data',one_hot=True)
train_x=mnist.train.images
train_y=mnist.train.labels
test_x=mnist.test.images
test_y=mnist.test.labels

#数据集的维度
train_x.shape
test_x.shape

#显示照片
plt.matshow(train_x[0].reshape([28,28]),cmap=plt.get_cmap('gray'))

#设置批次,设置每100一个批次
batch_size=100
batch_x,batch_y=mnist.train.next_batch(batch_size)
batch_x.shape
batch_y.shape