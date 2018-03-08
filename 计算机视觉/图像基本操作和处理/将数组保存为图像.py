from PIL import Image
import numpy as np
from scipy.misc import imsave

#保存数组为图片
im=np.array(Image.open('C:\\Users\\T\\Downloads\\5.jpg').convert('L'))
imsave('C:\\Users\\T\\Downloads\\6.jpg',im)