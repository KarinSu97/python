import cv2
import numpy as np

#Sobel角点检测
img=cv2.imread('C:\\Users\\T\\Downloads\\14.jpg')
gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
gray=np.float32(gray)

#角点检测，第三个参数表示Sobel的中孔，一般介于3和31之间
dst=cv2.cornerHarris(gray,2,23,0.04)

#将角点标记为红色
img[dst>0.01*dst.max()]=[0,0,255]
cv2.imshow('img',img)
cv2.waitKey()
