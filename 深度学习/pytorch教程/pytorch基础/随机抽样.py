import torch

#设定随机数的种子
torch.manual_seed(1234)

#返回设定的种子
torch.initial_seed()

#生成伯努利分布
a=torch.Tensor(3,3).uniform_(0,1)
a
torch.bernoulli(a)

