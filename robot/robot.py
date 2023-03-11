
from random import randint
from datetime import datetime

import robot.core.bloomz as bloomz

from config import api_token

from robot.state import State
from robot.memery import Memery
from robot.memery import MemeryType
from robot.state.action import Action

from utils.time_utils import get_current_datetime
from utils.time_utils import get_datetime_str_by_datetime
from utils.time_utils import get_datetime_str_by_timestamp
from utils.time_utils import get_interval_years_by_date_str
from utils.time_utils import get_interval_minutes_by_timestamp

class Robot:
    def __init__(self, settings:dict) -> None:
        self.memery:Memery = Memery()
        self.state:State = State()

        self.state.update_profile(settings)
        self.state.update_describe_list(settings["DESCRIBE"])
        self.state.update_example_list(settings["EXAMPLES"])

    def __get_profile_str(self) -> str:
        profile = self.state.profile

        profile_str:str = "{}，{}，生日{}年{}月{}日，{}岁".format(
            profile["NAME"],
            profile["GENDER"],
            profile["YEAROFBIRTH"],
            profile["MONTHOFBIRTH"],
            profile["DAYOFBIRTH"],
            get_interval_years_by_date_str(
                profile["YEAROFBIRTH"] + "-" + profile["MONTHOFBIRTH"] + "-" + profile["DAYOFBIRTH"],
                datetime.now().strftime("%Y-%m-%d")
            )
        )
        for describe in self.state.describe_list:
            profile_str += "，"
            profile_str += describe
        profile_str += "。"

        return profile_str + "\n"

    def __get_prompt_by_examples(self) -> str:
        example_list:list[dict] = self.state.example_list
        prompt:str = ""
        for example in example_list:
            prompt += "{%s：%s}\n" % (example["speaker"], example["message"])

        return prompt

    def __get_prompt_by_last_memery(self, n:int) -> str:
        memery_list:list[dict] = self.memery.get_last_memery_list(MemeryType.CHAT, n)
        prompt:str = ""
        prep_memery:dict = None
        for cur_memery in memery_list:
            if prep_memery is not None and get_interval_minutes_by_timestamp(cur_memery["timestap"], prep_memery["timestap"]) < 15:
                pass
            else:
                prompt += "\n现在是%s\n" % get_datetime_str_by_timestamp( cur_memery["timestap"] )
            prompt += "{%s：%s}\n" % (cur_memery["data"]["speaker"], cur_memery["data"]["message"])
            prep_memery = cur_memery

        return prompt

    def __get_prompt(self) -> str:
        prompt:str = self.__get_profile_str()
        prompt += self.__get_prompt_by_examples()
        prompt += self.__get_prompt_by_last_memery(10)

        return prompt

    def chat(self, input:dict) -> list[str]:
        current_datetime:datetime = get_current_datetime()
        action:Action = self.state.get_action_by_datetime(current_datetime)

        prompt:str = self.__get_prompt()
        prompt += "\n现在是%s\n" % get_datetime_str_by_datetime(current_datetime)
        if action.label:
            prompt += "%s%s\n" % ( self.state.profile["NAME"], action.label )
        prompt += "{%s：%s}\n" % (input["speaker"], input["message"])
        prompt += "{%s：" % self.state.profile["NAME"]

        self.memery.add_memery(MemeryType.CHAT, input)

        generated_text_list:list[dict] = []
        seed:int = randint(1, 512)
        output:str = bloomz.sample(prompt, 64, seed, 1, 0.65, api_token)
        if type(output) == int:
            generated_text_list.append({"speaker": self.state.profile["NAME"], "message": "BLOOM API HTTP ERROR {}".format(output)})
        elif type(output) == str:
            output:str = output[( len(prompt)-len("{" + self.state.profile["NAME"] + "：") ):]
            for line in output.split("}"):
                generated:str = line
                # if generated.startswith(self.state.profile["NAME"] + "："):
                #     message:str = generated[len(self.state.profile["NAME"] + "："):]
                #     if message and message != "":
                #         generated_text_list.append({"speaker": self.state.profile["NAME"], "message": message})
                #         self.memery.add_memery(MemeryType.CHAT, {"speaker": self.state.profile["NAME"], "message": message})
                # el
                if generated.startswith("{" + self.state.profile["NAME"] + "："):
                    message:str = generated[len("{" + self.state.profile["NAME"] + "："):]
                    if message and message != "":
                        generated_text_list.append({"speaker": self.state.profile["NAME"], "message": message})
                        self.memery.add_memery(MemeryType.CHAT, {"speaker": self.state.profile["NAME"], "message": message})
                else:
                    break
        if len(generated_text_list) == 0:
            generated_text_list.append({"speaker": self.state.profile["NAME"], "message": "……"})
        return generated_text_list

    def write(self, prompt):
        seed:int = randint(1, 512)
        output:str = bloomz.sample(prompt, 256, seed, 1, 0.65, api_token)
        rs = ""
        if type(output) == int:
            rs = "BLOOM API HTTP ERROR {}".format(output)
        if type(output) == str:
            rs = output[len(prompt):]
        else:
            rs = "ERROR"
        return rs
