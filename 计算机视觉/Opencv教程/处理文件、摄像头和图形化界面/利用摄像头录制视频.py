import cv2

#定义读取函数
cameraCapture=cv2.VideoCapture(0)

#定义写出函数，这里只录制10秒
fps=30
size=(int(cameraCapture.get(cv2.CAP_PROP_FRAME_WIDTH)),int(cameraCapture.get(cv2.CAP_PROP_FRAME_HEIGHT)))
videoWriter=cv2.VideoWriter('C:\\Users\\T\\Desktop\\2.avi',cv2.VideoWriter_fourcc('I','4','2','0'),fps,size)

#开始录制
numFramesRemaining=10*fps-1
success,frame=cameraCapture.read()
while success and numFramesRemaining>0:
    videoWriter.write(frame)
    success, frame = cameraCapture.read()
    numFramesRemaining-=1
cameraCapture.release()

#当有多个摄像头时
success0=cameraCapture0.grab()
success1=cameraCapture1.grab()
while success0 and success1:
    frame0=cameraCapture0.retrieve()
    frame1=cameraCapture1.retrieve()

#实时显示摄像头获取的帧
#定义鼠标操作函数，这里双击则关闭显示
clicked=False
def onmouse(event,x,y,flags,param):
    global clicked
    if event==cv2.EVENT_LBUTTONDBLCLK:
        clicked=True

cameraCapture=cv2.VideoCapture(0)
fps=30
size=(int(cameraCapture.get(cv2.CAP_PROP_FRAME_WIDTH)),int(cameraCapture.get(cv2.CAP_PROP_FRAME_HEIGHT)))
videoWriter=cv2.VideoWriter('C:\\Users\\T\\Desktop\\2.avi',cv2.VideoWriter_fourcc('I','4','2','0'),fps,size)

cv2.namedWindow('MyWindow')
cv2.setMouseCallback("MyWindow",onmouse)   #获取鼠标操作
success,frame=cameraCapture.read()
while success and cv2.waitKey(1)==-1 and not clicked:
    #waitKey表示获取键盘的输入状态，当没有按下任何操作时，返回为-1，也可以利用ord函数，比如ord('ESC')表示按下ESC键
    cv2.imshow('MyWindow',frame)
    videoWriter.write(frame)
    success, frame = cameraCapture.read()

cv2.destroyWindow("MyWindow")
cameraCapture.release()
