
from PyQt5.QtWidgets import (QWidget, QDesktopWidget,
    QPushButton, QApplication, QHBoxLayout, QComboBox, QLabel,
                             QFrame, QSplitter, )
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QImage,QPixmap
import sys


class Viewer(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        hbox = QHBoxLayout(self)

        self.left_map = QLabel()
        self.left_map.move(135,318)

        self.right_map = QLabel()
        self.right_map.move(135, 318)

        bottom = QFrame(self)
        bottom.setFrameShape(QFrame.StyledPanel)

        self.dataset = QComboBox(bottom)
        self.dataset.addItem("t4.8k.dat",1)
        self.dataset.addItem("paint",2)
        self.dataset.move(120,18)
        msg1 = QLabel("Select a dataset:",bottom)
        msg1.move(10,20)

        algorithm = QComboBox(bottom)
        algorithm.addItem("k-means")
        algorithm.move(120,43)
        msg2 = QLabel("Select a method:",bottom)
        msg2.move(10,45)

        start = QPushButton('Start', bottom)
        start.move(10, 65)
        start.clicked.connect(self.show_picture)

        msg3 = QLabel("PS: Select a dataset and a clustering algorithm then push start to see the stability analysis result.",bottom)
        msg4 = QLabel("PSS: To see the details of the algorithm, please run stability.py in command line.",bottom)
        msg3.move(10,120)
        msg4.move(10,140)

        splitter1 = QSplitter(Qt.Horizontal)
        splitter1.addWidget(self.left_map)
        splitter1.addWidget(self.right_map)

        splitter2 = QSplitter(Qt.Vertical)
        splitter2.addWidget(splitter1)
        splitter2.addWidget(bottom)
        splitter2.setSizes([380, 200])

        hbox.addWidget(splitter2)
        self.setLayout(hbox)

        self.resize(800, 550)
        self.center()
        self.show()

    def show_picture(self):
        dataInfo = self.dataset.currentData()
        print(dataInfo)
        if dataInfo == 1:
            original = "original_t4.8k.png"
            new = "new_t4.8k.png"
        else:
            original = "original_paint.png"
            new = "new_paint.png"
        print(original)
        original_map = QImage(original).scaledToHeight(300)
        new_map = QImage(new).scaledToHeight(300)

        self.left_map.setPixmap(QPixmap.fromImage(original_map))
        self.right_map.setPixmap(QPixmap.fromImage(new_map))

    def handleActivated(self,index):
        print(self.dataset.itemData(index),type(self.dataset.itemData(index)))
        return self.dataset.itemData(index)

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Viewer()
    sys.exit(app.exec_())