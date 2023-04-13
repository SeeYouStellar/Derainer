import sys
import time

from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QHBoxLayout, QSizePolicy, QVBoxLayout, QLabel, \
    QTextEdit, QComboBox
import cv2
import zmq
import base64
import numpy as np
import threading

mutex_flag = threading.Lock()
flag = 0

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
        IP = '172.20.10.5'
        contest = zmq.Context()
        socket_send = contest.socket(zmq.PAIR)
        socket_send.connect('tcp://%s:5556' % IP)
        print("send socket 5556 build\n")
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
            mutex_flag.release()
            msg = socket_send.recv_string()
            time.sleep(1)

class MyWindows(QWidget):
    def __init__(self):
        super(MyWindows, self).__init__()
        self.Win()

    def MakePhoto(self):
        print('-----MakePhoto-----')
        mutex_flag.acquire()
        global flag
        flag = 3
        mutex_flag.release()

    def BeginVideo(self):
        print('-----BeginVideo----')
        self.work1.start()
        self.work2.start()
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

    def EndVideo(self):
        print('-----EndVideo----')
        self.work1.exit()
        mutex_flag.acquire()
        global flag
        flag = 2
        mutex_flag.release()

    def Win(self):
        self.work1 = ListenThread()
        self.work2 = SendThread()
        LayoutWin = QHBoxLayout(self)

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
        self.setLayout(LayoutWin)
        # self.statusBar.showMessage('就绪')



if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MyWindows()
    w.show()
    sys.exit(app.exec_())