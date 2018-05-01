import torch.nn as nn
import torch

#利用均匀分布进行初始化操作
# tensor - n维的torch.Tensor
# a - 均匀分布的下界
# b - 均匀分布的上界
w=torch.Tensor(3,5)
nn.init.uniform(w,a=0,b=1)

#利用正态分布进行初始化
w=torch.Tensor(3,5)
nn.init.normal(w,mean=0,std=1)

#用常量进行初始化
w=torch.Tensor(3,5)
nn.init.constant(w,val=5)

#用单位矩阵进行初始化
w=torch.Tensor(3,5)
nn.init.eye(w)