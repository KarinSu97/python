import torch.nn as nn
import torch.nn.functional as F
from torch.autograd import Variable
import torch
from torch import autograd

#继承网络的基类
class Model(nn.Module):
    def __init__(self):
        super(Model,self).__init__()
        self.conv1=nn.Conv2d(1,20,5)
        self.conv2=nn.Conv2d(20,20,5)
    #定义了每次执行的计算步骤。在所有的子类中都需要重写这个函数
    def forward(self,x):
        x=F.relu(self.conv1(x))
        return F.relu(self.conv2(x))
model=Model()

#children,返回当前模型子模块中的迭代器
for sub_module in model.children():
    print(sub_module)

#named_children,返回当前模型中子模块中的迭代器及其名称
for name,sub_module in model.named_children():
    print(name,sub_module)

#modules，返回当前模型中所有模块的迭代器
for module in model.modules():
    print(module)

#parameters，返回模型中所有参数的迭代器
for param in model.parameters():
    print(type(param.data),param.size())

#add_module,将一个child module添加到当前model,被添加的module可以通过name属性来获取
class Model(nn.Module):
    def __init__(self):
        super(Model,self).__init__()
        #相当于self.conv=nn.Conv2d(20,20,4)
        self.add_module("conv",nn.Conv2d(10,20,4))
model=Model()
print(model.conv)

#state_dict，保留module中所有parameters和persistent buffers的状态
class Model(nn.Module):
    def __init__(self):
        super(Model, self).__init__()
        self.conv2 = nn.Linear(1, 2)
        self.vari = Variable(torch.rand([1]))
        self.par = nn.Parameter(torch.rand([1]))
        self.register_buffer("buffer", torch.randn([2,3]))

model = Model()
print(model.state_dict().keys())

#一维卷积层
# in_channels(int) – 输入信号的通道
# out_channels(int) – 卷积产生的通道
# kerner_size(int or tuple) - 卷积核的尺寸
# stride(int or tuple, optional) - 卷积步长
# padding (int or tuple, optional)- 输入的每一条边补充0的层数
# dilation(int or tuple, `optional``) – 卷积核元素之间的间距
# groups(int, optional) – 从输入通道到输出通道的阻塞连接数
# bias(bool, optional) - 如果bias=True，添加偏置
m=nn.Conv1d(16,33,3,stride=2)
input=autograd.Variable(torch.randn(20,16,50))
output=m(input)


#最大一维池化层
m=nn.MaxPool1d(3,stride=2)
input=autograd.Variable(torch.randn(20,16,50))
output=m(input)

#平均一维池化层
m=nn.AvgPool1d(3,stride=2)
input=Variable(torch.Tensor([[[1,2,3,4,5,6,7,8,9]]]))
m(input)

#relu激活函数
m=nn.ReLU()
input=Variable(torch.randn(2,2))
m(input)

#阈值函数，输入值小于阈值threshold则会被value代替
m=nn.Threshold(threshold=0.1,value=20)
input=Variable(torch.randn(2,2))
m(input)

#Hardtanh函数，f(x)=+1,if x>1; f(x)=−1,if x<−1; f(x)=x,otherwise
m=nn.Hardtanh(min_value=-1,max_value=1)
input=Variable(torch.randn(2,2))
m(input)

#sigmoid激活函数
m = nn.Sigmoid()
input = autograd.Variable(torch.randn(2))
print(input)
print(m(input))

#tanh函数
m = nn.Tanh()
input = autograd.Variable(torch.randn(2))
print(input)
print(m(input))

#softmax函数，fi(x)=e(xi−shift)/∑je(xj−shift),shift=max(xi)
m = nn.Softmax()
input = autograd.Variable(torch.randn(2, 3))
print(input)
print(m(input))

#批标准化操作，即对每个批次的数据进行标准化操作，y=(x−mean[x])∗gamma/(Var[x]+ϵ)+beta
# num_features： 来自期望输入的特征数，该期望输入的大小为'batch_size x num_features [x width]'
# eps： 为保证数值稳定性（分母不能趋近或取0）,给分母加上的值。默认为1e-5。
# momentum： 动态均值和动态方差所使用的动量。默认为0.1。
# affine： 一个布尔值，当设为true，给该层添加可学习的仿射变换参数。
m=nn.BatchNorm1d(100)
input=Variable(torch.randn(20,100))
m(input)

#建立递归神经网络RNN
# input_size – 输入x的特征数量。
# hidden_size – 隐层的特征数量。
# num_layers – RNN的层数。
# nonlinearity – 指定非线性函数使用tanh还是relu。默认是tanh。
# bias – 如果是False，那么RNN层就不会使用偏置权重 $b_ih$和$b_hh$,默认是True
# batch_first – 如果True的话，那么输入Tensor的shape应该是[batch_size, time_step, feature],输出也是这样。
# dropout – 如果值非零，那么除了最后一层外，其它层的输出都会套上一个dropout层。
# bidirectional – 如果True，将会变成一个双向RNN，默认为False。
rnn = nn.RNN(10, 20, 2)
input = Variable(torch.randn(5, 3, 10))
h0 = Variable(torch.randn(2, 3, 20))
output, hn = rnn(input, h0)


#建立LSTM神经网络
# input_size – 输入的特征维度
# hidden_size – 隐状态的特征维度
# num_layers – 层数（和时序展开要区分开）
# bias – 如果为False，那么LSTM将不会使用$b_{ih},b_{hh}$，默认为True。
# batch_first – 如果为True，那么输入和输出Tensor的形状为(batch, seq, feature)
# dropout – 如果非零的话，将会在RNN的输出上加个dropout，最后一层除外。
# bidirectional – 如果为True，将会变成一个双向RNN，默认为False。
lstm = nn.LSTM(10, 20, 2)
input = Variable(torch.randn(5, 3, 10))   #初始化输入
h0 = Variable(torch.randn(2, 3, 20))   #初始化隐状态
c0 = Variable(torch.randn(2, 3, 20))   #初始化细胞状态
output, hn = lstm(input, (h0, c0))

#Linear线性变换
# in_features - 每个输入样本的大小
# out_features - 每个输出样本的大小
# bias - 若设置为False，这层不会学习偏置。默认值：True
m = nn.Linear(20, 30)
input = autograd.Variable(torch.randn(128, 20))
output = m(input)
print(output.size())

#dropout,将部分元素设置为0
m=nn.Dropout(p=0.2)
input=Variable(torch.randn(20,16))
output=m(input)

#距离函数
# x (Tensor): 包含两个输入batch的张量
# p (real): 范数次数，默认值：2
m=nn.PairwiseDistance(2)
input1=Variable(torch.randn(4,4))
input2=Variable(torch.randn(4,4))
m(input1,input2)

#绝对值损失函数
m=nn.L1Loss()
m(input1,input2)

#MSE损失函数
m=nn.MSELoss()

#负对数似然损失函数
m=nn.NLLLoss()

#并行操作
net=torch.nn.DataParallel(model)
output=net(input1)
