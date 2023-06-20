import sys
# from PySide6 import QtWidgets
# from PySide2 import QtWidgets
from PyQt5 import QtWidgets
from qt_material import apply_stylesheet

# create the application and the main window
app = QtWidgets.QApplication(sys.argv)
window = QtWidgets.QMainWindow()

# setup stylesheet
apply_stylesheet(app, theme='dark_teal.xml')

# class MyWindows(QWidget):
#     def __int__(self):
#         super(MyWindows, self).__int__()
#
#     def ui(self):

# run
window.show()
app.exec_()