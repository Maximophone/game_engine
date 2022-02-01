from enum import Enum, auto


class BodyType(Enum):
    Dynamic = auto()
    Kinematic = auto()
    Static = auto()