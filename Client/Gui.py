import sys

from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QHBoxLayout, QSizePolicy, QVBoxLayout, QLabel, \
    QTextEdit, QComboBox


# QHBoxLayout 水平布局相关的类
# QSizePolicy 设置大小策略

class MyWindows(QWidget):
    def __init__(self):
        super().__init__()
        self.Win()

    def Win(self):
        LayoutWin = QHBoxLayout(self)

        Widget123 = QWidget()
        Layout123 = QVBoxLayout(self)

        Widget1 = QWidget()
        Layout1 = QHBoxLayout(self)
        Button1 = QPushButton('拍照', self)
        Button2 = QPushButton('暂停', self)
        Layout1.addWidget(Button1)
        Layout1.addWidget(Button2)
        Widget1.setLayout(Layout1)

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
        Label2.setPixmap(QPixmap("../Network/TestData/input/1.jpg"))
        Layout3.addWidget(Label2)
        Widget3.setLayout(Layout3)

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