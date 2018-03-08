import sys
sys.path.insert(0,'C:\\Users\\T\\Desktop\\python\\计算机视觉\\图像基本操作和处理')

import imtool
from PIL import Image
import numpy as np
from matplotlib.pylab import *

#读取图片
im=np.array(Image.open('C:\\Users\\T\\Downloads\\1.jpg').convert('L'))

#直方图均衡化，可以使得照片的黑白对比更加明显
im2,cdf=imtool.histeq(im)
flt=figure()
flt.add_subplot(2,2,1)
hist(im.flatten(),bins=256)
flt.add_subplot(2,2,2)
hist(im2.flatten(),bins=256)
flt.add_subplot(2,2,3)
imshow(im)
flt.add_subplot(2,2,4)
imshow(im2)