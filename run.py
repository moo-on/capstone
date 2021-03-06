import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(1100, 300, 400, 400)
        self.setWindowIcon(QIcon("icon.png"))
        self.setWindowTitle("bitcoin")

        btn = QPushButton("버튼 1", self)
        btn.move(10, 10)
        btn.clicked.connect(self.btn_clicked)

        btn = QPushButton("버튼 1", self)
        btn.move(10, 40)

    def btn_clicked(self):
        print("버튼 클릭")


app = QApplication(sys.argv)
window = MyWindow()
window.show()
app.exec_()