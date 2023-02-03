
import sys
import requests

from config.config import client_config

if __name__ == "__main__":
    web_host:str = client_config["web_host"]
    message:str = sys.argv[1]
    bot_id:str = client_config["default_bot"]
    speaker:str = client_config["name"]

    url:str = "{}/api_v1/{}/chat?speaker={}&message={}".format(web_host, bot_id, speaker, message)
    rs:dict = requests.get(url).json()
    if rs["code"]==0:
        for item in rs["data"]["response"]:
            print("{}:{}".format(item["speaker"], item["message"]))
    else:
        print(rs["msg"])
