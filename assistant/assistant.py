
import webbrowser

from functools import partial

from PyQt5.QtGui import QIcon
from PyQt5.QtGui import QPixmap
from PyQt5.QtGui import QDropEvent
from PyQt5.QtGui import QMouseEvent
from PyQt5.QtGui import QDragEnterEvent

from PyQt5.QtCore import Qt
from PyQt5.QtCore import QRect
from PyQt5.QtCore import QPoint
from PyQt5.QtCore import QTimer

from PyQt5.QtWidgets import qApp
from PyQt5.QtWidgets import QMenu
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QAction
from PyQt5.QtWidgets import QInputDialog
from PyQt5.QtWidgets import QDesktopWidget
from PyQt5.QtWidgets import QSystemTrayIcon

from config.config import client_config
from config.config import actions

from assistant.worker_thread import WorkerThread
from assistant.chat_thread import ChatThread
from assistant.text_window import TextWindow

class DesktopAssistant(QWidget):
    def __init__(self) -> None:
        super().__init__()

        self.setAutoFillBackground(False)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.setWindowFlags(Qt.FramelessWindowHint|Qt.WindowStaysOnTopHint|Qt.Tool)
        self.setAcceptDrops(True)

        pixmap:QPixmap = QPixmap( "resources/image/rabbit.png" )
        pixmap_height:int = 300
        pixmap_width:int  = int((pixmap.width()/pixmap.height())*300)
        pixmap = pixmap.scaled(pixmap_width, pixmap_height, Qt.KeepAspectRatio )

        label:QLabel = QLabel(self)
        label.setPixmap(pixmap)
        label.show()

        self.resize(label.width(), label.height())

        screen:QRect = QDesktopWidget().availableGeometry()
        screen_width:int = screen.width()
        screen_height:int = screen.height()
        self.setGeometry(screen_width - self.width(), screen_height - self.height(), self.width(), self.height())

        self._text_window = TextWindow()
        self._timer = QTimer(self)
        self._timer.timeout.connect(self._on_timer_stop)
        self._is_thinking = False
        self._dropped_text= None

        command_menu_items = []

        for action in actions:
            tmp = {
                "text": action["label"],
                "connect": partial(self._action, action["prompt"])
            }
            command_menu_items.append(tmp)

        self._command_menu:QMenu = QMenu(self)
        for item in command_menu_items:
            action = QAction(item["text"], self)
            action.triggered.connect(item["connect"])
            self._command_menu.addAction(action)

        tray_menu_items = [
            {"text": "显示/隐藏", "connect": self._show_or_hide},
            {"text": "Anything v4.5", "connect": self._browse_anything_ai},
            {"text": "Protogen Diffusion", "connect": self._browse_protogen_ai},
            {"text": "写作(Writing)", "connect": self._browse_writing},
            {"text": "聊天室", "connect": self._browse_chatroom},
            {"text": "退出", "connect": qApp.quit}
        ]

        self._tray_menu = QMenu(self)

        for item in tray_menu_items:
            action = QAction(item["text"], self)
            action.triggered.connect(item["connect"])
            self._tray_menu.addAction(action)

        self.tray = QSystemTrayIcon(self)
        self.tray.setIcon(QIcon('resources/icon.png'))
        self.tray.setContextMenu(self._tray_menu)
        self.tray.show()

    def mouseDoubleClickEvent(self, event:QMouseEvent) -> None:
        if event.button() == Qt.LeftButton:
            input_dialog = QInputDialog(self)
            input_dialog.setInputMode(QInputDialog.TextInput)
            input_dialog.setLabelText("你想和我说什么~")
            input_dialog.setWindowTitle(" ")
            input_dialog.resize(500, 100)
            input_dialog.show()
            if input_dialog.exec_() == input_dialog.Accepted:
                message:str = input_dialog.textValue()
                self._chat_thread = ChatThread()
                self._chat_thread.message = message
                self._chat_thread.finished.connect(self.on_chat)
                self._chat_thread.start()

    def mousePressEvent(self, event:QMouseEvent) -> None:
        if event.button() == Qt.LeftButton:
            self._dragging:bool = True
            self._drag_position:QPoint = event.globalPos() - self.pos()
            self._text_window.hide()
        event.accept()

    def mouseMoveEvent(self, event:QMouseEvent) -> None:
        if self._dragging:
            self.move(event.globalPos() - self._drag_position)
        event.accept()

    def mouseReleaseEvent(self, event:QMouseEvent) -> None:
        if event.button() == Qt.LeftButton:
            self._dragging = False
        event.accept()

    def dragEnterEvent(self, event:QDragEnterEvent) -> None:
        if event.mimeData().hasText():
            event.acceptProposedAction()
        event.accept()

    def dropEvent(self, event: QDropEvent) -> None:
        if event.mimeData().hasText():
            self._dropped_text = event.mimeData().text()
            self._command_menu.exec_( self.mapToGlobal( event.pos() ) )
        event.accept()

    def contextMenuEvent(self, event):
        self._command_menu.exec_( self.mapToGlobal( event.pos() ) )
        event.accept()

    def _action(self, prompt_format:str):
        if not self._is_thinking:
            if not self._dropped_text:
                clipboard = qApp.clipboard()
                if clipboard.mimeData().hasText():
                    self._dropped_text = clipboard.text()

            self._is_thinking = True
            self._text_window.show()
            self._text_window.set_process_style()
            self._text_window.set_width(600)
            self._text_window.move(self.x() - (self._text_window.width() - self.width()), self.y() - self._text_window.height())
            self._text_window.set_plain_text("思考中……")
            self._worker_thread = WorkerThread()
            self._worker_thread.prompt = prompt_format.format(self._dropped_text)
            self._worker_thread.update.connect(self.on_update_text)
            self._worker_thread.finished.connect(self.finished)
            self._worker_thread.start()
        else:
            self._text_window.set_plain_text("还有工作正在进行中……")

    def on_update_text(self, rev_msg:str):
        self._text_window.set_plain_text(rev_msg)

    def finished(self):
        self._text_window.set_success_style()
        self._dropped_text = None
        self._is_thinking = False

    def on_chat(self, rev_msg):
        if not self._text_window.isVisible():
            self._text_window.show()
            self._text_window.set_width(300)
            self._text_window.move(self.x() - (self._text_window.width() - self.width()), self.y() - self._text_window.height())
            self._timer.start(5000)
        self._text_window.set_plain_text(rev_msg)

    def _on_timer_stop(self):
        self._text_window.hide()
        self._timer.stop()

    def _browse_anything_ai(self) -> None:
        webbrowser.open("https://camenduru-webui-docker.hf.space/")

    def _browse_protogen_ai(self) -> None:
        webbrowser.open("https://darkstorm2150-protogen-web-ui.hf.space/")

    def _browse_writing(self) -> None:
        web_host:str = client_config["web_host"]
        bot_id:str = client_config["default_bot"]
        webbrowser.open( "{}/{}/write".format(web_host, bot_id) )

    def _browse_chatroom(self) -> None:
        web_host:str = client_config["web_host"]
        bot_id:str = client_config["default_bot"]
        webbrowser.open( "{}/{}/chatroom".format(web_host, bot_id) )

    def _show_or_hide(self) -> None:
        if self.isVisible():
            self.hide()
            self._text_window.hide()
        else:
            self.show()
