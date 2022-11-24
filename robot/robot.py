
from random import randint
from datetime import datetime

import robot.core.bloomz as bloomz

from robot.memery import Memery
from robot.memery import MemeryType

from config import api_token

from utils.time_utils import get_current_datetime_str
from utils.time_utils import get_datetime_str_by_timestamp
from utils.time_utils import get_interval_years_by_date_str
from utils.time_utils import get_interval_minutes_by_timestamp

class Robot:
    def __init__(self, profile:dict) -> None:
        self.profile:dict = profile
        self.memery:Memery = Memery()

    def __get_profile_str(self) -> str:
        profile_str:str = "{}，{}，生日{}年{}月{}日，{}岁".format(
            self.profile["NAME"],
            self.profile["GENDER"],
            self.profile["YEAROFBIRTH"],
            self.profile["MONTHOFBIRTH"],
            self.profile["DAYOFBIRTH"],
            get_interval_years_by_date_str(
                self.profile["YEAROFBIRTH"] + "-" + self.profile["MONTHOFBIRTH"] + "-" + self.profile["DAYOFBIRTH"],
                datetime.now().strftime("%Y-%m-%d")
            )
        )
        for describe in self.profile["DESCRIBE"]:
            profile_str += "，"
            profile_str += describe
        profile_str += "。"

        return profile_str + "\n"

    def __get_prompt_by_last_memery(self, n:int) -> str:
        memery_list:list[dict] = self.memery.get_last_memery_list(MemeryType.CHAT, n)
        prompt:str = ""
        prep_memery:dict = None
        for cur_memery in memery_list:
            if prep_memery is not None and get_interval_minutes_by_timestamp(cur_memery["timestap"], prep_memery["timestap"]) < 15:
                pass
            else:
                prompt += "\n现在是%s\n" % get_datetime_str_by_timestamp( cur_memery["timestap"] )
            prompt += "%s：%s\n" % (cur_memery["data"]["speaker"], cur_memery["data"]["message"])
            prep_memery = cur_memery

        return prompt

    def __get_prompt(self) -> str:
        prompt:str = self.__get_profile_str()
        prompt += self.__get_prompt_by_last_memery(16)

        return prompt

    def update_profile(self, profile:dict) -> None:
        self.profile = profile

    def chat(self, input:dict) -> list[str]:
        generated_text_list:list[dict] = []

        seed:int = randint(1, 512)

        prompt:str = self.__get_prompt()
        prompt += "\n现在是%s\n" % get_current_datetime_str()
        prompt += "%s：%s\n" % (input["speaker"], input["message"])
        prompt += "%s：" % self.profile["NAME"]

        self.memery.add_memery(MemeryType.CHAT, input)
        while len(generated_text_list) == 0:
            output:str = bloomz.sample( prompt, seed, 0.65,api_token)
            if output:
                output:str = output[( len(prompt)-len(self.profile["NAME"] + "：") ):]
                for line in output.split("\n"):
                    generated:str = line.strip(" ")
                    if generated.startswith(self.profile["NAME"] + "："):
                        message:str = generated[len(self.profile["NAME"] + "："):]
                        if message and message != "":
                            generated_text_list.append({"speaker": self.profile["NAME"], "message": message})
                            self.memery.add_memery(MemeryType.CHAT, {"speaker": self.profile["NAME"], "message": message})
                    else:
                        break
        return generated_text_list
