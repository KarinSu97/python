from torch import optim
import torch

#随机梯度下降
optimizer=optim.SGD(model.parameters(),lr=0.01)
#指定不同参数的学习速率，model.base的参数将会使用1e-2的学习率，model.classifier的参数将会使用1e-3的学习率，
# 并且0.9的momentum将会被用于所有的参数
optim.SGD([
                {'params': model.base.parameters()},
                {'params': model.classifier.parameters(), 'lr': 1e-3}
            ], lr=1e-2, momentum=0.9)

#optimizer.step(),更新所有的参数
for input,target in dataset:
    optimizer.zero_grad()
    output=model(input)
    loss=loss_fn(output,target)
    loss.backward()
    optimizer.step()