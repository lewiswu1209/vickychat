
import time
import requests

from PyQt5.QtCore import QThread
from PyQt5.QtCore import pyqtSignal

from config.config import client_config

class WorkerThread(QThread):
    update = pyqtSignal(str, int, bool)
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
                splited_rs:list = rs["data"]["generated_text"].split("\n----------")
                generated_text = splited_rs[0]
                if generated_text != "":
                    for char in generated_text:
                        all_generated_text += char
                        self.prompt += char
                        self.update.emit( all_generated_text, 4, False )
                        time.sleep(0.02)
                    if len( splited_rs ) > 1:
                        self.finished.emit()
                        break
                else:
                    self.finished.emit()
                    break
            else:
                self.update.emit( rs["msg"], 4, False )
                self.finished.emit()
                break
