import sys
sys.path.insert(0,'C:\\Users\\T\\Desktop\\python\\计算机视觉\\图像基本操作和处理')

from PIL import Image
import numpy as np
from matplotlib.pylab import *
import imtool
import os


#读取图像列表
path='C:\\Users\\T\\Downloads'
imlist=imtool.get_imlist(path)

#图像平均
avg_im=imtool.compute_average(imlist)
imshow(avg_im)
