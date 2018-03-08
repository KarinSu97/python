import sys
sys.path.insert(0,'C:\\Users\\T\\Desktop\\python\\计算机视觉\\局部图像描述子')
import harris
from PIL import Image
import numpy as np

#图像角点检测
im=np.array(Image.open('C:\\Users\\T\\Downloads\\5.jpg').convert('L'))
harrisim=harris.compute_harris_response(im)
filtered_coords=harris.get_harris_points(harrisim,10)
harris.plot_harris_points(im,filtered_coords)