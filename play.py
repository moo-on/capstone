import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic

form_class = uic.loadUiType("/Users/I/Desktop/mywindow.ui")[0]

class MyWindow(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.btn_clicked)ㄴㅇㄹㅇ

    def btn_clicked(self):
        print("버튼클릭")

app = QApplication(sys.argv)
mywindow = MyWindow()
mywindow.show()
app.exec_()
