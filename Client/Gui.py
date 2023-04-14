import os.path
import sys
import time

from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QHBoxLayout, QSizePolicy, QVBoxLayout, QLabel, \
    QTextEdit, QComboBox, QStatusBar, QMainWindow, QDesktopWidget
import cv2
import zmq
import base64
import numpy as np
import threading
from time import strftime, localtime

mutex_flag = threading.Lock()
flag = 0

mutex_num = threading.Lock()
num = 0

mutex_beginderain = threading.Lock()
beginderain = False

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
            frame = socket_listen.recv()  # 接收TCP传输过来的一帧视频图像数据
            socket_listen.send_string("receive frame")
            # print("listen a frame\n")
            img = base64.b64decode(frame)  # 把数据进行base64解码后储存到内存img变量中
            npimg = np.frombuffer(img, dtype=np.uint8)  # 把这段缓存解码成一维数组
            source = cv2.imdecode(npimg, 1)  # 将一维数组解码为图像source
            # cv2.imshow("Stream", source)  # 把图像显示在窗口中
            self.trigger.emit(source)
            cv2.waitKey(1)  # 延时等待，防止出现窗口无响应

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
                flag = 1
            mutex_flag.release()
            msg = socket_send.recv_string()
            time.sleep(1)
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
    trigger = pyqtSignal(object)

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
            # print("listen a frame\n")
            img = base64.b64decode(frame)  # 把数据进行base64解码后储存到内存img变量中
            npimg = np.frombuffer(img, dtype=np.uint8)  # 把这段缓存解码成一维数组
            source = cv2.imdecode(npimg, 1)  # 将一维数组解码为图像source
            # cv2.imshow("Stream", source)  # 把图像显示在窗口中
            timelog = strftime('%Y-%m-%d %H-%M-%S', localtime())
            cv2.imwrite("UnDerainImg/"+timelog+".jpg", source)

            mutex_beginderain.acquire()
            global beginderain
            if beginderain is True:
                mutex_num.acquire()
                global num
                if num == len(os.listdir("UnDerainImg")):
                    self.trigger.emit("本轮次未去雨图像已全部传输完毕")
                    num = 0
                    beginderain = False
                mutex_num.release()
            mutex_beginderain.release()
            time.sleep(1)

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

        mutex_num.acquire()
        global num
        num += 1
        mutex_num.release()

        # 获取显示帧数的label 并修改
        Text1 = self.findChild(QTextEdit, "Text1")
        text = int(Text1.toPlainText())
        print("%d"%text)
        Text1.setPlainText(str(text+1))

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
        mutex_flag.acquire()
        global flag
        flag = 4
        mutex_flag.release()
        mutex_beginderain.acquire()
        global beginderain
        beginderain = True
        mutex_beginderain.release()

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

    def SetFrameNum(self, num):
        Text1 = self.findChild(QTextEdit, "Text1")
        text = int(Text1.toPlainText())
        Text1.setPlainText(str(num))

    def center(self):
        # 获得屏幕坐标系
        screen = QDesktopWidget().screenGeometry()
        # 获得窗口坐标系
        size = self.geometry()
        # 获得窗口相关坐标
        L = (screen.width() - size.width()) // 2
        T = (screen.height() - size.height()) // 2
        # 移动窗口使其居中
        self.move(L, T)

    def Win(self):
        self.center()
        self.work1 = ListenThread()
        self.work2 = SendThread()
        self.work3 = CleanThread()
        self.work4 = ListenUnDerainThread()
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
        Text1 = QTextEdit()
        Text1.setObjectName("Text1")
        Text1.append("0")
        Button3 = QPushButton('去雨', self)
        Button4 = QPushButton('清空', self)
        Button5 = QPushButton('查看', self)
        Layout2.addWidget(Label1)
        Layout2.addWidget(Text1)
        Layout2.addWidget(Button3)
        Layout2.addWidget(Button4)
        Layout2.addWidget(Button5)
        Widget2.setLayout(Layout2)

        self.work3.signal.connect(self.SetFrameNum)

        Button3.clicked.connect(self.DeRain)
        Button4.clicked.connect(self.Clean)

        Widget3 = QWidget()
        Layout3 = QHBoxLayout(self)
        Label2 = QLabel()
        Label2.setObjectName('Label2')
        Label2.setPixmap(QPixmap("../Network/TestData/input/1.jpg"))
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
        Combox1 = QComboBox(self)
        Combox1.setObjectName("ComboBox")
        Layout4.addWidget(Combox1)
        Widget4.setLayout(Layout4)

        Widget5 = QWidget()
        Layout5 = QHBoxLayout(self)
        Label3 = QLabel()
        Label3.setPixmap(QPixmap("../Network/TestData/input/1.jpg"))
        Label4 = QLabel()
        Label4.setPixmap(QPixmap("../Network/TestData/input/1.jpg"))
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

        self.work4.trigger.connect(self.StatusBarChange)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MyWindows()
    w.show()
    sys.exit(app.exec_())