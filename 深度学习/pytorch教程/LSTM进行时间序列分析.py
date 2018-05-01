'''
预测飞机月流量
'''
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import torch
from torch import nn
from torch import optim
from torch.autograd import Variable

#加载数据集
path='C:\\Users\\T\\Downloads\\code-of-learn-deep-learning-with-pytorch-master\\chapter5_RNN\\time-series\\data.csv'
data_csv=pd.read_csv(path,usecols=[1])

#绘制时间序列图
#plt.plot(data_csv)

#数据预处理，去除NA值,并进行标准化
data_csv=data_csv.dropna()
dataset = data_csv.values
dataset = dataset.astype('float32')
max_value = np.max(dataset)
min_value = np.min(dataset)
scalar = max_value - min_value
dataset = list(map(lambda x: x / scalar, dataset))

#创建数据集，将每个月的前5个月作为输入特征
def create_dataset(dataset,lookback=5):
    dataX, dataY = [], []
    for i in range(len(dataset)-lookback):
        dataX.append(dataset[i:(i+lookback)])
        dataY.append(dataset[i+lookback])
    return np.array(dataX),np.array(dataY)

data_X, data_Y = create_dataset(dataset)

#划分训练集和测试集，以前70%作为训练集
train_size=int(len(data_X)*0.7)
train_X = data_X[:train_size]
train_Y = data_Y[:train_size]

#更改数据为LSTM模型的输入形状，即[seq,batch,input],这里只有一个序列，所以batch=1,另外输入特征input=5,
#序列长度即为训练集的长度
train_X=train_X.reshape(-1,1,5)
train_Y=train_Y.reshape(-1,1,1)

#将数据转变为tensor类型
train_X=torch.from_numpy(train_X)
train_Y=torch.from_numpy(train_Y)

#定义LSTM模型
class lstm_model(nn.Module):
    def __init__(self,input_size,hidden_size,num_layers=2,output_size=1):
        super(lstm_model,self).__init__()
        self.layer1=nn.LSTM(input_size=input_size,hidden_size=hidden_size,num_layers=num_layers)
        self.layer2=nn.Linear(hidden_size,output_size)
    def forward(self, x):
        x,_=self.layer1(x)
        s,b,h=x.shape
        x=x.view(s*b,h)
        x=self.layer2(x)
        x=x.view(s,b,-1)
        return x

model=lstm_model(5,4).cuda()

#定义损失函数和优化函数
criterion=nn.MSELoss()
optimizer=optim.Adam(model.parameters(),lr=0.005)

#进行迭代
for epoch in range(1000):
    x=Variable(train_X).cuda()
    y=Variable(train_Y).cuda()
    #前向传播
    out=model(x)
    loss=criterion(out,y)
    #反向传播
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()
    if (epoch+1) % 20 ==0:
        print('epoch:%d,loss:%.6f' % (epoch+1,loss.data[0]))

#进行预测
model.eval()
data_X=data_X.reshape(-1,1,5)
data_X=torch.from_numpy(data_X)
data_X=Variable(data_X).cuda()
pred=model(data_X)
pred= pred.view(-1).data

#绘制预测效果图
plt.plot(data_Y,'r',label='Y')
plt.plot(pred,'b',label='Predict')
plt.legend(loc='best')