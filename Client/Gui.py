# port 5555:send-receive cap frame
# port 5556:send-receive flag
# port 5557:send-receive UnDerain Img
# port 5558:send-receive Derain Img

import os.path
import sys
import time

from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QHBoxLayout, QSizePolicy, QVBoxLayout, QLabel, \
    QTextEdit, QComboBox, QStatusBar, QMainWindow, QDesktopWidget, QLineEdit
import cv2
import zmq
import base64
import numpy as np
import threading
from time import strftime, localtime
from queue import Queue

mutex_flag = threading.Lock()
flag = 0

mutex_num = threading.Lock()
num = 0

mutex_timelogs = threading.Lock()
timelogs = Queue()

class ListenThread(QThread):
    trigger = pyqtSignal(object)

    def __int__(self):
        super(ListenThread, self).__int__()

    def run(self):
        print("thread1 is start\n")
        context = zmq.Context()
        socket_listen = context.socket(zmq.PAIR)
        socket_listen.bind('tcp://*:5555')
        print("bind socket 5555 build\n")
        while True:
            frame = socket_listen.recv()
            socket_listen.send_string("receive frame")
            # print("listen a frame\n")
            img = base64.b64decode(frame)
            npimg = np.frombuffer(img, dtype=np.uint8)
            source = cv2.imdecode(npimg, 1)
            # cv2.imshow("Stream", source)
            self.trigger.emit(source)
            cv2.waitKey(1)

class SendThread(QThread):
    def __int__(self):
        super(SendThread, self).__int__()

    def run(self):
        print("thread2 is start\n")
        # IP = '172.20.10.5'
        IP = '172.23.80.1'
        contest = zmq.Context()
        socket_send = contest.socket(zmq.PAIR)
        socket_send.connect('tcp://%s:5556' % IP)
        print("send socket 5556 build\n")
        old_flag = -1
        global flag
        while True:
            # if self.flag == 1:
            #     socket_.send("1")
            # elif self.flag == 2:
            #     socket_.send("2")
            # elif self.flag == 0:
            #     socket_.send("0")
            # elif self.flag == 3:
            #     socket_.send("3")
            # try:
            mutex_flag.acquire()
            print("thread2 is running, self.flag==" + str(flag) + "\n")
            socket_send.send_string(str(flag))
            if flag == 3 or flag == 5 or flag == 4:  # 这几个操作和摄像头显示是并行的
                if old_flag == 1:
                    flag = 1
                else:
                    flag = 0
            old_flag = flag
            mutex_flag.release()
            msg = socket_send.recv_string()


class CleanThread(QThread):
    signal = pyqtSignal(object)

    def __int__(self):
        super(CleanThread, self).__int__()

    def run(self):
        print("thread3 is start\n")
        path = "DerainedImg"
        if os.path.isdir(path):
            os.system("del /q \""+path+"\"")
        else:
            print("path:"+path+"is not exist\n")
        path = "UnDerainImg"
        if os.path.isdir(path):
            os.system("del /q \"" + path + "\"")
        else:
            print("path:" + path + "is not exist\n")
        mutex_num.acquire()
        global num
        num = 0
        mutex_num.release()
        self.signal.emit(0)

class ListenUnDerainThread(QThread):
    # trigger = pyqtSignal(object)

    def __int__(self):
        super(ListenUnDerainThread, self).__int__()

    def run(self):
        print("thread4 is start\n")
        context = zmq.Context()
        socket_listen = context.socket(zmq.PAIR)
        socket_listen.bind('tcp://*:5557')
        print("bind socket 5557 build\n")
        while True:
            frame = socket_listen.recv()  # 接收TCP传输过来的一帧视频图像数据
            socket_listen.send_string("receive frame")
            img = base64.b64decode(frame)  # 把数据进行base64解码后储存到内存img变量中
            npimg = np.frombuffer(img, dtype=np.uint8)  # 把这段缓存解码成一维数组
            source = cv2.imdecode(npimg, 1)  # 将一维数组解码为图像source
            timelog = strftime('%Y-%m-%d %H-%M-%S', localtime())
            cv2.imwrite("UnDerainImg/"+timelog+".jpg", source)
            print("save a underain photo\n")

            mutex_timelogs.acquire()
            global timelogs
            timelogs.put(timelog)
            mutex_timelogs.release()

            time.sleep(1)

class ListenDerainThread(QThread):

    def __int__(self):
        super(ListenDerainThread, self).__int__()

    def run(self):
        print("thread5 is start\n")
        context = zmq.Context()
        socket_listen = context.socket(zmq.PAIR)
        socket_listen.bind('tcp://*:5558')
        print("bind socket 5558 build\n")
        while True:
            frame = socket_listen.recv()
            socket_listen.send_string("receive frame")
            img = base64.b64decode(frame)
            npimg = np.frombuffer(img, dtype=np.uint8)
            source = cv2.imdecode(npimg, 1)
            # timelog = strftime('%Y-%m-%d %H-%M-%S', localtime())
            mutex_timelogs.acquire()
            timelog = timelogs.get()
            mutex_timelogs.release()
            cv2.imwrite("DerainedImg/"+timelog+".jpg", source)
            print("save a derain photo\n")
            time.sleep(1)

class JudgeThread(QThread):
    beginderain = pyqtSignal(object)
    endderain1 = pyqtSignal(object)
    endderain2 = pyqtSignal(object)

    def __int__(self):
        super(JudgeThread, self).__int__()

    def run(self):
        num_derain = -1
        while True:
            mutex_flag.acquire()
            global flag
            if flag == 4:
                print("JudgeThread|flag:" + str(flag) + "\n")
                mutex_num.acquire()
                global num
                if num == len(os.listdir("UnDerainImg")):
                    self.beginderain.emit("待去雨帧收集完毕，开始去雨")
                    print("JudgeThread|num:" + str(num) + "\n")
                    num_derain = num
                    num = 0
                mutex_num.release()
            mutex_flag.release()
            print("JudgeThread|num_derain:" + str(num_derain) + "\n")
            if num_derain == len(os.listdir("DerainedImg")):
                self.endderain1.emit("去雨帧收集完毕，去雨完成")
                self.endderain2.emit(0)
                num_derain = -1
            time.sleep(5)

class MyWindows(QWidget):

    def __init__(self):
        super(MyWindows, self).__init__()
        self.Win()
        self.StatusMsgs = ["开始清理本地照片", "本地照片清理完毕", "摄像头开始工作", "本轮次未去雨图像已全部传输完毕"]

    def MakePhoto(self):
        print('-----MakePhoto-----')

        mutex_flag.acquire()
        global flag
        flag = 3
        mutex_flag.release()
        self.work2.start()

        mutex_num.acquire()
        global num
        num += 1
        mutex_num.release()

        # 获取显示帧数的label 并修改
        Text1 = self.findChild(QLineEdit, "Text1")
        Text1Value = int(Text1.text())
        # print("%d"%Text1Value)
        Text1.setText(str(Text1Value+1))

    def BeginVideo(self):
        print('-----BeginVideo----')
        self.work1.start()
        self.work2.start()
        self.work4.start()

        mutex_flag.acquire()
        global flag
        flag = 1
        mutex_flag.release()

    def ShowPerFrame(self, frame):
        Label2 = self.findChild(QLabel, 'Label2')
        len_x = frame.shape[1]  # 获取图像大小
        wid_y = frame.shape[0]
        frame = QImage(frame.data, len_x, wid_y, len_x * 3, QImage.Format_RGB888)  # 此处如果不加len_x*3，就会发生倾斜
        pix = QPixmap.fromImage(frame)
        Label2.setPixmap(pix)  # 在label上显示图片
        Label2.setScaledContents(True)  # 让图片自适应label大小

    def StopVideo(self):
        print('-----StopVideo----')
        self.work1.exit()
        mutex_flag.acquire()
        global flag
        flag = 0
        mutex_flag.release()
        StatusBar = self.findChild(QStatusBar, 'StatusBar')
        StatusBar.showMessage("摄像头暂停")

    def EndVideo(self):
        print('-----EndVideo----')
        self.work1.exit()
        mutex_flag.acquire()
        global flag
        flag = 2
        mutex_flag.release()
        StatusBar = self.findChild(QStatusBar, 'StatusBar')
        StatusBar.showMessage("摄像头关闭")

    def DeRain(self):
        print('-----DeRain-----')

        self.work5.start()  # 开始接受 derain img
        self.work6.start()
        mutex_flag.acquire()
        global flag
        flag = 4
        mutex_flag.release()

    def Clean(self):
        print('-----Clean-----')
        self.work3.start()
        mutex_flag.acquire()
        global flag
        flag = 5
        mutex_flag.release()

    def StatusBarChange(self, msg):
        StatusBar = self.findChild(QStatusBar, 'StatusBar')
        StatusBar.showMessage(msg)

    def SetFrameNum(self, num_):
        Text1 = self.findChild(QLineEdit, "Text1")
        Text1Value = int(Text1.text())
        Text1.setText(str(num_))

    def Center(self):
        # 获得屏幕坐标系
        screen = QDesktopWidget().screenGeometry()
        # 获得窗口坐标系
        size = self.geometry()
        # 获得窗口相关坐标
        L = (screen.width() - size.width()) // 2
        T = (screen.height() - size.height()) // 2
        # 移动窗口使其居中
        self.move(L, T)

    def AddComboBoxItem(self, msg):
        ComboBox1 = self.findChild(QComboBox, "ComboBox1")
        UnDerainImgs = os.listdir("UnDerainImg")
        DerainedImgs = os.listdir("DerainedImg")
        if len(UnDerainImgs) != len(DerainedImgs):
            print("warning|len(UnDerainImgs) != len(DerainedImgs)\n")
        for i, val in enumerate(UnDerainImgs):
            for j, val_ in enumerate(DerainedImgs):
                if val == val_:
                    break
            if j < len(DerainedImgs):
                timelog = val[:-4]
                ComboBox1.addItem(timelog+".jpg")

    def ShowFrame(self):
        Label3 = self.findChild(QLabel, "Label3")
        Label4 = self.findChild(QLabel, "Label4")
        UnDerainImgs = os.listdir("UnDerainImg")
        DerainedImgs = os.listdir("DerainedImg")
        ComboBox1 = self.findChild(QComboBox, "ComboBox1")
        Index = ComboBox1.currentIndex()
        text = ComboBox1.itemText(Index)
        Label3.setPixmap(QPixmap("UnDerainImg/"+text))
        Label4.setPixmap(QPixmap("DerainedImg/"+text))

    def Win(self):
        # self.Center()

        self.work1 = ListenThread()
        self.work2 = SendThread()
        self.work3 = CleanThread()
        self.work4 = ListenUnDerainThread()
        self.work5 = ListenDerainThread()
        self.work6 = JudgeThread()

        LayoutWin = QHBoxLayout(self)
        WidgetWin = QWidget()

        Widget123 = QWidget()
        Layout123 = QVBoxLayout(self)

        Widget1 = QWidget()
        Layout1 = QHBoxLayout(self)
        Button0 = QPushButton('开始', self)
        Button1 = QPushButton('拍照', self)
        Button2 = QPushButton('暂停', self)
        Button22 = QPushButton('停止', self)
        Layout1.addWidget(Button0)
        Layout1.addWidget(Button1)
        Layout1.addWidget(Button2)
        Layout1.addWidget(Button22)
        Widget1.setLayout(Layout1)

        Button0.clicked.connect(self.BeginVideo)
        Button1.clicked.connect(self.MakePhoto)
        Button2.clicked.connect(self.StopVideo)
        Button22.clicked.connect(self.EndVideo)

        Widget2 = QWidget()
        Layout2 = QHBoxLayout(self)
        Label1 = QLabel('需处理的帧数：')
        Text1 = QLineEdit()

        Text1.setObjectName("Text1")
        Text1.setText("0")
        Button3 = QPushButton('去雨', self)
        Button4 = QPushButton('清空', self)
        Layout2.addWidget(Label1)
        Layout2.addWidget(Text1)
        Layout2.addWidget(Button3)
        Layout2.addWidget(Button4)
        Widget2.setLayout(Layout2)

        self.work3.signal.connect(self.SetFrameNum)

        Button3.clicked.connect(self.DeRain)
        Button4.clicked.connect(self.Clean)

        Widget3 = QWidget()
        Layout3 = QHBoxLayout(self)
        Label2 = QLabel()
        Label2.setObjectName('Label2')
        Label2.setPixmap(QPixmap("../Server/Network/TestData/input/1.jpg"))
        Layout3.addWidget(Label2)
        Widget3.setLayout(Layout3)

        self.work1.trigger.connect(self.ShowPerFrame)


        Layout123.addWidget(Widget1)
        Layout123.addWidget(Widget2)
        Layout123.addWidget(Widget3)
        Widget123.setLayout(Layout123)

        Widget45 = QWidget()
        Layout45 = QVBoxLayout(self)

        Widget4 = QWidget()
        Layout4 = QHBoxLayout(self)
        ComboBox1 = QComboBox(self)
        ComboBox1.setObjectName("ComboBox1")
        ComboBox1.activated.connect(self.ShowFrame)

        Layout4.addWidget(ComboBox1)
        Widget4.setLayout(Layout4)


        Widget5 = QWidget()
        Layout5 = QHBoxLayout(self)
        Label3 = QLabel()
        Label3.setPixmap(QPixmap("../Server/Network/TestData/input/1.jpg"))
        Label3.setObjectName("Label3")
        Label4 = QLabel()
        Label4.setPixmap(QPixmap("../Server/Network/TestData/input/1.jpg"))
        Label4.setObjectName("Label4")
        Layout5.addWidget(Label3)
        Layout5.addWidget(Label4)
        Widget5.setLayout(Layout5)

        Layout45.addWidget(Widget4)
        Layout45.addWidget(Widget5)
        Widget45.setLayout(Layout45)

        LayoutWin.addWidget(Widget123)
        LayoutWin.addWidget(Widget45)
        WidgetWin.setLayout(LayoutWin)

        # 状态栏信号-槽函数
        statusBar = QStatusBar()
        statusBar.setObjectName("StatusBar")

        LayoutWin_StatusBar = QVBoxLayout(self)
        LayoutWin_StatusBar.addWidget(WidgetWin)
        LayoutWin_StatusBar.addWidget(statusBar)
        self.setLayout(LayoutWin_StatusBar)

        self.work1.started.connect(lambda : self.StatusBarChange(self.StatusMsgs[2]))

        self.work3.started.connect(lambda : self.StatusBarChange(self.StatusMsgs[0]))
        self.work3.finished.connect(lambda : self.StatusBarChange(self.StatusMsgs[1]))

        self.work6.beginderain.connect(self.StatusBarChange)

        self.work6.endderain1.connect(self.StatusBarChange)
        self.work6.endderain2.connect(self.SetFrameNum)
        self.work6.endderain1.connect(self.AddComboBoxItem)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MyWindows()
    w.show()
    sys.exit(app.exec_())
