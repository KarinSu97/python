from PIL import Image
import pytesseract

#打开图像
im=Image.open('C:\\Users\\T\\Downloads\\1.jpg')
text=pytesseract.image_to_string(im,lang='chi_sim')
print(text)