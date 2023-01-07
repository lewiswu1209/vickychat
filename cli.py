
import sys
import requests

from config.config import chat_config

if __name__ == "__main__":
    msg = sys.argv[1]
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
            print("{}:{}".format(item["speaker"], item["message"]))
