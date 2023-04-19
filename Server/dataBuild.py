import cv2
import numpy as np
# https://blog.csdn.net/adhkcnbk/article/details/124250435
img = cv2.imread('demo.jpg')
noise = np.random.uniform(0, 256, img.shape[0:2])
value = 100
v = value * 0.01
noise[np.where(noise < (256 - v))] = 0
k = np.array([[0, 0.1, 0],
              [0.1, 8, 0.1],
              [0, 0.1, 0]])
noise = cv2.filter2D(noise, -1, k)
#获得仿射变化矩阵，由于对角阵自带45度的倾斜，所以减去了45度，三个参数分别表示：中心点的位置，旋转角度，等比例缩放
trans = cv2.getRotationMatrix2D((length/2, length/2), angle-45, 1-length/100.0)
#生成对角矩阵（雨线的长度）
dig = np.diag(np.ones(length))
#生成模糊核，通过对对角矩阵的仿射变换，得到模糊核，三个参数分别表示为：对角矩阵，仿射变换矩阵，输出的大小
k = cv2.warpAffine(dig, trans, (length, length))
k = cv2.GaussianBlur(k, (w, w), 0) #高斯模糊这个旋转后的对角核，使得雨有宽度，高斯矩阵为w*w， 0为方差
blurred = cv2.filter2D(noise, -1, k)
cv2.normalize(blurred, blurred, 0, 255, cv2.NORM_MINMAX)
blurred = np.array(blurred, dtype=np.uint8)
rain_result = img.copy()
rain_result[:, :, 0] = rain_result[:, :, 0] * (255 - rain[:, :, 0])/255.0 + beta*rain[:, :, 0]
rain_result[:, :, 1] = rain_result[:, :, 1] * (255 - rain[:, :, 0])/255.0 + beta*rain[:, :, 0]
rain_result[:, :, 2] = rain_result[:, :, 2] * (255 - rain[:, :, 0])/255.0 + beta*rain[:, :, 0]
