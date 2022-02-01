from observers.events.event_type import EventType


class Event:
    def __init__(self, typ: EventType = EventType.UserEvent):
        self.type: EventType = typ