from PIL import Image
import matplotlib.pyplot as pyl
import os

#读取图片
pil_img=Image.open('C:\\Users\\T\\Downloads\\1.jpg')
pyl.imshow(pil_img)
pyl.axis('off')   #不显示坐标轴

#将图片转化为灰度图像
grey_img=pil_img.convert('L')
pyl.imshow(grey_img)

#保存图片
grey_img.save('C:\\Users\\T\\Downloads\\2.jpg')

#创建缩略图,这里生成128*128的缩略图
pil_img.thumbnail((128,128))
pil_img.save('C:\\Users\\T\\Downloads\\3.jpg')

#裁剪指定区域
box=[0,200,200,700]
region=pil_img.crop(box)
pyl.imshow(region)

#粘贴截取的图像
region=region.transpose(Image.ROTATE_180)
pil_img.paste(region,[278,200,478,700])

#调整图像的尺寸
resize_img=pil_img.resize((128,128))
resize_img.save('C:\\Users\\T\\Downloads\\4.jpg')

#图片翻转
roat_img=pil_img.rotate(180)
roat_img.save('C:\\Users\\T\\Downloads\\5.jpg')

