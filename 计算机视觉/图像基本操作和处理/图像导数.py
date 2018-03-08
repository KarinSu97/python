from PIL import Image
import numpy as np
from scipy.ndimage import filters
from matplotlib.pylab import *

#Sobel滤波器
im=np.array(Image.open('C:\\Users\\T\\Downloads\\5.jpg').convert('L'))
#计算x方向的导数
imx=np.zeros(im.shape)
filters.sobel(im,1,imx)
#计算y方向的导数
imy=np.zeros(im.shape)
filters.sobel(im,0,imy)
#计算图像的梯度
magnitude=np.sqrt(imx**2+imy**2)
flt=figure()
gray()
flt.add_subplot(1,4,1)
imshow(im)
flt.add_subplot(1,4,2)
imshow(imx)
flt.add_subplot(1,4,3)
imshow(imy)
flt.add_subplot(1,4,4)
imshow(magnitude)

#高斯导数滤波器
im=np.array(Image.open('C:\\Users\\T\\Downloads\\5.jpg').convert('L'))
sigma=5
#计算x方向的导数
imx=np.zeros(im.shape)
filters.gaussian_filter(im,(sigma,sigma),(0,1),imx)
#计算y方向的导数
imy=np.zeros(im.shape)
filters.gaussian_filter(im,(sigma,sigma),(1,0),imy)
#计算图像的梯度
magnitude=np.sqrt(imx**2+imy**2)
flt=figure()
gray()
flt.add_subplot(1,4,1)
imshow(im)
flt.add_subplot(1,4,2)
imshow(imx)
flt.add_subplot(1,4,3)
imshow(imy)
flt.add_subplot(1,4,4)
imshow(magnitude)