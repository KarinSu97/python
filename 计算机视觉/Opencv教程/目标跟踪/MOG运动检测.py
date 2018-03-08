import cv2
import numpy as np

#打开摄像头
camera=cv2.VideoCapture(0)

es=cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(9,4))
kernel=np.ones((5,5),np.uint8)
background=None

while True:
    ret,frame=camera.read()
    #将第一帧赋给背景,并进行模糊操作，以减少因为震动带来的影响
    if background is None:
        background=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        background=cv2.GaussianBlur(background,(21,21),0)
        continue
    #将获取的帧也做同样的处理
    gray_frame=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    gray_frame=cv2.GaussianBlur(gray_frame,(21,21),0)
    #计算获取到的图像与背景图像的差异
    diff=cv2.absdiff(background,gray_frame)
    #进行二值化处理
    diff=cv2.threshold(diff,25,255,cv2.THRESH_BINARY)[1]
    #进行膨胀操作
    diff=cv2.dilate(diff,es,iterations=2)
    #寻找物体的轮廓
    image,cnts,hierarchy=cv2.findContours(diff.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    #标记矩形框
    for c in cnts:
        if cv2.contourArea(c)<1500:
            continue
        (x,y,w,h)=cv2.boundingRect(c)
        cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)
        cv2.imshow('frame',frame)
        if cv2.waitKey(1) & 0xFF==ord('q'):
            break

cv2.destroyAllWindows()
camera.release()

