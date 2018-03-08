import cv2

bs=cv2.createBackgroundSubtractorKNN(detectShadows=True)
camera=cv2.VideoCapture('C:/Users/T/Downloads/1.avi')
while True:
    ret,frame=camera.read()
    fgmask=bs.apply(frame)
    th=cv2.threshold(fgmask.copy(),244,255,cv2.THRESH_BINARY)[1]
    dilated=cv2.dilate(th,cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(3,3)),iterations=2)
    image,cnts,hier=cv2.findContours(dilated,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    for c in cnts:
        if cv2.contourArea(c)>1600:
            (x,y,w,h)=cv2.boundingRect(c)
            cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,255),2)
    cv2.imshow('frame',frame)
    if cv2.waitKey(1) & 0xff==ord('q'):
        break
camera.release()
cv2.destroyAllWindows()
