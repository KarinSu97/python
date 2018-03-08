import cv2
import numpy as np

#定义人脸检测函数
def detect():
    face_cascade=cv2.CascadeClassifier('C:\\Users\\T\\Desktop\\haarcascade_frontalface_default.xml')
    eye_cascade=cv2.CascadeClassifier('C:\\Users\\T\\Desktop\\haarcascade_eye.xml')
    #打开摄像头
    camera=cv2.VideoCapture(0)
    cv2.namedWindow('camera')
    #进行人脸跟踪
    while True:
        #获取帧
        ret,frame=camera.read()
        gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        #检测人脸
        faces=face_cascade.detectMultiScale(gray,1.3,5)
        #绘制人脸框
        for (x,y,w,h) in faces:
            img=cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)
            #检测眼睛,设置对眼睛搜索的最小尺寸为40*40
            eyes=eye_cascade.detectMultiScale(gray,1.03,5,0,(40,40))
            for (ex,ey,ew,eh) in eyes:
                cv2.rectangle(img,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)
        cv2.imshow('camera',frame)
        if cv2.waitKey(1) & 0xFF==ord("q"):
            break
    camera.release()
    cv2.destroyAllWindows()

detect()