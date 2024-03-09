from enum import Enum


class NodeStatus(Enum):
    CLEAN = 1
    DIRTY = 2
    ERROR = 3
