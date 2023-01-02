
import requests

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from config.config import chat_config

class Widget(QWidget):
    def __init__(self, bubble) -> None:
        super(Widget, self).__init__()
        self.bubble = bubble
        self.setWindowFlags(Qt.FramelessWindowHint|Qt.WindowStaysOnTopHint|Qt.SubWindow)
        self.setAutoFillBackground(False)
        self.setAttribute(Qt.WA_TranslucentBackground, True)

        pixmap:QPixmap = QPixmap('resources/image.png')
        label:QLabel = QLabel(self)
        label.setPixmap(pixmap)
        label.show()
        self.resize(label.width(), label.height())

        screen = QDesktopWidget().availableGeometry()
        screen_width = screen.width()
        screen_height = screen.height()
        self.setGeometry(screen_width - self.width() - self.bubble.width(), screen_height - self.height(), self.width(), self.height())

        action1 = QAction("退出", self)
        action1.triggered.connect(qApp.quit)
        action2 = QAction("显示/隐藏", self)
        action2.triggered.connect(self.show_or_hide)
        self.tray_menu = QMenu(self)
        self.tray_menu.addAction(action2)
        self.tray_menu.addAction(action1)
        self.tray:QSystemTrayIcon = QSystemTrayIcon(self)
        self.tray.setIcon(QIcon('resources/image.png'))
        self.tray.setContextMenu(self.tray_menu)
        self.tray.show()

    def show_or_hide(self):
        if self.isVisible():
            self.hide()
            self.bubble.hide()
        else:
            self.show()

    def mouseDoubleClickEvent(self, event:QMouseEvent) -> None:
        if event.button() == Qt.LeftButton:
            self.bubble.hide()
            msg, ok = QInputDialog.getText(self, '', '')
            if ok:
                hash = chat_config["hash"]

                url = "{}/api_v1/set_session_hash?hash={}".format(chat_config["webhost"], hash)
                rs = requests.get(url).json()
                if rs["status"]==2:
                    print("在设置中配置hash")
                if rs["status"]==1:
                    print("在web中创建机器人")
                if rs["status"]==0:
                    url = "{}/api_v1/chat?message={}&hash={}".format(chat_config["webhost"], msg, hash)
                    rs = requests.get(url).json()
                    for item in rs["output"]:
                        self.bubble.setText(item["message"])
                        self.bubble.move(self.x() + self.width(), self.y())
                        self.bubble.show()

    def contextMenuEvent(self, a0) -> None:
        self.tray_menu.exec_(self.mapToGlobal(a0.pos()))

    def mousePressEvent(self, event:QMouseEvent) -> None:
        if event.button() == Qt.LeftButton:
            self.dragging = True
            self.drag_position = event.globalPos() - self.pos()

    def mouseMoveEvent(self, event:QMouseEvent) -> None:
        if Qt.LeftButton and self.dragging:
            self.move(event.globalPos() - self.drag_position)
            self.bubble.move(self.x() + self.width(), self.y())
            event.accept()

    def mouseReleaseEvent(self, event:QMouseEvent) -> None:
        self.dragging = False
