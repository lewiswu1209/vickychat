
import json

from random import randint
from datetime import datetime

import bot.core.bloomz as bloomz

from bot.disposition import Disposition
from bot.utils.time_utils import get_year_diff

from config.config import api_token

class Chatbot:
    def __init__(self, profile:dict, disposition:Disposition):
        self.profile = profile

        try:
            self.disposition = json.load( open("data/disposition/" + disposition.value, "r", encoding="utf-8") )
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
            context += term["speaker"] + "：" + term["message"] + "\n"

        return context

    def __get_context(self, history_list):
        context = ""
        for item in history_list[-10:]:
            context += item["speaker"] + "：" + item["message"] + "\n"

        return context

    def __get_prompt(self, history_list=[]):
        prompt = self.__get_profile_str()
        prompt += self.__get_disposition()
        prompt += self.__get_context(history_list)

        return prompt

    def update_profile(self, profile:dict):
        self.profile = profile

    def chat(self, input, history_list=[]):
        seed = randint(1, 512)

        prompt = self.__get_prompt(history_list)
        prompt += input["speaker"] + "：" + input["message"] + "\n"
        prompt += self.profile["NAME"] + "："

        generated_text = bloomz.sample( prompt, seed, 0.7,api_token)
        if generated_text:
            generated_text_list = generated_text.split(input["speaker"] + "：")
            generated_text_list = generated_text_list[0].split(self.profile["NAME"] + "：")
            fixed_generated_text = generated_text_list[0].strip(" \n")

            return {
                "speaker" : self.profile["NAME"],
                "message" : fixed_generated_text
            }
        else:
            return None
