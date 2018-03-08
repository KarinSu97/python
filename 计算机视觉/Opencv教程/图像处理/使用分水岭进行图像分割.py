import numpy as np
import cv2
from matplotlib import pyplot as plt

#加载图像
img=cv2.imread('C:\\Users\\T\\Downloads\\10.jpg')
gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

#对图像进行二值化操作
ret,thresh=cv2.threshold(gray,0,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)

#去除噪声数据
kernel=np.ones((3,3),np.uint8)
opening=cv2.morphologyEx(thresh,cv2.MORPH_OPEN,kernel,iterations=2)

#进行膨胀操作，可以得到大部分都是背景的区域
sure_bg=cv2.dilate(opening,kernel,iterations=3)

#确定前景区域
dist_transform=cv2.distanceTransform(opening,cv2.DIST_L2,5)
ret,sure_fg=cv2.threshold(dist_transform,0.7*dist_transform.max(),255,0)

#标记前景区域和背景区域中重合的区域
sure_fg=np.uint8(sure_fg)
unknown=cv2.subtract(sure_bg,sure_fg)

#设定栅栏
ret,markers=cv2.connectedComponents(sure_fg)

#给背景区域加上1
markers+=1
markers[unknown==255]=0

#将栅栏打开，并绘制成红色
markers=cv2.watershed(img,markers)
img[markers==-1]=[255,0,0]
plt.imshow(img)