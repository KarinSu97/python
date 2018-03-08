import cv2

filename='C:\\Users\\T\\Downloads\\13.jpg'

def dectect(filename):
    #这里的路径需要注意，中文下会识别不了文件，所以强行移到了桌面
    face_cascade=cv2.CascadeClassifier('C:\\Users\\T\\Desktop\\haarcascade_frontalface_default.xml')
    face_cascade.load('C:\\Users\\T\\Desktop\\haarcascade_frontalface_default.xml')
    img=cv2.imread(filename)
    gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    faces=face_cascade.detectMultiScale(gray,1.3,5)
    for (x,y,w,h) in faces:
        img=cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
    cv2.namedWindow('Vikings Detected!!')
    cv2.imshow('Vikings Detected!!',img)
    cv2.waitKey(0)

dectect(filename)

