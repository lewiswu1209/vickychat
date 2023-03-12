
import time
import requests

from PyQt5.QtCore import QThread
from PyQt5.QtCore import pyqtSignal

from config.config import client_config

class WorkerThread(QThread):
    finished = pyqtSignal(str)

    def __init__(self, parent=None):
        super(WorkerThread, self).__init__(parent)
        self.prompt = ""

    def run(self):
        web_host:str = client_config["web_host"]
        bot_id:str = client_config["default_bot"]
        url:str = "{}/api_v1/{}/write".format(web_host, bot_id)

        all_generated_text = ""

        while(True):
            rs:dict = requests.post(url, data={"prompt":self.prompt}).json()

            if rs["code"]==0:
                generated_text = rs["data"]["generated_text"]
                if generated_text != "":
                    for chat in generated_text:
                        all_generated_text += chat
                        self.prompt += chat
                        self.finished.emit( all_generated_text )
                        time.sleep(0.05)
                else:
                    break
            else:
                self.finished.emit( rs["msg"] )
                break
