from enum import Enum, auto

from util.serialization import senum

@senum
class BodyType(Enum):
    Dynamic = auto()
    Kinematic = auto()
    Static = auto()