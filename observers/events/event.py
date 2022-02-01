from observers.events.event_type import EventType


class Event:
    def __init__(self, typ: EventType):
        self.type: EventType = typ