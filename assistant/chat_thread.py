
import requests

from PyQt5.QtCore import QThread
from PyQt5.QtCore import pyqtSignal

from config.config import client_config

class ChatThread(QThread):
    finished = pyqtSignal(str)

    def __init__(self, parent=None):
        super(ChatThread, self).__init__(parent)
        self.message = ""

    def run(self):
        web_host:str = client_config["web_host"]
        bot_id:str = client_config["default_bot"]
        speaker:str = client_config["name"]

        url:str = "{}/api_v1/{}/chat?speaker={}&message={}".format(web_host, bot_id, speaker, self.message)
        rs:dict = requests.get(url).json()

        if rs["code"]==0:
            for item in rs["data"]["response"]:
                self.finished.emit( item["message"] )
