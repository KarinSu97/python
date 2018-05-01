import torch

#tensor张量的构建
torch.FloatTensor([1,2,3],[4,5,6])  #通过列表构建
torch.IntTensor(2,4).zero_()   #通过规定大小构建

#会改变tensor的函数操作会用一个下划线后缀来标示。比如，torch.FloatTensor.abs_()会在原地计算绝对值，并返回改变后的tensor，
#而tensor.FloatTensor.abs()将会在一个新的tensor中计算结果。
torch.Tensor(4,3).fill_(1)   #用指定的数字填充Tensor

#将两个张量按照指定的顺序进行相加
a=torch.ones(3,3)
b=torch.Tensor([[1,2,3],[4,5,6],[7,8,9]])
index=torch.LongTensor([0,2,1])
a.index_add_(0,index,b)

#将一个张量的内容覆盖到另一个张量
a=torch.Tensor(3,3)
b=torch.Tensor([[1,2,3],[4,5,6],[7,8,9]])
index=torch.LongTensor([0,2,1])
a.index_copy_(0,index,b)

#根据指定的顺序或位置填充指定的数字
a=torch.arange(1,10).view(3,3)
index=torch.LongTensor([0,2])
a.index_fill_(0,index,-1)

#切片
a=torch.arange(1,10).view(3,3)
a.narrow(0,0,2)
a.narrow(1,1,2)

#维度变换
x=torch.Tensor(2,3,5)
x.size()
x.permute(2,0,1).size()

#沿着指定的维度重复Tensor
x=torch.Tensor([1,2,3])
x.repeat(4,2)

#改变tensor的大小
x=torch.Tensor([[1,2,3],[4,5,6],[7,8,9]])
x.resize_(2,2)

#将tensor的大小调整为与指定tensor同样大小
x=torch.Tensor([[1,2,3],[4,5,6],[7,8,9]])
y=torch.Tensor(4,4)
x.resize_as_(y)

#返回tensor的类型
x=torch.Tensor([[1,2,3],[4,5,6],[7,8,9]])
x.type()
