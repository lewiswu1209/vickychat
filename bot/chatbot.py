
import json

from datetime import datetime

import core.glm_130B  as glm

from bot.disposition import Disposition
from utils.time_utils import get_year_diff

class Chatbot:
    def __init__(self, profile:dict, disposition:Disposition):
        self.profile = profile

        try:
            self.disposition = json.load( open("data/disposition/" + disposition.value, "r") )
            for item in self.disposition:
                if item["speaker"]=="bot":
                    item["speaker"] = self.profile["NAME"]
        except:
            self.disposition = []

    def __get_profile_str(self):
        profile_str = "{},{},生日{}年{}月{}日,{}岁".format(
            self.profile["NAME"],
            self.profile["GENDER"],
            self.profile["YEAROFBIRTH"],
            self.profile["MONTHOFBIRTH"],
            self.profile["DAYOFBIRTH"],
            get_year_diff(
                self.profile["YEAROFBIRTH"] + "-" + self.profile["MONTHOFBIRTH"] + "-" + self.profile["DAYOFBIRTH"],
                datetime.now().strftime("%Y-%m-%d")
            )
        )

        for item in self.profile["DESCRIBE"]:
            profile_str += "," + item

        return profile_str + "\n"

    def __get_disposition(self):
        context = ""
        for term in self.disposition:
            context += term["speaker"] + "：" + term["content"] + "\n"

        return context

    def __get_context(self, history_list):
        context = ""
        for item in history_list[-4:]:
            context += item["speaker"] + "：" + item["content"] + "\n"

        return context

    def __get_prompt(self, history_list=[]):
        prompt = self.__get_profile_str()
        prompt += self.__get_disposition()
        prompt += self.__get_context(history_list)

        return prompt

    def chat(self, input, history_list=[]):
        max_length = 512
        temperature = 0.5
        top_k = 1
        top_p = 0
        stop_words = ["\n"]
        presence_penalty = 2
        frequency_penalty = 2

        prompt = self.__get_prompt(history_list)
        prompt += input["speaker"] + "：" + input["content"] + "\n"
        prompt += self.profile["NAME"] + "：[MASK]"

        forecast = glm.base_strategy_search(prompt, max_length, temperature, top_k, top_p, stop_words, presence_penalty, frequency_penalty)

        return {
            "speaker" : self.profile["NAME"],
            "content" : forecast[0]
        }
