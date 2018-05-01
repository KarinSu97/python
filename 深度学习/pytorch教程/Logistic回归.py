import torch
import numpy as np
from torch import nn
import torch.optim
from torch.autograd import Variable
import matplotlib.pyplot as plt

#读取数据
path='C:\\Users\\T\\Downloads\\code-of-learn-deep-learning-with-pytorch-master\\chapter3_NN\\logistic-regression\\data.txt'
with open(path,'r') as f:
    lines=f.readlines()
    data_list=[line.split(",") for line in lines]
    data=[(np.float(line[0]),np.float(line[1]),np.float(line[2])) for line in data_list]

#定义模型
class LogisticRegression(nn.Module):
    def __init__(self):
        super(LogisticRegression,self).__init__()
        self.lr=nn.Linear(2,1)
        self.sm=nn.Sigmoid()
    def forward(self, x):
        x=self.lr(x)
        out=self.sm(x)
        return out
model=LogisticRegression().cuda()

#将变量转化为tensor
x_data=torch.FloatTensor([i[:2] for i in data])
y_data=torch.FloatTensor([i[-1] for i in data])

#定义损失函数和优化函数
criterion=nn.BCELoss()
optimizer=torch.optim.SGD(model.parameters(),lr=0.001,momentum=0.9)

#进行迭代
for epoch in range(50000):
    x=Variable(x_data).cuda()
    y=Variable(y_data).cuda()
    #forward
    output=model(x)
    loss=criterion(output,y)
    #计算准确率
    mask=output.ge(0.5).float()
    mask=mask.squeeze(1)
    acc=float((mask==y).sum())/len(y)
    #backward
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()
    if (epoch+1) % 1000 ==0:
        print("epoch:%d,loss:%f,acc:%f" % (epoch+1,loss.data[0],acc))

#权重和偏置值
w1,w2=model.lr.weight[0]
w1=w1.data[0]
w2=w2.data[0]
b=model.lr.bias[0]
b=b.data[0]

#绘制划分效果图
x0=list(filter(lambda x:x[-1]==0,data))
x1=list(filter(lambda x:x[-1]==1,data))
x0_0=[i[0] for i in x0]
x0_1=[i[1] for i in x0]
x1_0=[i[0] for i in x1]
x1_1=[i[1] for i in x1]
plt.plot(x0_0,x0_1,'ro',label='x0')
plt.plot(x1_0,x1_1,'bo',label='x1')
line_x=np.arange(30,100,0.1)
line_y=(-w1*line_x-b)/w2
plt.plot(line_x,line_y)