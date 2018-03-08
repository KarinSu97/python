import cv2
import numpy as np

#打开摄像头
cap=cv2.VideoCapture(0)

#创建一个BackgroundSubtractor类
mog=cv2.createBackgroundSubtractorMOG2()
while True:
    ret,frame=cap.read()
    fgmask=mog.apply(frame)
    cv2.imshow('frame',fgmask)
    if cv2.waitKey(1) & 0xff==ord('q'):
        break
cap.release()
cv2.destroyAllWindows()