from enum import Enum, auto
from util.serialization import senum

@senum
class Direction(Enum):
    Down = auto()
    Up = auto()
    Right = auto()
    Left = auto()