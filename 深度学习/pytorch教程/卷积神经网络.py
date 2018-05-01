'''
卷积神经网络做MNIST手写数字识别
'''
from torchvision.datasets import mnist
from torch.utils.data import DataLoader
from torch import nn
from torch import optim
from torch.autograd import Variable
import numpy as np
import torch

#定义超参数
batch_size=64
learning_rate=0.01
num_epoches=20

#定义数据预处理函数,Compose将预处理函数进行组合
def data_tf(x):
    x = np.array(x, dtype='float32') / 255
    x = (x - 0.5) / 0.5 # 标准化
    x=np.reshape(x,[1,28,28])
    x = torch.from_numpy(x)
    return x

#下载mnist数据集
train_set=mnist.MNIST('C:\\Users\\T\\Desktop\\python\\data',train=True,transform=data_tf,download=True)
test_set=mnist.MNIST('C:\\Users\\T\\Desktop\\python\\data',train=False,transform=data_tf,download=True)

#加载数据集,shuffle=True表示在每个epoch都会对数据进行打乱
train_loader=DataLoader(train_set,batch_size=batch_size,shuffle=True)
test_loader=DataLoader(test_set,batch_size=batch_size,shuffle=False)

#定义卷积神经网络
class CNN(nn.Module):
    def __init__(self):
        super(CNN,self).__init__()
        self.layer1=nn.Sequential(
            nn.Conv2d(1,16,kernel_size=3),   #16,26,26
            nn.BatchNorm2d(16),
            nn.ReLU(True)
        )
        self.layer2=nn.Sequential(
            nn.Conv2d(16, 32, kernel_size=3),  #32,24,24
            nn.BatchNorm2d(32),
            nn.ReLU(True),
            nn.MaxPool2d(kernel_size=2,stride=2)  #32,12,12
        )
        self.layer3 = nn.Sequential(
            nn.Conv2d(32, 64, kernel_size=3),  # 64,10,10
            nn.BatchNorm2d(64),
            nn.ReLU(True)
        )
        self.layer4 = nn.Sequential(
            nn.Conv2d(64, 128, kernel_size=3),  # 128,8,8
            nn.BatchNorm2d(128),
            nn.ReLU(True),
            nn.MaxPool2d(kernel_size=2, stride=2)  # 128,4,4
        )
        self.fc=nn.Sequential(
            nn.Linear(128*4*4,1024),
            nn.ReLU(True),
            nn.Linear(1024,128),
            nn.ReLU(True),
            nn.Linear(128,10)
        )
    def forward(self, x):
        x=self.layer1(x)
        x=self.layer2(x)
        x=self.layer3(x)
        x=self.layer4(x)
        x=x.view(x.size(0),-1)
        x=self.fc(x)
        return x

model=CNN().cuda()

#定义损失函数和优化函数
criterion=nn.CrossEntropyLoss()
optimizer=optim.SGD(model.parameters(),lr=learning_rate,momentum=0.9)

#进行迭代
train_losses=[]
train_acces=[]
test_losses=[]
test_acces=[]
for epoch in range(num_epoches):
    train_loss=0
    train_acc=0
    for im,label in train_loader:
        im=Variable(im).cuda()
        label=Variable(label).cuda()
        #前向传播
        out=model(im)
        loss=criterion(out,label)
        #反向传播
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        #计算训练集损失值和准确率
        train_loss+=loss.data[0]
        _,pred=out.max(1)
        train_acc+=(pred==label).sum().data[0]/im.shape[0]
    train_losses.append(train_loss/len(train_loader))
    train_acces.append(train_acc/len(train_loader))
    #计算测试集的准确率
    model.eval()
    test_loss=0
    test_acc=0
    for im,label in test_loader:
        im=Variable(im).cuda()
        label=Variable(label).cuda()
        out=model(im)
        loss=criterion(out,label)
        test_loss+=loss.data[0]
        _,pred=out.max(1)
        test_acc+=(pred==label).sum().data[0]/im.shape[0]
    test_losses.append(test_loss/len(test_loader))
    test_acces.append(test_acc/len(test_loader))
    print('epoch:%d,train_loss:%.6f,train_acc:%.6f,test_loss:%.6f,test_acc:%.6f' % (
        epoch,train_loss/len(train_loader),train_acc/len(train_loader),test_loss/len(test_loader),test_acc/len(test_loader)
    ))