
from PyQt5.QtWidgets import QHBoxLayout

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

class Bubble(QWidget):
    def __init__(self) -> None:
        super(Bubble, self).__init__()
        self.setWindowFlags(Qt.FramelessWindowHint|Qt.WindowStaysOnTopHint|Qt.SubWindow)
        self.setAutoFillBackground(False)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        pixmap:QPixmap = QPixmap('resources/bubble.png')
        pixmap = pixmap.scaled(int(pixmap.width() * 0.7), int(pixmap.height() * 0.7), Qt.KeepAspectRatio)
        label_bg = QLabel(self)
        label_bg.setPixmap(pixmap)
        label_bg.resize(pixmap.width(), pixmap.height())
        layout_bg = QHBoxLayout()
        layout_bg.addWidget(label_bg)
        layout_bg.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.resize(label_bg.width(), label_bg.height())
        self.setLayout(layout_bg)

        self.window_txt = QWidget(self)
        self.label_txt = QLabel(self.window_txt)
        self.label_txt.setWordWrap(True)
        self.label_txt.setText("")
        self.label_txt.resize(self.width(), self.height())
        layout_txt = QHBoxLayout()
        layout_txt.addWidget(self.label_txt)
        layout_txt.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.window_txt.resize(self.width(), self.height())
        self.window_txt.setLayout(layout_txt)
    
    def setText(self, text):
        self.label_txt.setText(text)
