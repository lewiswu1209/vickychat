
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

        bubble_bg:QPixmap = QPixmap('resources/bubble.png')
        label_bg:QLabel = QLabel(self)
        label_bg.setPixmap(bubble_bg)
        label_bg.resize( bubble_bg.width() + 50, bubble_bg.height() )
        layout_bg:QHBoxLayout = QHBoxLayout()
        layout_bg.addWidget(label_bg)
        layout_bg.setAlignment( Qt.AlignHCenter | Qt.AlignVCenter )
        self.resize( label_bg.width(), label_bg.height() )
        self.setLayout(layout_bg)

        window_txt:QWidget = QWidget(self)
        self.label_txt:QLabel = QLabel(window_txt)
        self.label_txt.setWordWrap(True)
        self.label_txt.setText("")
        self.label_txt.resize(self.width(), self.height())
        layout_txt:QHBoxLayout = QHBoxLayout()
        layout_txt.addWidget(self.label_txt)
        layout_txt.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        window_txt.resize(self.width(), self.height())
        window_txt.setLayout(layout_txt)

    def setText(self, text:str) -> None:
        self.label_txt.setText(text)
