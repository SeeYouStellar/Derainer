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
for i in range(100):
    s = ''
    if i+1 < 10:
        s = '0000'
    elif i+1 == 100:
        s = '00'
    else :
        s = '000'
    img1 = cv2.imread('../Dataset_TrafficDataset_test/ground_truth/'+s+str(i+1)+'.jpg')
    img2 = cv2.imread('../Dataset_TrafficDataset_test/angle6_result/'+s+str(i+1)+'.png')

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
avgpsnr /= 100
avgssim /= 100
print('maxpsnr:{},minpsnr:{},maxssim:{},minssim:{}'.format(maxpsnr, minpsnr, maxssim, minssim))
print('avgpsnr:{},avgssim:{}'.format(avgpsnr, avgssim))

fxssim = 0
fxpsnr = 0
for i in range(100):
    fxssim += (ssim_[i]-avgssim)*(ssim_[i]-avgssim)
    fxpsnr += (psnr_[i]-avgpsnr)*(psnr_[i]-avgpsnr)

fxpsnr /= 100
fxssim /= 100

print('fxpsnr:{},fxssim:{}'.format(fxpsnr, fxssim))




maxpsnr = -1
minpsnr = 101
maxssim = -1
minssim = 101
avgpsnr = 0
avgssim = 0
psnr_ = []
ssim__ = []
for i in range(100):
    s = ''
    if i+1 < 10:
        s = '0000'
    elif i+1 == 100:
        s = '00'
    else :
        s = '000'
    img1 = cv2.imread('../Dataset_TrafficDataset_test/ground_truth/'+s+str(i+1)+'.jpg')
    img2 = cv2.imread('../Dataset_TrafficDataset_test/angle6_plus_result/'+s+str(i+1)+'.png')

    psnr = compare_psnr(img1, img2)
    ssim = compare_ssim(img1, img2, multichannel=True)  # 对于多通道图像(RGB、HSV等)关键词multichannel要设置为True
    psnr_.append(psnr)
    ssim__.append(ssim)
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
avgpsnr /= 100
avgssim /= 100
print('maxpsnr:{},minpsnr:{},maxssim:{},minssim:{}'.format(maxpsnr, minpsnr, maxssim, minssim))
print('avgpsnr:{},avgssim:{}'.format(avgpsnr, avgssim))

fxssim = 0
fxpsnr = 0
for i in range(100):
    fxssim += (ssim__[i]-avgssim)*(ssim__[i]-avgssim)
    fxpsnr += (psnr_[i]-avgpsnr)*(psnr_[i]-avgpsnr)

fxpsnr /= 100
fxssim /= 100

print('fxpsnr:{},fxssim:{}'.format(fxpsnr, fxssim))


plt.figure(figsize=(11,5))
plt.subplot(1, 2, 1)
plt.title("70° drizzle streaks SSIM")
plt.plot(ssim_, color='cornflowerblue')
plt.xlabel("image id")
plt.ylabel("SSIM value")
# plt.show()

plt.subplot(1, 2, 2)
plt.title("70° wide streaks SSIM")
plt.plot(ssim__, color='cornflowerblue')
plt.xlabel("image id")
plt.ylabel("SSIM value")
plt.show()