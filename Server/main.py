import time

import cv2
import numpy as np
import zmq
import base64
import threading
from time import strftime, localtime

mutex_flag = threading.Lock()
flag = 0

def SendThread():
    # init camera
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    # fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    # vw = cv2.VideoWriter('output.mp4', fourcc, 20, (640, 480))
    print("thread1 is start")
    # port 5555
    IP = '172.20.10.5'
    contest = zmq.Context()
    socket_send = contest.socket(zmq.PAIR)
    socket_send.connect('tcp://%s:5555' % IP)
    makephoto = False
    global flag
    while True:
        mutex_flag.acquire()
        # print(str(flag))
        if flag == 0:
            mutex_flag.release()
            time.sleep(1)
            continue
        elif flag == 1:
            mutex_flag.release()
        elif flag == 2:
            mutex_flag.release()
            cap.release()
            cv2.destroyAllWindows()
            break
        elif flag == 3:
            mutex_flag.release()
            makephoto = True
        if cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                print('can not recive frame!')
                break
            # vw.write(frame)
            # cv2.imshow('frame', frame)
            encoded, buffer = cv2.imencode('.jpg', frame)  # 把转换后的图像数据再次转换成流数据，
            jpg_buffer = base64.b64encode(buffer)  # 把内存中的图像流数据进行base64编码
            socket_send.send(jpg_buffer)  # 把编码后的流数据发送给视频的接收端
            msg = socket_send.recv_string()
            if makephoto:
                timelog = strftime('%Y-%m-%d %H:%M:%S', localtime())
                cv2.imwrite(timelog+'.jpg', frame)
            if cv2.waitKey(1) == ord('q'):
                break
        else:
            # 在关闭摄像头后可能会还会需要重启摄像头（flag 2->1），那么就会进入这个分支，只需要重新获取摄像头
            cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    cap.release()
    cv2.destroyAllWindows()
    print("cap is close")

def ListenThread():
    print("thread2 is start")
    contest = zmq.Context()
    socket_listen = contest.socket(zmq.PAIR)
    socket_listen.bind('tcp://*:5556')
    global flag
    while True:
        # try:
        msg = socket_listen.recv_string()
        socket_listen.send_string("receive flag")
        # except zmq.ZMQError:
        #     print("zmq.ZMQError")
        #     time.sleep(1)
        #     continue
        # else:
        # print(msg)
        mutex_flag.acquire()

        if msg == "1":  # 开启摄像头，开始传帧
            flag = 1
        elif msg == "0":  # 暂停传帧
            flag = 0
        elif msg == "2":  # 关闭摄像头
            flag = 2
        elif msg == "3":
            flag = 3
        mutex_flag.release()
        time.sleep(1)

if __name__ == "__main__":
    t1 = threading.Thread(target=SendThread)
    t2 = threading.Thread(target=ListenThread)
    t1.start()
    t2.start()
    t1.join()
    t2.join()