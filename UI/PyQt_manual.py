import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtCore import *
import pykorbit

form_class = uic.loadUiType("window.ui")[0]

class MyWindow(QMainWindow, form_class):
    def __init__(self):
        super().__init__()  # QMainWindow 상속
        self.setupUi(self)

        self.timer = QTimer(self)
        self.timer.start(1000)
        self.timer.timeout.connect(self.inquiry)

        self.pushButton.clicked.connect(self.inquiry)

        # self.setGeometry(300, 200, 300, 400) # 위치
        # self.setWindowTitle("PyQt")

        # self.setWindowIcon(QIcon = "love.png")
        # btn = QPushButton("버튼1", self)
        # btn.move(10,10)
        # btn.clicked.connect(self.btn_clicked)
        # btn2 = QPushButton("버튼2", self)
        # btn2.move(10, 40)

    # 이벤트 처리
    def btn_clicked(self):
        print("버튼클릭")

    def inquiry(self):
        price = pykorbit.get_current_price("BTC")
        self.lineEdit.setText(str(price))

    def timeout(self):
        cur_time = QTime.currentTime()
        str_time = cur_time.toString("hh:mm:ss")
        self.statusBar().showMessage(str_time)


# Qapplication 객체 생성 및 이벤트 루프 생성
app = QApplication(sys.argv)
window = MyWindow()
window.show()
app.exec_()
