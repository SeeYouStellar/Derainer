# port 5555:send-receive cap frame
# port 5556:send-receive flag
# port 5557:send-receive UnDerain Img
# port 5558:send-receive Derain Img

import os
import time

import cv2
import numpy as np
import zmq
import base64
import threading
from time import strftime, localtime
from queue import Queue

mutex_flag = threading.Lock()
flag = 0
filename = Queue()  # 线程安全，不用加锁
filename_deran = Queue()
def SendThread():
    # init camera
    # cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    # fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    # vw = cv2.VideoWriter('output.mp4', fourcc, 20, (640, 480))
    VideoPath = 'C:/Users/lisherry/Desktop/Server/video/'
    # VideoPath = './video/'
    print("SendThread is start")
    # port 5555
    # IP = '172.20.10.5'
    IP = '10.136.5.141'
    contest = zmq.Context()
    socket_send = contest.socket(zmq.PAIR)
    socket_send.connect('tcp://%s:6555' % IP)
    # socket_send.connect('tcp://*:5555')
    print("connect socket 5555 build\n")
    makephoto = False
    global flag
    index = 1
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
            # cap.release()
            cv2.destroyAllWindows()
            break
        elif flag == 3:
            flag = 1
            mutex_flag.release()
            makephoto = True
        # ret, frame = cap.read
        framename = ''
        if int(index / 10000) == 0:
            framename += '0'
        if int(index / 1000) == 0:
            framename += '0'
        if int(index / 100) == 0:
            framename += '0'
        if int(index / 10) == 0:
            framename += '0'
        framename += str(index)
        JPG = '.jpg'
        print(VideoPath+framename+JPG)
        frame = cv2.imread(VideoPath+framename+JPG)
        index += 1
        # if not ret:
        #     print('can not recive frame!')
        #     break
        # vw.write(frame)
        # cv2.imshow('frame', frame)
        encoded, buffer = cv2.imencode('.jpg', frame)  # 把转换后的图像数据再次转换成流数据，
        jpg_buffer = base64.b64encode(buffer)  # 把内存中的图像流数据进行base64编码
        socket_send.send(jpg_buffer)  # 把编码后的流数据发送给视频的接收端
        msg = socket_send.recv_string()
        if makephoto:
            # timelog = strftime('%Y-%m-%d %H-%M-%S', localtime())
            filename.put(framename)
            print("save a frame at "+VideoPath+framename+JPG+"\n")
            cv2.imwrite("./UnDerainImg/"+framename+JPG, frame)
            makephoto = False
        if cv2.waitKey(1) == ord('q'):
            break

    # cap.release()
    # cv2.destroyAllWindows()
    print("cap close")
    print("SendThread dead")

def ListenThread():
    print("ListenThread is start")
    contest = zmq.Context()
    socket_listen = contest.socket(zmq.PAIR)
    socket_listen.bind('tcp://*:6556')
    print("bind socket 5556 build\n")
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
        elif msg == "3":   # 拍照
            flag = 3
        elif msg == "4":   # 去雨
            flag == 4
            DerainT = threading.Thread(target=DerainThread)
            DerainT.start()
        elif msg == "5":
            # os.system("rm -rf UnDerainImg/*.jpg")
            # os.system("rm -rf DerainedImg/*.png")
            os.system("del /q \"UnDerainImg\"")
            os.system("del /q \"DerainedImg\"")
        mutex_flag.release()
        time.sleep(1)
    print("ListenThread dead")

def SendUnDerainThread():
    # 异步传输
    # IP = '172.20.10.5'
    print("SendUnDerainThread is start")
    IP = '10.136.5.141'
    contest = zmq.Context()
    socket_send = contest.socket(zmq.PAIR)
    socket_send.connect('tcp://%s:6557' % IP)
    print("connect socket 5557 build\n")
    while True:
        # print("1111111\n")
        if not filename.empty():
            name = filename.get()

            # print(name)
            frame = cv2.imread("C:/Users/lisherry/Desktop/Server/UnDerainImg/"+name+".jpg")
            # frame = cv2.imread("./UnDerainImg/" + name + ".jpg")
            # print(name)
            try:
                encoded, buffer = cv2.imencode('.jpg', frame)  # 把转换后的图像数据再次转换成流数据，
            except BaseException:
                # print("C:/Users/lisherry/Desktop/Server/UnDerainImg/" + name + ".jpg" + "  is not find\n")
                # print("./UnDerainImg/" + name + ".jpg" + "  is not find\n")
                filename.put(name)
                continue
            else:
                # print('copy C:/Users/lisherry/Desktop/Server/video_derain/' + name + '.png C:/Users/lisherry/Desktop/Server/DerainedImg/')
                os.system("copy video_derain\\" + name + ".png DerainedImg\\")

                filename_deran.put(name)
                jpg_buffer = base64.b64encode(buffer)  # 把内存中的图像流数据进行base64编码
                # print(name)
                socket_send.send(jpg_buffer)  # 把编码后的流数据发送给视频的接收端
                # print(name)
                msg = socket_send.recv_string()
                print("send a UnDerainImg\n")
        else:
            time.sleep(1)
    print("SendUnDerainThread is dead")

def DerainThread():
    print("DerainThread is start\n")
    # os.system("python Network/testing.py")
    print("DerainThread is dead\n")
    # os.system("Xcopy \"UnDerainImg\" \"DerainedImg\"")

def SendDerainThread():
    # 异步传输
    # IP = '172.20.10.5'
    print("SendDerainThread is start\n")
    IP = '10.136.5.141'
    contest = zmq.Context()
    socket_send = contest.socket(zmq.PAIR)
    socket_send.connect('tcp://%s:6558' % IP)
    print("connect socket 5558 build\n")
    while True:
        print("filename_deran.empty():"+str(filename_deran.empty())+"\n")
        if not filename_deran.empty() and len(os.listdir("DerainedImg")) > 0:
            name = filename_deran.get()
            time.sleep(2)
            print("SendDerainThread|"+name+"\n")
            frame = cv2.imread('C:/Users/lisherry/Desktop/Server/DerainedImg/'+name+'.png')
            try:
                encoded, buffer = cv2.imencode('.png', frame)  # 把转换后的图像数据再次转换成流数据，
            except BaseException:
                print("C:/Users/lisherry/Desktop/Server/DerainedImg/"+name+".png"+"  is not find\n")
                filename_deran.put(name)
                continue
            else:
                print(name)
                jpg_buffer = base64.b64encode(buffer)  # 把内存中的图像流数据进行base64编码
                print(name)
                socket_send.send(jpg_buffer)  # 把编码后的流数据发送给视频的接收端
                print(name)
                msg = socket_send.recv_string()
                print("send a DerainedImg\n")
        else:
            time.sleep(1)
    print("SendDerainThread is dead\n")

if __name__ == "__main__":
    print("---------clean local photo---------")
    os.system("del /q \"UnDerainImg\"")
    os.system("del /q \"DerainedImg\"")

    t1 = threading.Thread(target=SendThread)
    t2 = threading.Thread(target=ListenThread)
    t3 = threading.Thread(target=SendUnDerainThread)
    t4 = threading.Thread(target=SendDerainThread)

    t1.start()
    t2.start()
    t3.start()
    t4.start()

    t1.join()
    t2.join()
    t3.join()
    t4.join()
