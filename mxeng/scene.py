from abc import abstractmethod
from typing import List

from mxeng.game_object import GameObject
from mxeng.camera import Camera
from renderer.renderer import Renderer

import imgui

from util.serialization import serializable

@serializable("_is_running", "_game_objects", "_camera")
class Scene:
    def __init__(self):
        self._is_running = False
        self._game_objects: List[GameObject] = []
        self._camera: Camera = None
        self._renderer: Renderer = Renderer()
        self._active_game_object: GameObject = None
 
    @abstractmethod
    def update(self, dt: float):
        pass

    @abstractmethod
    def init(self):
        pass

    def start(self):
        for go in self._game_objects:
            go.start()
            self._renderer.add(go)
        self._is_running = True

    def add_game_object_to_scene(self, go: GameObject):
        if not self._is_running:
            self._game_objects.append(go)
        else:
            self._game_objects.append(go)
            go.start()
            self._renderer.add(go)

    def camera(self):
        return self._camera

    def scene_imgui(self):
        if self._active_game_object is not None:
            imgui.begin("Inspector", True)
            self._active_game_object.imgui()
            imgui.end()

        self.imgui()

    def imgui(self):
        pass
    