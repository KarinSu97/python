from PIL import Image
from torchvision import transforms
import os
import torch
from torch.autograd import Variable
from torch import nn
from torchvision import models
from torch import optim
import matplotlib.pyplot as plt

'''1.加载图像'''
#定义图像加载函数
def load_img(img_path):
    img=Image.open(img_path).convert('RGB')
    img=img.resize((200,200))
    img=transforms.ToTensor()(img)
    img=img.unsqueeze(0)
    return img

#定义图像展示函数
def show_img(img):
    img=img.squeeze(0)
    img=transforms.ToPILImage()(img)
    img.show()

#加载原图像和风格图像
path='C:/Users/T/Downloads/code-of-learn-deep-learning-with-pytorch-master/chapter9_Computer-Vision/neural-transfer/picture'
content_img=load_img(os.path.join(path,'dancing.jpg'))
content_img=Variable(content_img).cuda()
style_img=load_img(os.path.join(path,'style2.jpg'))
style_img=Variable(style_img).cuda()
input_img = content_img.clone()


'''2.定义损失函数'''
#定义内容损失函数类
class Content_Loss(nn.Module):
    def __init__(self,target,weight):
        super(Content_Loss,self).__init__()
        self.weight = weight
        #detach是将target从模型中分离出来
        self.target = target.detach() * self.weight
        self.criterion=nn.MSELoss()
    def forward(self, input):
        self.loss=self.criterion(input*self.weight,self.target)
        out=input.clone()
        return out
    def backward(self):
        self.loss.backward(retain_variables=True)
        return self.loss

#定义风格矩阵类
class Gram(nn.Module):
    def __init__(self):
        super(Gram,self).__init__()
    def forward(self, input):
        a,b,c,d=input.size()
        #将图像进行展开，变成（深度，长*宽）的形式
        feature=input.view(a*b,c*d)
        #计算深度两两之间的内积
        gram=torch.mm(feature,feature.t())
        #进行标准化
        gram/=(a*b*c*d)
        return gram

#定义风格损失函数类
class Style_Loss(nn.Module):
    def __init__(self, target, weight):
        super(Style_Loss, self).__init__()
        self.weight = weight
        self.target = target.detach() * self.weight
        self.gram = Gram()
        self.criterion = nn.MSELoss()
    def forward(self, input):
        G = self.gram(input) * self.weight
        self.loss = self.criterion(G, self.target)
        out = input.clone()
        return out
    def backward(self, retain_variabels=True):
        self.loss.backward(retain_variables=retain_variabels)
        return self.loss


'''3.定义模型'''
#采用vgg19神经网络,只需要vgg19的卷积层
vgg=models.vgg19(pretrained=True).features
vgg=vgg.cuda()

#指定计算内容差异和风格差异需要的层
content_layers_default=['conv_4']
style_layers_default = ['conv_1', 'conv_2', 'conv_3', 'conv_4', 'conv_5']

#模型重构
def get_style_model_and_loss(style_img,content_img,cnn=vgg,style_weight=1000,content_weight=1):
    #内容差异列表和风格差异列表
    content_loss_list = []
    style_loss_list = []
    #定义一个空模型
    model=nn.Sequential().cuda()
    #风格矩阵计算函数
    gram=Gram().cuda()
    #开始重构
    i=1
    for layer in cnn:
        if isinstance(layer,nn.Conv2d):
            name = 'conv_' + str(i)
            model.add_module(name, layer)
            if name in content_layers_default:
                target = model(content_img)
                content_loss = Content_Loss(target, content_weight)
                model.add_module('content_loss_' + str(i), content_loss)
                content_loss_list.append(content_loss)
            if name in style_layers_default:
                target = model(style_img)
                target = gram(target)
                style_loss = Style_Loss(target, style_weight)
                model.add_module('style_loss_' + str(i), style_loss)
                style_loss_list.append(style_loss)
            i+=1
        if isinstance(layer, nn.MaxPool2d):
            name = 'pool_' + str(i)
            model.add_module(name, layer)
        if isinstance(layer, nn.ReLU):
            name = 'relu' + str(i)
            model.add_module(name, layer)
    return model, style_loss_list, content_loss_list


'''4.训练模型'''
#指定优化的参数为输入图像的像素
def get_input_param_optimier(input_img):
    input_param = nn.Parameter(input_img.data)
    #论文作者建议用LBFGS作为优化函数
    optimizer = optim.LBFGS([input_param])
    return input_param, optimizer

#定义训练函数
def run_style_transfer(content_img, style_img, input_img, num_epoches=300):
    model, style_loss_list, content_loss_list = get_style_model_and_loss(
        style_img, content_img)
    input_param, optimizer = get_input_param_optimier(input_img)
    epoch = [0]
    while epoch[0] < num_epoches:
        def closure():
            input_param.data.clamp_(0, 1)
            model(input_param)
            style_score = 0
            content_score = 0
            optimizer.zero_grad()
            for sl in style_loss_list:
                style_score += sl.backward()
            for cl in content_loss_list:
                content_score += cl.backward()
            epoch[0] += 1
            if epoch[0] % 50 == 0:
                print('run {}'.format(epoch))
                print('Style Loss: {:.4f} Content Loss: {:.4f}'.format(
                    style_score.data[0], content_score.data[0])
                )
            return style_score + content_score
        optimizer.step(closure)
        input_param.data.clamp_(0, 1)
    return input_param.data

#开始训练
out = run_style_transfer(content_img, style_img, input_img, num_epoches=200)
show_img(out.cpu())
save_pic = transforms.ToPILImage()(out.cpu().squeeze(0))
save_pic.save(os.path.join(path,'output.jpg'))

#显示图像
fig=plt.figure()
fig.add_subplot(1,3,1)
plt.imshow(plt.imread(os.path.join(path,'dancing.jpg')))
plt.axis('off')
fig.add_subplot(1,3,2)
plt.imshow(plt.imread(os.path.join(path,'style2.jpg')))
plt.axis('off')
fig.add_subplot(1,3,3)
plt.imshow(plt.imread(os.path.join(path,'output.jpg')))
plt.axis('off')
