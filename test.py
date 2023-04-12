import sys
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import QApplication, QWidget, QDesktopWidget, QPushButton, QHBoxLayout, QTextBrowser

class Worker(QThread):
    signal = pyqtSignal(object)

    def __init__(self):
        super(Worker, self).__init__()
        self.t_code = True

    def run(self):
        num = 0
        print(self.t_code)
        while self.t_code:
            num += 1
            self.signal.emit(num)
            self.sleep(1)


class MyWin(QWidget):
    def __init__(self):
        super(MyWin, self).__init__()
        self.b_code = 0
        self.MyUi()

    def MyUi(self):
        self.setWindowTitle('多线程测试')
        self.resize(400, 400)
        self.center()

        b = QPushButton('启动')
        b.clicked.connect(lambda: self.b_onclick(b))

        self.txts = QTextBrowser()

        hbl = QHBoxLayout()
        hbl.addWidget(b)
        hbl.addWidget(self.txts)

        self.t = Worker()

        self.t.signal.connect(self.texts)
        self.setLayout(hbl)

    def b_onclick(self, b):

        if self.b_code == 0:
            self.b_code = 1
            b.setText('停止')

            self.txts.append('启动')
            self.t.start()
            self.t.t_code = True
        else:
            self.b_code = 0
            b.setText('启动')

            self.txts.append('停止')
            self.t.t_code = False
            self.t.exit()

    def texts(self, data):
        print(data)
        self.txts.append(str(data))

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

if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MyWin()
    w.show()
    sys.exit(app.exec_())