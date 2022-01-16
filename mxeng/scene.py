from abc import abstractmethod
from typing import List

from mxeng.game_object import GameObject


class Scene:
    def __init__(self):
        self._is_running = False
        self._game_objects: List[GameObject] = []
 
    @abstractmethod
    def update(self, dt: float):
        pass

    @abstractmethod
    def init(self):
        pass

    def start(self):
        for go in self._game_objects:
            go.start()
        self._is_running = True

    def add_game_object_to_scene(self, go: GameObject):
        if not self._is_running:
            self._game_objects.append(go)
        else:
            self._game_objects.append(go)
            go.start()