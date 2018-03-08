import cv2
import numpy as np

'''直线检测'''
img=cv2.imread('C:\\Users\\T\\Downloads\\9.jpg')
gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
edges=cv2.Canny(gray,50,120)
minLineLength=20   #设置最小直线长度
maxLineGap=5   #设置最大线段间隙
lines=cv2.HoughLinesP(edges,1,np.pi/180,100,minLineLength,maxLineGap)
for line in lines:
    for x1,y1,x2,y2 in line:
        cv2.line(img,(x1,y1),(x2,y2),(0,255,0),2)

cv2.imshow('edges',edges)
cv2.imshow('img',img)
cv2.waitKey()

'''圆形检测'''
planets=cv2.imread('C:\\Users\\T\\Downloads\\4.jpg')
gray_img=cv2.cvtColor(planets,cv2.COLOR_BGR2GRAY)
img=cv2.medianBlur(gray_img,5)
cimg=cv2.cvtColor(img,cv2.COLOR_GRAY2BGR)

circles=cv2.HoughCircles(img,cv2.HOUGH_GRADIENT,1,120,param1=100,param2=50,minRadius=0,maxRadius=0)
circles=np.uint16(np.around(circles))

for i in circles[0,:]:
    #绘制圆形
    cv2.circle(planets,(i[0],i[1]),i[2],(0,255,0),2)
    #绘制中心
    cv2.circle(planets,(i[0],i[1]),2,(0,0,255),3)

cv2.imshow('circles',planets)
cv2.waitKey()