
import time

from robot.memery.memery_type import MemeryType

class Memery:
    def __init__(self) -> None:
        self.memery_list:list[dict] = []

    def add_memery(self, type:MemeryType, data:dict) -> None:
        memery:dict = {
            "timestap": time.time(),
            "type": type,
            "data": data
        }
        self.memery_list.append(memery)

    def get_last_memery_list(self, memery_type:MemeryType, n:int) -> list[dict]:
        memery_list:list[dict] = []
        for memery in reversed( self.memery_list ):
            if len(memery_list) < n:
                if memery_type is not None:
                    if memery["type"] == memery_type:
                        memery_list.insert(0, memery)
                else:
                    memery_list.insert(0, memery)
            else:
                break
        return memery_list
