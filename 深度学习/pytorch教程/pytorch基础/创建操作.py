import torch
import numpy as np

#返回x中元素的个数
torch.numel(x)

#创建单位矩阵
torch.eye(n=3)

#将numpy数组转化为torch中的张量,返回的张量tensor和numpy的ndarray共享同一内存空间。修改一个会导致另外一个也被修改。
# 返回的张量不能改变大小。
a=np.array([1,2,3])
b=torch.from_numpy(a)
b
b[0]=-1
a

#生成等差数列,数列长度为steps
torch.linspace(start=0,end=10,steps=5)

#返回一个1维张量，包含在区间 10start 和 10end上以对数刻度均匀间隔的steps个点
torch.logspace(-10,10,5)

#返回一个全为1的张量
torch.ones(2,3)

#生成全为0的张量
torch.zeros(2,3)

#判断是否是一个张量
torch.is_tensor(b)

#产生区间[0,1)的均匀分布
torch.rand(2,3)

#生成正态分布,均值为0，标准差为1
torch.randn(2,3)

#给定参数n，返回一个从0 到n -1 的随机整数排列
torch.randperm(10)

#返回一个1维张量，长度为 floor((end−start)/step)。包含从start到end，以step为步长的一组序列值(默认步长为1)。
torch.arange(0,10,2)