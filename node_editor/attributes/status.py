from enum import Enum


class NodeStatus(Enum):
    CLEAN = 0
    WARNING = -1
    ERROR = 1
