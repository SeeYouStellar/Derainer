
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from Gui import MyWindows


class MyMainWindow(QMainWindow, MyWindows):
    def __init__(self, parent=None):
        super(MyMainWindow, self).__init__(parent)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWin = MyMainWindow()
    myWin.show()
    sys.exit(app.exec_())
