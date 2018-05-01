import numpy as np
import matplotlib.pyplot as plt
import torch
from torch import nn
from torch import optim
from torch.autograd import Variable

#模拟数据
x_train = np.array([[3.3], [4.4], [5.5], [6.71], [6.93], [4.168],
                    [9.779], [6.182], [7.59], [2.167], [7.042],
                    [10.791], [5.313], [7.997], [3.1]], dtype=np.float32)

y_train = np.array([[1.7], [2.76], [2.09], [3.19], [1.694], [1.573],
                    [3.366], [2.596], [2.53], [1.221], [2.827],
                    [3.465], [1.65], [2.904], [1.3]], dtype=np.float32)
plt.scatter(x_train,y_train)

#将numpy数组转化为tensor
x_train=torch.from_numpy(x_train)
y_train=torch.from_numpy(y_train)

#定义线性回归模型
class LinearRegression(nn.Module):
    def __init__(self):
        super(LinearRegression,self).__init__()
        #输入和输出都是1维
        self.linear=nn.Linear(1,1)

    def forward(self, x):
        output=self.linear(x)
        return output
model=LinearRegression().cuda()

#定义损失函数和优化函数
criterion=nn.MSELoss()
optimizer=optim.SGD(model.parameters(),lr=0.001)

#进行迭代
for epoch in range(100):
    inputs=Variable(x_train).cuda()
    target=Variable(y_train).cuda()
    #forward
    out=model(inputs)
    loss=criterion(out,target)
    #backward
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()
    if (epoch+1)%20==0:
        print('%d--%f' % (epoch+1,loss.data[0]))

#进行预测
model.eval()   #将模型变成测试模式
predict=model(inputs)
plt.plot(x_train.numpy(),y_train.numpy(),'ro')
plt.plot(x_train.numpy(),np.array(predict.data))