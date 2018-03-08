import cv2
import sys
import os
import numpy as np
import cv2.face
import pandas as pd

#生成人脸检测数据
def gerenate(people_name):
    face_cascade=cv2.CascadeClassifier('C:\\Users\\T\\Desktop\\haarcascade_frontalface_default.xml')
    eye_cascade=cv2.CascadeClassifier('C:\\Users\\T\\Desktop\\haarcascade_eye.xml')
    camera=cv2.VideoCapture(0)
    count=0
    while count<10:
        ret,frame=camera.read()
        gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        faces=face_cascade.detectMultiScale(gray,1.3,5)
        for (x,y,w,h) in faces:
            img=cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)
            #截取人脸，并控制图像大小为200*200
            f=cv2.resize(gray[y:y+h,x:x+w],(200,200))
            cv2.imwrite('./data/{0}_{1}.pgm'.format(people_name,str(count)),f)
            cv2.imshow('camera',frame)
            cv2.waitKey(100)
        count+=1
    camera.release()
    cv2.destroyAllWindows()

gerenate('linshizhe')

#定义人脸数据读取函数
def read_images(path,sz=None):
    filenames=os.listdir(path)
    X=[]
    Y=[]
    for filename in filenames:
        Y.append(filename[:-6])
        im=cv2.imread(os.path.join(path,filename),cv2.IMREAD_GRAYSCALE)
        #判断是否需要规范图像的大小
        if sz is not None:
            im=cv2.resize(im,(200,200))
        X.append(np.asarray(im,dtype=np.uint8))
    return X,Y

#基于LBPH的人脸识别
def face_rec(path):
    X,Y=read_images(path)
    name_list=pd.DataFrame()
    name_list['Y']=Y
    index=[]
    for i in range(len(set(Y))):
        index.extend(np.repeat(i,10))
    name_list['index']=index
    name_list=name_list.drop_duplicates()
    model=cv2.face.LBPHFaceRecognizer_create()
    model.train(np.asarray(X),np.asarray(index))
    camera=cv2.VideoCapture(0)
    face_cascade=cv2.CascadeClassifier('C:\\Users\\T\\Desktop\\haarcascade_frontalface_default.xml')
    while True:
        read,img=camera.read()
        faces=face_cascade.detectMultiScale(img,1.3,5)
        for (x,y,w,h) in faces:
            img=cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
            gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
            roi=gray[x:x+w,y:y+h]
            try:
                roi=cv2.resize(roi,(200,200),interpolation=cv2.INTER_LINEAR)
                params=model.predict(roi)
                cv2.putText(img,name_list['Y'][name_list['index']==params[0]][0],(x,y-20),cv2.FONT_HERSHEY_SIMPLEX,1,255,2)
            except:
                continue
        cv2.imshow("camera",img)
        if cv2.waitKey(1) & 0xFF==ord('q'):
            break
    camera.release()
    cv2.destroyAllWindows()

face_rec('./data')