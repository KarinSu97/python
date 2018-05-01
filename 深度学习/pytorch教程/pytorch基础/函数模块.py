import torch.nn.functional as F
from torch.autograd import Variable
import torch

#卷积函数
filters=Variable(torch.randn(33,16,3))
inputs=Variable(torch.randn(20,16,50))
F.conv1d(inputs,filters)

#池化函数
input = Variable(torch.Tensor([[[1,2,3,4,5,6,7]]]))
F.avg_pool1d(input, kernel_size=3, stride=2)

