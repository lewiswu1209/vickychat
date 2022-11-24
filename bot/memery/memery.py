
import time

from bot.utils.time_utils import get_interval_minutes_by_timestamp
from bot.utils.time_utils import get_time_str_by_timestamp

class Memery:
    def __init__(self):
        self.memery = []

    def add_memery(self, data):
        memery = {
            "timestap": time.time(),
            "data": data
        }
        self.memery.append(memery)

    def get_last_memery(self, n):
        return self.memery[-n:]

    def get_prompt_by_last_memery(self, n):
        memery = self.get_last_memery(n)
        prompt = ""
        prep = None
        for item in memery:
            if prep is not None and get_interval_minutes_by_timestamp(item["timestap"], prep["timestap"]) < 15:
                pass
            else:
                prompt += "现在是%s\n" % get_time_str_by_timestamp( item["timestap"] )
            prompt += "%s：%s\n" % (item["data"]["speaker"], item["data"]["message"])
            prep = item
        return prompt
