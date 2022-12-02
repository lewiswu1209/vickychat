
from enum import Enum

class Action(Enum):
    UNDEFINED = 0
    WORKING = 1
    SLEEPING = 2
    WAY_TO_WORK = 4
    WAY_TO_HOME = 8
    AT_HOME = 16

Action.UNDEFINED.label = None
Action.WORKING.label = "正在工作"
Action.SLEEPING.label = "正在睡觉"
Action.WAY_TO_WORK.label = "在去上班的路上"
Action.WAY_TO_HOME.label = "在回家的路上"
Action.AT_HOME.label = "在家里"
