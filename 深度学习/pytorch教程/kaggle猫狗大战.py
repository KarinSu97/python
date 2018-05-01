'''
利用迁移学习来进行猫狗识别
'''
import os
import shutil
from torchvision import transforms
from torchvision.datasets import ImageFolder
from torch.utils.data import DataLoader
from torchvision import models
from torch import nn
import torch
from torch import optim
from torch.autograd import Variable

#超参数
batch_size=32
fix_param=True   #是否固定住卷积层的参数，若是则不更新卷积层的参数
num_epoch=20

#将训练集和测试集划分为dog文件夹和cat文件夹
train_path='C:/Users/T/Desktop/python视频/data/train'
test_path = 'C:/Users/T/Desktop/python视频/data/val'
# img_list=os.listdir(train_path)
# cat_list=list(filter(lambda x:x[:3]=='cat',img_list))
# dog_list=list(filter(lambda x:x[:3]=='dog',img_list))
# os.mkdir(os.path.join(train_path,'dog'))
# os.mkdir(os.path.join(train_path,'cat'))
# os.mkdir(os.path.join(test_path, 'dog'))
# os.mkdir(os.path.join(test_path, 'cat'))
# for i in range(len(cat_list)):
#     if i <= int(len(cat_list)*0.9):
#         shutil.move(os.path.join(train_path,cat_list[i]),os.path.join(train_path,'cat',cat_list[i]))
#     else:
#         shutil.move(os.path.join(train_path,cat_list[i]), os.path.join(test_path, 'cat',cat_list[i]))
#
# for i in range(len(dog_list)):
#     if i <= int(len(dog_list)*0.9):
#         shutil.move(os.path.join(train_path,dog_list[i]),os.path.join(train_path,'dog',dog_list[i]))
#     else:
#         shutil.move(os.path.join(train_path,dog_list[i]), os.path.join(test_path, 'dog',dog_list[i]))

#定义数据预处理函数
data_transforms={
    #训练集预处理函数
    'train':transforms.Compose([
        #首先对图片进行随机尺寸的裁剪，然后对裁剪的图片进行一个随机比例的缩放 ，最后将图片变成给定的大小
        transforms.RandomSizedCrop(299),
        #对图像进行水平翻转
        transforms.RandomHorizontalFlip(),
        #将图像转化为tensor对象
        transforms.ToTensor(),
        #对图像进行标准化
        transforms.Normalize((0.5,0.5,0.5),(0.5,0.5,0.5))
    ]),
    'test':transforms.Compose([
        #对图像进行缩放
        transforms.Scale(320),
        #对图像进行中心裁剪
        transforms.CenterCrop(299),
        #将图像转化为tensor对象
        transforms.ToTensor(),
        #对图像进行标准化
        transforms.Normalize((0.5,0.5,0.5),(0.5,0.5,0.5))
    ])
}

#加载数据集
data_folder={
    'train':ImageFolder(train_path,transform=data_transforms['train']),
    'test':ImageFolder(test_path,transform=data_transforms['test'])
}
data_loader={
    'train':DataLoader(data_folder['train'],batch_size=batch_size,shuffle=True,num_workers=4),
    'test':DataLoader(data_folder['test'],batch_size=batch_size,shuffle=False,num_workers=4)
}

#数据集大小
data_size={
    'train':len(data_loader['train'].dataset),
    'test':len(data_loader['test'].dataset)
}

#迁移学习，直接调用resnet18模型
transfer_model=models.resnet18(pretrained=True)

#是否固定住模型的参数
if fix_param:
    for param in transfer_model.parameters():
        param.requires_grad=False

#修改模型的全连接层
dim_in=transfer_model.fc.in_features
transfer_model.fc=nn.Linear(8192,2)
transfer_model=transfer_model.cuda()

#定义损失函数和优化函数
criterion=nn.CrossEntropyLoss()
if fix_param:
    optimizer=optim.Adam(transfer_model.fc.parameters(),lr=0.001)
else:
    optimizer=optim.Adam(transfer_model.parameters(),lr=0.001)

#进行迭代
for epoch in range(num_epoch):
    train_loss=0
    train_acc=0
    transfer_model.train()
    for im,label in data_loader['train']:
        im=Variable(im).cuda()
        label=Variable(label).cuda()
        #前向传播
        out=transfer_model(im)
        loss=criterion(out,label)
        #反向传播
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        #计算训练集损失值和准确率
        train_loss+=loss.data[0]*label.size(0)
        _, pred = torch.max(out, 1)
        num_correct = torch.sum(pred == label)
        train_acc += num_correct.data[0]
    train_loss/=data_size['train']
    train_acc/=data_size['train']
    #计算测试集损失值和准确率
    transfer_model.eval()
    test_loss=0
    test_acc=0
    for im,label in data_loader['test']:
        im = Variable(im).cuda()
        label = Variable(label).cuda()
        out=transfer_model(im)
        loss=criterion(out,label)
        _,pred=torch.max(out,1)
        num_correct=torch.sum(pred==label)
        test_acc+=num_correct.data[0]
        test_loss+=loss.data[0]*label.size(0)
    test_acc/=data_size['test']
    test_loss/=data_size['test']
    print('epoch:%d,train_loss:%.4f,train_acc:%.4f,test_loss:%.4f,test_acc:%.4f' % (
        epoch+1,train_loss,train_acc,test_loss,test_acc
    ))

#对单张图片进行预测
from PIL import Image
im_new=Image.open('C:\\Users\\T\\Downloads\\1.jpg')
im_new=data_transforms['test'](im_new)
transfer_model.eval()
out=transfer_model(Variable(im_new.view(1,3,299,299)).cuda())