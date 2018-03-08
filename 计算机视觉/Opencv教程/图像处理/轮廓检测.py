import cv2
import numpy as np

#读取照片,并执行二值化操作
img=cv2.pyrDown(cv2.imread('C:\\Users\\T\\Downloads\\8.jpg',cv2.IMREAD_UNCHANGED))
ret,thresh=cv2.threshold(cv2.cvtColor(img.copy(),cv2.COLOR_BGR2GRAY),127,255,cv2.THRESH_BINARY)
image,contours,hier=cv2.findContours(thresh,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

#轮廓检测
for c in contours:
    #计算简单的边界框
    x,y,w,h=cv2.boundingRect(c)
    cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)   #绘制矩形框

    #计算最小边界框
    rect=cv2.minAreaRect(c)
    box=cv2.boxPoints(rect)
    box=np.int0(box)
    cv2.drawContours(img,[box],0,(0,0,255),3)   #绘制矩形框

    #计算最小闭圆
    (x,y),radius=cv2.minEnclosingCircle(c)
    center=(int(x),int(y))
    radius=int(radius)
    img=cv2.circle(img,center,radius,(0,255,0),2)

cv2.drawContours(img,contours,-1,(255,0,0),1)
cv2.imshow('contours',img)
cv2.waitKey()