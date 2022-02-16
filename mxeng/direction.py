from enum import Enum, auto
from util.serialization import senum

@senum
class Direction(Enum):
    Down = auto()
    Up = auto()
    Left = auto()
    Right = auto()