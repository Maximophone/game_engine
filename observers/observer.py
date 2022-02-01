from observers.events.event import Event
from mxeng.game_object import GameObject

class Observer:
    def on_notify(self, obj: GameObject, event: Event):
        pass