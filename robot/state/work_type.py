
from enum import Enum

from utils.day_type import DayType

from robot.state.action import Action

class WorkType(Enum):
    NORMAL = {
        DayType.WorkDay: [Action.SLEEPING, Action.SLEEPING, Action.SLEEPING, Action.SLEEPING, Action.SLEEPING, Action.SLEEPING, Action.SLEEPING, Action.SLEEPING,
            Action.WAY_TO_WORK, Action.WORKING, Action.WORKING, Action.WORKING, Action.UNDEFINED, Action.UNDEFINED,
            Action.WORKING, Action.WORKING, Action.WORKING, Action.WORKING, Action.WAY_TO_HOME,
            Action.AT_HOME, Action.AT_HOME, Action.AT_HOME, Action.AT_HOME, Action.SLEEPING
        ],
        DayType.Weekend: [Action.SLEEPING, Action.SLEEPING, Action.SLEEPING, Action.SLEEPING, Action.SLEEPING, Action.SLEEPING, Action.SLEEPING, Action.SLEEPING,
            Action.UNDEFINED, Action.UNDEFINED, Action.UNDEFINED, Action.UNDEFINED, Action.UNDEFINED, Action.UNDEFINED,
            Action.UNDEFINED, Action.UNDEFINED, Action.UNDEFINED, Action.UNDEFINED, Action.UNDEFINED,
            Action.AT_HOME, Action.AT_HOME, Action.AT_HOME, Action.AT_HOME, Action.SLEEPING
        ],
        DayType.Holiday: [Action.SLEEPING, Action.SLEEPING, Action.SLEEPING, Action.SLEEPING, Action.SLEEPING, Action.SLEEPING, Action.SLEEPING, Action.SLEEPING,
            Action.UNDEFINED, Action.UNDEFINED, Action.UNDEFINED, Action.UNDEFINED, Action.UNDEFINED, Action.UNDEFINED,
            Action.UNDEFINED, Action.UNDEFINED, Action.UNDEFINED, Action.UNDEFINED, Action.UNDEFINED,
            Action.AT_HOME, Action.AT_HOME, Action.AT_HOME, Action.AT_HOME, Action.SLEEPING
        ]
    }
