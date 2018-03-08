import numpy as np
import cv2
from matplotlib import pyplot as plt

#加载图像
img=cv2.imread('C:\\Users\\T\\Downloads\\10.jpg')

#创建一个空图像
mask=np.zeros(img.shape[:2],np.uint8)

#创建前景模型和背景模型
bgdModel=np.zeros((1,65),np.float64)
fgdModel=np.zeros((1,65),np.float64)

#初始化矩形区域
rect=(155,20,390,260)

#进行GrabCut算法
cv2.grabCut(img,mask,rect,bgdModel,fgdModel,10,cv2.GC_INIT_WITH_RECT)
mask2=np.where((mask==2)|(mask==0),0,1).astype('uint8')
img=img*mask2[:,:,np.newaxis]

#展示图像
cv2.imshow('img',img)
cv2.waitKey()
