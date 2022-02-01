from typing import List
from mxeng.game_object import GameObject
from observers.events.event import Event

from observers.observer import Observer


class EventSystem:
    observers: List[Observer] = []

    @staticmethod
    def add_observer(observer: Observer):
        EventSystem.observers.append(observer)

    @staticmethod
    def notify(obj: GameObject, event: Event):
        for observer in EventSystem.observers:
            observer.on_notify(obj, event)