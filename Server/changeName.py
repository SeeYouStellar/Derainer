import cv2
import numpy as np
import os
files = os.listdir("D:/SPAC-SupplementaryMaterials/Dataset_Testing_Synthetic/b2_GT")
index = 299
# for i in range(len(files)):
#     # print(files[i])
#     img = cv2.imread("D:/SPAC-SupplementaryMaterials/Dataset_Testing_Synthetic/b2_GT/"+files[i])
#     # print(img)
#     # cv2.imshow("1", img)
#     # print(".\\TrainData\\label\\"+str(index)+".jpg")
#     cv2.imwrite("C:/Users/lisherry/OneDrive/桌面/文献/code/Server/Network/TrainData/label/"+str(index)+".jpg", img)
#     index = index + 1

img = cv2.imread("D:/SPAC-SupplementaryMaterials/Dataset_Testing_Synthetic/b2_GT/"+files[0])
cv2.imshow("1", img)
cv2.imwrite("C:\\Users\\lisherry\\OneDrive\\桌面\\文献\\code\\Server\\Network\\TrainData\\label\\"+str(index)+".jpg", img)
img = cv2.imread("C:/Users/lisherry/OneDrive/桌面/文献/code/Server/Network/TrainData/label/299.jpg")
cv2.imshow("1", img)
cv2.destroyAllWindows()
