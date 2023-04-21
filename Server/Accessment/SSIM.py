import numpy as np
import matplotlib.pyplot as plt

from skimage import data, img_as_float
from skimage.metrics import structural_similarity as ssim
from skimage.metrics import mean_squared_error




from skimage.measure import compare_ssim, compare_psnr, compare_mse
import cv2

img1 = cv2.imread('../DerainedImg/2023-04-19 22-03-20.jpg')
img2 = cv2.imread('../UnDerainImg/2023-04-19 22-03-20.jpg')

psnr = compare_psnr(img1, img2)
ssim = compare_ssim(img1, img2, multichannel=True)  # 对于多通道图像(RGB、HSV等)关键词multichannel要设置为True
mse = compare_mse(img1, img2)

print('PSNR：{}，SSIM：{}，MSE：{}'.format(psnr, ssim, mse))