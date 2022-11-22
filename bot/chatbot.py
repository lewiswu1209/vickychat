
import json

import bot.core.bloomz as bloomz

from random import randint
from datetime import datetime

from config.config import api_token
from bot.disposition import Disposition
from bot.utils.time_utils import get_year_diff
from bot.utils.time_utils import get_current_time_str

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
            profile_str += ","
            profile_str += item

        return profile_str + "\n"

    def __get_disposition(self):
        context = ""

        for item in self.disposition:
            context += "%s：%s\n" % (item["speaker"], item["message"])

        return context

    def __get_context(self, history_list):
        context = ""

        for item in history_list[-10:]:
            context += "%s：%s\n" % (item["speaker"], item["message"])

        return context

    def __get_prompt(self, history_list=[]):
        prompt = self.__get_profile_str()
        prompt += self.__get_disposition()
        prompt += self.__get_context(history_list)

        return prompt

    def update_profile(self, profile:dict):
        self.profile = profile

    def chat(self, input, history_list=[]):
        generated_text_list = []

        seed = randint(1, 512)

        prompt = self.__get_prompt(history_list)
        prompt += "现在是%s\n" % get_current_time_str()
        prompt += "%s：%s\n" % (input["speaker"], input["message"])
        prompt += "%s：" % self.profile["NAME"]

        while len(generated_text_list) == 0:
            output = bloomz.sample( prompt, seed, 0.7,api_token)
            if output:
                output = output[( len(prompt)-len(self.profile["NAME"] + "：") ):]
                # is_finished = False
                # for line in output.split("\n"):
                #     line = line.replace(", ", ",")
                #     for generated in line.split(" "):
                #         generated = generated.strip(" ")
                #         if generated.startswith(self.profile["NAME"] + "："):
                #             message = generated[len(self.profile["NAME"] + "："):]
                #             if message and message != "":
                #                 generated_text_list.append({"speaker": self.profile["NAME"], "message": message})
                #         else:
                #             is_finished = True
                #             break
                #     if is_finished:
                #         break
                for line in output.split("\n"):
                    # line = line.replace(", ", ",")
                    # for generated in line.split(" "):
                        generated = line.strip(" ")
                        if generated.startswith(self.profile["NAME"] + "："):
                            message = generated[len(self.profile["NAME"] + "："):]
                            if message and message != "":
                                generated_text_list.append({"speaker": self.profile["NAME"], "message": message})
                        else:
                            # is_finished = True
                            break
                    # if is_finished:
                    #     break
        return generated_text_list
