
import requests
import webbrowser

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from widget.bubble import Bubble
from config.config import client_config

class Widget(QWidget):
    def __init__(self, bubble:Bubble) -> None:
        super(Widget, self).__init__()
        self.bubble:Bubble = bubble
        self.timer = QTimer(self)
        self.waiting_input = False

        self.timer.timeout.connect(self.bubble.hide)

        self.setWindowFlags(Qt.FramelessWindowHint|Qt.WindowStaysOnTopHint|Qt.SubWindow)
        self.setAutoFillBackground(False)
        self.setAttribute(Qt.WA_TranslucentBackground, True)

        pixmap:QPixmap = QPixmap( "resources/image/{}".format( client_config["image"]) )
        pixmap = pixmap.scaled( int((pixmap.width()/pixmap.height())*300), 300, Qt.KeepAspectRatio )
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
        action_anything:QAction = QAction("Anything v4.5", self)
        action_anything.triggered.connect(self.browse_anything_ai)
        action_protogen_ai:QAction = QAction("Protogen Diffusion", self)
        action_protogen_ai.triggered.connect(self.browse_protogen_ai)
        action_writing:QAction = QAction("写作(Writing)", self)
        action_writing.triggered.connect(self.browse_writing)
        action_chatroom:QAction = QAction("聊天室", self)
        action_chatroom.triggered.connect(self.browse_chatroom)

        self.tray_menu:QMenu = QMenu(self)
        self.tray_menu.addAction(action_show)
        self.tray_menu.addAction(action_chatroom)
        self.tray_menu.addAction(action_writing)
        self.tray_menu.addAction(action_anything)
        self.tray_menu.addAction(action_protogen_ai)
        self.tray_menu.addAction(action_quit)

        self.tray:QSystemTrayIcon = QSystemTrayIcon(self)
        self.tray.setIcon(QIcon('resources/icon.png'))
        self.tray.setContextMenu(self.tray_menu)
        self.tray.show()

    def browse_anything_ai(self) -> None:
        webbrowser.open("https://camenduru-webui-docker.hf.space/")
        self.bubble.hide()

    def browse_protogen_ai(self) -> None:
        webbrowser.open("https://darkstorm2150-protogen-web-ui.hf.space/")
        self.bubble.hide()

    def browse_writing(self) -> None:
        web_host:str = client_config["web_host"]
        bot_id:str = client_config["default_bot"]
        webbrowser.open( "{}/{}/write".format(web_host, bot_id) )
        self.bubble.hide()

    def browse_chatroom(self) -> None:
        web_host:str = client_config["web_host"]
        bot_id:str = client_config["default_bot"]
        webbrowser.open( "{}/{}/chatroom".format(web_host, bot_id) )
        self.bubble.hide()

    def show_or_hide(self) -> None:
        if self.isVisible():
            self.hide()
            self.bubble.hide()
        else:
            self.show()

    def show_bubble_with_text(self, text:str) -> None:
        self.bubble.setText(text)
        self.bubble.move(self.x() + int(self.width()*2/3), self.y() - int(self.height()/3))
        self.bubble.show()
        self.timer.start(5000)

    def mouseDoubleClickEvent(self, event:QMouseEvent) -> None:
        if event.button() == Qt.LeftButton and not self.waiting_input:
            self.waiting_input = True
            self.bubble.hide()
            input_dialog = QInputDialog(self)
            input_dialog.setInputMode(QInputDialog.TextInput)
            input_dialog.setLabelText("你想和我说什么~")
            input_dialog.setWindowTitle(" ")
            input_dialog.resize(500, 100)
            input_dialog.show()
            if input_dialog.exec_() == input_dialog.Accepted:
                web_host:str = client_config["web_host"]
                message:str = input_dialog.textValue()
                bot_id:str = client_config["default_bot"]
                speaker:str = client_config["name"]

                url:str = "{}/api_v1/{}/chat?speaker={}&message={}".format(web_host, bot_id, speaker, message)
                rs:dict = requests.get(url).json()

                if rs["code"]==0:
                    for item in rs["data"]["response"]:
                        self.show_bubble_with_text( item["message"] )
            self.waiting_input = False

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
