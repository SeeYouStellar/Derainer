import numpy as np
import matplotlib.pyplot as plt

from skimage import data, img_as_float
from skimage.metrics import structural_similarity as ssim
from skimage.metrics import mean_squared_error




from skimage.measure import compare_ssim, compare_psnr, compare_mse
import cv2
maxpsnr = -1
minpsnr = 101
maxssim = -1
minssim = 101
avgpsnr = 0
avgssim = 0
psnr_ = []
ssim_ = []
for i in range(1):
    img1 = cv2.imread('903_1.jpg')
    img2 = cv2.imread('903_1.png')

    psnr = compare_psnr(img1, img2)
    ssim = compare_ssim(img1, img2, multichannel=True)  # 对于多通道图像(RGB、HSV等)关键词multichannel要设置为True
    psnr_.append(psnr)
    ssim_.append(ssim)
    # mse = compare_mse(img1, img2)
    # print('PSNR：{}，SSIM：{}'.format(psnr, ssim))
    # print(i+1)
    if maxpsnr < psnr:
        maxpsnr = psnr
    if minpsnr > psnr:
        minpsnr = psnr
    avgpsnr += psnr
    if maxssim < ssim:
        maxssim = ssim
    if minssim > ssim:
        minssim = ssim
    avgssim += ssim
avgpsnr /= 1
avgssim /= 1
print('maxpsnr:{},minpsnr:{},maxssim:{},minssim:{}'.format(maxpsnr, minpsnr, maxssim, minssim))
print('avgpsnr:{},avgssim:{}'.format(avgpsnr, avgssim))

fxssim = 0
fxpsnr = 0
for i in range(1):
    fxssim += (ssim_[i]-avgssim)*(ssim_[i]-avgssim)
    fxpsnr += (psnr_[i]-avgpsnr)*(psnr_[i]-avgpsnr)

fxpsnr /= 1
fxssim /= 1

print('fxpsnr:{},fxssim:{}'.format(fxpsnr, fxssim))

