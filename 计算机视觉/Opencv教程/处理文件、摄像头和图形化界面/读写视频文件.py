import cv2

#读取视频文件
videoCapture=cv2.VideoCapture('C:\\Users\\T\\Desktop\\新视频_中.mp4')

#定义写出函数
fps=videoCapture.get(cv2.CAP_PROP_FPS)   #帧速率
size=(int(videoCapture.get(cv2.CAP_PROP_FRAME_WIDTH)),int(videoCapture.get(cv2.CAP_PROP_FRAME_HEIGHT)))   #帧大小
#cv2.VideoWriter_fourcc表示变编码器，常用的有：
#cv2.VideoWriter_fourcc('I','4','2','0')：表示一个未压缩的YUV颜色编码，是4:2:0色度子采样，文件拓展名为.avi
#cv2.VideoWriter_fourcc('P','I','M','1')：表示MPEG-1编码类型，文件拓展名为.avi
#cv2.VideoWriter_fourcc('X','V','I','D')：表示MPEG-4编码类型,可以得到大小为平均值的视频，文件拓展名为.avi
#cv2.VideoWriter_fourcc('T','H','E','O')：表示Ogg Vorbis,文件拓展名为.ogv
#cv2.VideoWriter_fourcc('F','L','V','1')：表示FLASH视频，文件拓展名为.flv
videoWriter=cv2.VideoWriter('C:\\Users\\T\\Desktop\\1.avi',cv2.VideoWriter_fourcc('I','4','2','0'),fps,size)

#通过read函数获取新的帧,frame其实就是获取到的图像
success,frame=videoCapture.read()

#通过write函数将获取的帧加到videoWriter指定的文件中
while success:
    videoWriter.write(frame)
    success, frame = videoCapture.read()