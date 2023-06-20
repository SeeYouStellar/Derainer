import os

import numpy as np
import matplotlib.pyplot as plt

from skimage import data, img_as_float
from skimage.metrics import structural_similarity as ssim
from skimage.metrics import mean_squared_error

# 人像类36，场景类51，动物类13


from skimage.measure import compare_ssim, compare_psnr, compare_mse
import cv2
# maxpsnr = -1
# minpsnr = 101
# maxssim = -1
# minssim = 101
# avgpsnr = 0
# avgssim = 0
# psnr_ = []
# ssim_ = []
# filename = os.listdir("../Dataset_Rain14000_test/ground_truth_animal_/")
# for i in range(len(filename)):
#     # print(filename[i])
#     img1 = cv2.imread('../Dataset_Rain14000_test/ground_truth_animal_/' + filename[i])
#
#     img2 = cv2.imread('../Dataset_Rain14000_test/animal_result_2/'+filename[i][:-4]+".png")
#
#     psnr = compare_psnr(img1, img2)
#     ssim = compare_ssim(img1, img2, multichannel=True)  # 对于多通道图像(RGB、HSV等)关键词multichannel要设置为True
#     psnr_.append(psnr)
#     ssim_.append(ssim)
#     # mse = compare_mse(img1, img2)
#     # print('PSNR：{}，SSIM：{}'.format(psnr, ssim))
#     if maxpsnr < psnr:
#         maxpsnr = psnr
#     if minpsnr > psnr:
#         minpsnr = psnr
#     avgpsnr += psnr
#     if maxssim < ssim:
#         maxssim = ssim
#     if minssim > ssim:
#         minssim = ssim
#     avgssim += ssim
# avgpsnr /= len(filename)
# avgssim /= len(filename)
# print('maxpsnr:{},minpsnr:{},maxssim:{},minssim:{}'.format(maxpsnr, minpsnr, maxssim, minssim))
# print('avgpsnr:{},avgssim:{}'.format(avgpsnr, avgssim))
#
# fxssim = 0
# fxpsnr = 0
# for i in range(len(filename)):
#     fxssim += (ssim_[i]-avgssim)*(ssim_[i]-avgssim)
#     fxpsnr += (psnr_[i]-avgpsnr)*(psnr_[i]-avgpsnr)
#
# fxpsnr /= len(filename)
# fxssim /= len(filename)
#
# print('fxpsnr:{},fxssim:{}'.format(fxpsnr, fxssim))
#
#
#
# plt.title("animal SSIM")
# plt.plot(ssim_, color='cornflowerblue')
# plt.xlabel("image id")
# plt.ylabel("SSIM value")
# plt.show()
#
#
#
# maxpsnr = -1
# minpsnr = 101
# maxssim = -1
# minssim = 101
# avgpsnr = 0
# avgssim = 0
# psnr_ = []
# ssim_ = []
# filename = os.listdir("../Dataset_Rain14000_test/ground_truth_people_/")
# for i in range(len(filename)):
#     img1 = cv2.imread('../Dataset_Rain14000_test/ground_truth_people_/' + filename[i])
#
#     img2 = cv2.imread('../Dataset_Rain14000_test/people_result_2/'+filename[i][:-4]+".png")
#
#     psnr = compare_psnr(img1, img2)
#     ssim = compare_ssim(img1, img2, multichannel=True)  # 对于多通道图像(RGB、HSV等)关键词multichannel要设置为True
#     psnr_.append(psnr)
#     ssim_.append(ssim)
#     # mse = compare_mse(img1, img2)
#     # print('PSNR：{}，SSIM：{}'.format(psnr, ssim))
#     if maxpsnr < psnr:
#         maxpsnr = psnr
#     if minpsnr > psnr:
#         minpsnr = psnr
#     avgpsnr += psnr
#     if maxssim < ssim:
#         maxssim = ssim
#     if minssim > ssim:
#         minssim = ssim
#     avgssim += ssim
# avgpsnr /= len(filename)
# avgssim /= len(filename)
# print('maxpsnr:{},minpsnr:{},maxssim:{},minssim:{}'.format(maxpsnr, minpsnr, maxssim, minssim))
# print('avgpsnr:{},avgssim:{}'.format(avgpsnr, avgssim))
#
# fxssim = 0
# fxpsnr = 0
# for i in range(len(filename)):
#     fxssim += (ssim_[i]-avgssim)*(ssim_[i]-avgssim)
#     fxpsnr += (psnr_[i]-avgpsnr)*(psnr_[i]-avgpsnr)
#
# fxpsnr /= len(filename)
# fxssim /= len(filename)
#
# print('fxpsnr:{},fxssim:{}'.format(fxpsnr, fxssim))
#
# plt.title("people SSIM")
# plt.plot(ssim_, color='cornflowerblue')
# plt.xlabel("image id")
# plt.ylabel("SSIM value")
# plt.show()
#

maxpsnr = -1
minpsnr = 101
maxssim = -1
minssim = 101
avgpsnr = 0
avgssim = 0
psnr_ = []
ssim_ = []
filename = os.listdir("../Dataset_Rain14000_test/ground_truth_scence_/")
for i in range(len(filename)):
    img1 = cv2.imread('../Dataset_Rain14000_test/ground_truth_scence_/' + filename[i])

    img2 = cv2.imread('../Dataset_Rain14000_test/scence_result_2/'+filename[i][:-4]+".png")

    psnr = compare_psnr(img1, img2)
    ssim = compare_ssim(img1, img2, multichannel=True)  # 对于多通道图像(RGB、HSV等)关键词multichannel要设置为True
    psnr_.append(psnr)
    ssim_.append(ssim)
    # mse = compare_mse(img1, img2)
    # print('PSNR：{}，SSIM：{}'.format(psnr, ssim))
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
avgpsnr /= len(filename)
avgssim /= len(filename)
print('maxpsnr:{},minpsnr:{},maxssim:{},minssim:{}'.format(maxpsnr, minpsnr, maxssim, minssim))
print('avgpsnr:{},avgssim:{}'.format(avgpsnr, avgssim))

fxssim = 0
fxpsnr = 0
for i in range(len(filename)):
    fxssim += (ssim_[i]-avgssim)*(ssim_[i]-avgssim)
    fxpsnr += (psnr_[i]-avgpsnr)*(psnr_[i]-avgpsnr)

fxpsnr /= len(filename)
fxssim /= len(filename)

print('fxpsnr:{},fxssim:{}'.format(fxpsnr, fxssim))

plt.title("scence SSIM")
plt.plot(ssim_, color='cornflowerblue')
plt.xlabel("image id")
plt.ylabel("SSIM value")
plt.show()
