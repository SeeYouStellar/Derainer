import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt
img1 = cv.imread('Demo2/4.jpg')
# img2 = cv.imread('Demo2/demo_base.jpg')
# img3 = cv.imread('Demo2/neg.jpg')
# img4 = cv.imread('Demo2/demo_output.png')
# # # img_rainy = cv.imread('demo_output.png')
# # img_neg = cv.subtract(img1, img2)
# # cv.imshow("img_neg", img_neg)
# # cv.waitKey(0)
# # cv.imwrite("demo/00001_neg.jpg", img_neg)
#
img2 = cv.imread('Demo2/4.jpg')
plt.figure(figsize=(11,5))
plt.subplot(1, 2, 1)
plt.imshow(img2)



plt.subplot(1, 2, 2)
plt.title("Color Histogram")
hist_b = cv.calcHist([img2], [0], None, [256], [0, 256])
print(hist_b.shape)
hist_g = cv.calcHist([img2], [1], None, [256], [0, 256])
hist_r = cv.calcHist([img2], [2], None, [256], [0, 256])
hist_all = np.empty([256, 1], dtype=int)
for i in range(256):
    hist_all[i] = (hist_r[i]+hist_g[i]+hist_b[i])/3
# b, = plt.plot(hist_b, color='b')
# g, = plt.plot(hist_g, color='g')
# r, = plt.plot(hist_r, color='r')
all, = plt.plot(hist_all, color='cornflowerblue')

# plt.legend(loc="upper right", handles=[b, g, r], labels=['b channel', 'g channel', 'r channel'])
plt.legend(loc="upper right", handles=[all], labels=['all channel'])
plt.xlabel("Pixel Color Value")
plt.ylabel("Pixel Count")
plt.show()

#
# plt.subplot(2, 2, 1)
# plt.title("input")
# plt.imshow(img1)
#
# plt.subplot(2, 2, 2)
# plt.title("base")
# plt.imshow(img2)
#
# plt.subplot(2, 2, 3)
# plt.title("detail")
# plt.imshow(img3)
#
# plt.subplot(2, 2, 4)
# plt.title("output")
# plt.imshow(img4)
# plt.show()