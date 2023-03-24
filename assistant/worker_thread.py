
import time
import requests

from PyQt5.QtCore import QThread
from PyQt5.QtCore import pyqtSignal

from config.config import client_config

class WorkerThread(QThread):
    update = pyqtSignal(str)
    finished = pyqtSignal()

    def __init__(self, parent=None):
        super(WorkerThread, self).__init__(parent)
        self.prompt = ""

    def run(self):
        web_host:str = client_config["web_host"]
        bot_id:str = client_config["default_bot"]
        url:str = "{}/api_v1/{}/write".format(web_host, bot_id)

        all_generated_text = ""

        while(True):
            prompt: str = "----------\n{}".format(self.prompt)
            rs:dict = requests.post(url, data={"prompt":prompt}).json()

            if rs["code"]==0:
                generated_text = rs["data"]["generated_text"].split("----------")[0]
                if generated_text != "":
                    for char in generated_text:
                        all_generated_text += char
                        self.prompt += char
                        self.update.emit( all_generated_text )
                        time.sleep(0.05)
                else:
                    self.finished.emit()
                    break
            else:
                self.update.emit( rs["msg"] )
                break
