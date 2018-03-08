from PIL import Image
import numpy as np
import os
from matplotlib.pylab import *

#获取图像文件列表
def get_imlist(path):
    return [os.path.join(path,f) for f in os.listdir(path) if f.endswith('.jpg')]

#图像缩放
def imresize(im,sz):
    pil_im=Image.fromarray(np.uint8(im))
    return np.array(pil_im.resize(sz))

#直方图均衡化
def histeq(im,nbr_bins=256):
    imhist,bins=histogram(im.flatten(),nbr_bins,normed=True)
    cdf=imhist.cumsum()
    cdf=255*cdf/cdf[-1]   #归一化
    im2=interp(im.flatten(),bins[:-1],cdf)
    return im2.reshape(im.shape),cdf

#图像平均
def compute_average(imlist):
    averageim=np.array(Image.open(imlist[0]),'f')
    im_len=1
    for imname in imlist[1:]:
        try:
            averageim+=np.array(Image.open(imname),'f')
            im_len+=1
        except:
            print(imname + '...skipped')
    averageim/=im_len
    return np.array(averageim,'uint8')
