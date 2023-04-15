# from time import strftime, localtime
# timelog = strftime('%Y-%m-%d %H:%M:%S',localtime())
# print(type(timelog))
# print(type(str(1)))
#
# a = 0
#
# def func():
#     global a
#     a = 2
#     print("func:"+str(a))
#     if a == 2:
#         a = 4
#
# print(a)
# func()
# print(a)
import time

# import cv2
# from time import strftime, localtime
# cap = cv2.VideoCapture(0)
# print(cap.isOpened())
#
# i = 0
# while True:
#     ret, frame = cap.read()
#     cv2.imshow("1", frame)
#     timelog = strftime('%Y-%m-%d %H-%M-%S', localtime())
#     print("save a frame at "+timelog+"\n")
#     if i == 0:
#         i = 1
#         cv2.imwrite("D:/img/"+timelog+".jpg", frame)
#     if cv2.waitKey(1) == ord('q'):
#         break
#
# cap.release()
# cv2.destroyAllWindows()

import os
path = 'DerainedImg'  # 输入文件夹地址
os.system("rmdir /s/q "+path)
