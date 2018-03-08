from PIL import Image
import numpy as np
from scipy.ndimage import filters
from matplotlib.pylab import *


#对图像进行模糊操作，即采用高斯核进行卷积，这里5表示卷积核的方差，方差越大，图像越模糊
im=np.array(Image.open('C:\\Users\\T\\Downloads\\3.jpg').convert('L'))
im2=filters.gaussian_filter(im,5)
im2=np.uint8(im2)
imshow(im2)

#对彩色图像进行模糊操作
im=np.array(Image.open('C:\\Users\\T\\Downloads\\5.jpg'))
im2=np.zeros(im.shape)
for i in range(3):
    im2[:,:,i]=filters.gaussian_filter(im[:,:,i],1)
im2=np.uint8(im2)
imshow(im2)