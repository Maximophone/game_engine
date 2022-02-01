from enum import Enum, auto

class EventType(Enum):
    GameEngineStartPlay = auto()
    GameEngineStopPlay = auto()
    SaveLevel = auto()
    LoadLevel = auto()
    UserEvent = auto()