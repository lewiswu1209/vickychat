
import datetime

from robot.state.action import Action
from robot.state.work_type import WorkType
from robot.state.disposition import Disposition

from utils.day_type import DayType
from utils.time_utils import get_datetype_by_date

class State:
    def __init__(self) -> None:
        self.profile:dict = {}
        self.describe_list:list[str] = []
        self.disposition:Disposition = Disposition.NORMAL
        self.work_type:WorkType = WorkType.NORMAL

    def update_profile(self, profile:dict) -> None:
        self.profile = profile

    def update_disposition(self, disposition:Disposition) -> None:
        self.disposition = disposition

    def update_work_type(self, work_type:WorkType) -> None:
        self.work_type = work_type

    def add_describe(self, describe) -> None:
        self.describe_list.append(describe)

    def clear_describe(self) -> None:
        self.describe_list = []

    def update_describe_list(self, describe_list:list[str]) -> None:
        self.describe_list = describe_list

    def get_action_by_datetime(self, date_time:datetime.datetime) -> Action:
        date:datetime.date = date_time.date()
        datetype:DayType = get_datetype_by_date(date)
        action_list:list[Action] = self.work_type.value[datetype]
        hour:int = date_time.hour
        return action_list[hour]
