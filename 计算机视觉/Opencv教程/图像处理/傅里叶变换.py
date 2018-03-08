import cv2
import numpy as np
from scipy import ndimage

'''高通滤波器,主要是放大像素与邻近像素亮度的差值，一般用于检测图像的轮廓'''
#读取图像文件，这里转化为灰色图
img=cv2.imread('C:\\Users\\T\\Downloads\\5.jpg',0)

#方法一：定义两个卷积核
kernel_3x3=np.array([[-1,-1,-1],
                     [-1,8,-1],
                     [-1,-1,-1]])
kernel_5x5=np.array([[-1,-1,-1,-1,-1],
                     [-1,1,2,1,-1],
                     [-1,2,4,2,-1],
                     [-1,1,2,1,-1],
                     [-1,-1,-1,-1,-1]])
k3=ndimage.convolve(img,kernel_3x3)
k5=ndimage.convolve(img,kernel_5x5)

#方法二：先利用低通滤波器，然后与原始图像计算差值，这种方法效果最好
blurred=cv2.GaussianBlur(img,(11,11),0)
g_hpf=img-blurred

cv2.imshow('k3',k3)
cv2.imshow('k5',k5)
cv2.imshow('g_hpf',g_hpf)
cv2.waitKey()

'''低通滤波器，主要是平滑像素与邻居像素的亮度，一般用于去噪和模糊化'''
img=cv2.imread('C:\\Users\\T\\Downloads\\5.jpg',0)
blurred=cv2.GaussianBlur(img,(11,11),0)
cv2.imshow('blurred',blurred)
cv2.waitKey()