import cv2
frame = cv2.imread("UnDerainImg/2023-04-16 16-59-20.jpg")
cv2.imshow("1", frame)
encoded, buffer = cv2.imencode('.jpg', frame)  # 把转换后的图像数据再次转换成流数据，
