import time

import cv2
import numpy as np
import zmq
import base64
import threading

mutex = threading.Lock()
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

mutex_flag = threading.Lock()
flag = 0
def SendFrame():
    # init camera
    # fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    # vw = cv2.VideoWriter('output.mp4', fourcc, 20, (640, 480))

    # port 5555
    IP = '172.20.10.5'
    contest = zmq.Context()
    socket_send = contest.socket(zmq.PAIR)
    socket_send.connect('tcp://%s:5555' % IP)
    while True:
        mutex_flag.acquire()
        if flag == 0:
            mutex_flag.release()
            time.sleep(1)
            continue
        elif flag == 1:
            mutex_flag.release()
        else:
            mutex_flag.release()
            mutex.acquire()
            cap.release()
            cv2.destroyAllWindows()
            mutex.release()
            break
        mutex.acquire()
        if cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                print('can not recive frame!')
                break
            # vw.write(frame)
            # cv2.imshow('frame', frame)
            encoded, buffer = cv2.imencode('.jpg', frame)  # 把转换后的图像数据再次转换成流数据，
            # 并且把流数据储存到内存buffer中
            jpg_buffer = base64.b64encode(buffer)  # 把内存中的图像流数据进行base64编码
            socket_send.send(jpg_buffer)  # 把编码后的流数据发送给视频的接收端
            if cv2.waitKey(1) == ord('q'):
                break
        else:
            # 在关闭摄像头后可能会还会需要重启摄像头（flag 2->1），那么就会进入这个分支，只需要重新获取摄像头
            cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        mutex.release()
    cap.release()
    cv2.destroyAllWindows()
    print("cap is close")

def StopSendFrame():
    contest = zmq.Context()
    socket_listen = contest.socket(zmq.PAIR)
    socket_listen.bind('tcp://%s:5556')

    while True:
        msg = socket_listen.recv()
        mutex_flag.acquire()
        if msg == '1': #开启摄像头，开始传帧
            flag = 1
        elif msg == '0': #暂停传帧
            flag = 0
        else:           #关闭摄像头
            flag = 2
        mutex_flag.release()
        time.sleep(1)

if __name__ == "__main__":
    t1 = threading.Thread(target=SendFrame)
    t2 = threading.Thread(target=StopSendFrame)
    t1.start()
    t2.start()
    t1.join()
    t2.join()