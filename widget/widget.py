
import requests
import webbrowser

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from widget.bubble import Bubble
from config.config import chat_config

class Widget(QWidget):
    def __init__(self, bubble:Bubble) -> None:
        super(Widget, self).__init__()
        self.bubble:Bubble = bubble
        self.setWindowFlags(Qt.FramelessWindowHint|Qt.WindowStaysOnTopHint|Qt.SubWindow)
        self.setAutoFillBackground(False)
        self.setAttribute(Qt.WA_TranslucentBackground, True)

        pixmap:QPixmap = QPixmap('resources/image.png')
        label:QLabel = QLabel(self)
        label.setPixmap(pixmap)
        label.show()
        self.resize(label.width(), label.height())

        screen:QRect = QDesktopWidget().availableGeometry()
        screen_width:int = screen.width()
        screen_height:int = screen.height()
        self.setGeometry(screen_width - self.width() - self.bubble.width(), screen_height - self.height(), self.width(), self.height())

        action_quit:QAction = QAction("退出", self)
        action_quit.triggered.connect(qApp.quit)
        action_show:QAction = QAction("显示/隐藏", self)
        action_show.triggered.connect(self.show_or_hide)
        action_anything:QAction = QAction("作画(Anything)", self)
        action_anything.triggered.connect(self.browse_anything_ai)
        action_stable_diffusion_ai:QAction = QAction("作画(Stable Diffusion)", self)
        action_stable_diffusion_ai.triggered.connect(self.browse_stable_diffusion)
        action_writing:QAction = QAction("写作(Writing)", self)
        action_writing.triggered.connect(self.browse_writing)
        action_chatroom:QAction = QAction("聊天室", self)
        action_chatroom.triggered.connect(self.browse_chatroom)

        self.tray_menu:QMenu = QMenu(self)
        self.tray_menu.addAction(action_show)
        self.tray_menu.addAction(action_chatroom)
        self.tray_menu.addAction(action_writing)
        self.tray_menu.addAction(action_anything)
        self.tray_menu.addAction(action_stable_diffusion_ai)
        self.tray_menu.addAction(action_quit)

        self.tray:QSystemTrayIcon = QSystemTrayIcon(self)
        self.tray.setIcon(QIcon('resources/icon.png'))
        self.tray.setContextMenu(self.tray_menu)
        self.tray.show()

    def browse_anything_ai(self) -> None:
        webbrowser.open("https://camenduru-webui.hf.space/")
        self.bubble.hide()

    def browse_stable_diffusion(self) -> None:
        webbrowser.open("https://stabilityai-stable-diffusion.hf.space/")
        self.bubble.hide()

    def browse_writing(self) -> None:
        webbrowser.open( "{}/writing".format(chat_config["webhost"]) )
        self.bubble.hide()

    def browse_chatroom(self) -> None:
        webbrowser.open( "{}/?hash={}".format(chat_config["webhost"], chat_config["hash"]) )
        self.bubble.hide()

    def show_or_hide(self) -> None:
        if self.isVisible():
            self.hide()
            self.bubble.hide()
        else:
            self.show()

    def mouseDoubleClickEvent(self, event:QMouseEvent) -> None:
        if event.button() == Qt.LeftButton:
            self.bubble.hide()
            msg, ok = QInputDialog.getText(self, '', None, flags=Qt.FramelessWindowHint)
            if ok:
                hash:str = chat_config["hash"]

                url:str = "{}/api_v1/set_session_hash?hash={}".format(chat_config["webhost"], hash)
                rs:dict = requests.get(url).json()
                if rs["status"]==2:
                    print("在设置中配置hash")
                if rs["status"]==1:
                    print("在web中创建机器人")
                if rs["status"]==0:
                    url = "{}/api_v1/chat?message={}&hash={}".format(chat_config["webhost"], msg, hash)
                    rs = requests.get(url).json()
                    for item in rs["output"]:
                        self.bubble.setText(item["message"])
                        self.bubble.move(self.x() + int(self.width()*2/3), self.y() - int(self.height()/3))
                        self.bubble.show()

    def contextMenuEvent(self, event:QMouseEvent) -> None:
        self.tray_menu.exec_( self.mapToGlobal( event.pos() ) )

    def mousePressEvent(self, event:QMouseEvent) -> None:
        if event.button() == Qt.LeftButton:
            self.dragging = True
            self.drag_position = event.globalPos() - self.pos()

    def mouseMoveEvent(self, event:QMouseEvent) -> None:
        if Qt.LeftButton and self.dragging:
            self.move(event.globalPos() - self.drag_position)
            self.bubble.move(self.x() + int(self.width()*2/3), self.y() - int(self.height()/3))
            event.accept()

    def mouseReleaseEvent(self, event:QMouseEvent) -> None:
        if event.button() == Qt.LeftButton:
            self.dragging = False
