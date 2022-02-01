from abc import abstractmethod
from typing import List, Optional
import json
from components.component import Component
from components.transform import Transform

from mxeng.game_object import GameObject
from mxeng.camera import Camera
from renderer.renderer import Renderer

import imgui

from util.serialization import deserialize, serializable, serialize

class Scene:
    def __init__(self):
        self._is_running = False
        self._game_objects: List[GameObject] = []
        self._camera: Camera = None
        self._level_loaded: bool = False
 
    @abstractmethod
    def update(self, dt: float):
        pass

    @abstractmethod
    def render(self):
        pass

    @abstractmethod
    def init(self):
        pass

    def start(self):
        for go in self._game_objects:
            go.start()
            Renderer.add(go)
        self._is_running = True

    def add_game_object_to_scene(self, go: GameObject):
        if not self._is_running:
            self._game_objects.append(go)
        else:
            self._game_objects.append(go)
            go.start()
            Renderer.add(go)

    def get_game_object(self, game_object_id: int) -> Optional[GameObject]:
        return next((go for go in self._game_objects if go.uid == game_object_id), None)

    def create_game_object(self, name: str, transform: Transform = None) -> GameObject:
        transform = transform or Transform()
        go: GameObject = GameObject(name)
        go.add_component(transform)
        # self.add_game_object_to_scene(go)
        return go

    def camera(self):
        return self._camera

    def imgui(self):
        pass
    
    def save_exit(self):
        with open("level.txt", "w") as f:
            json.dump(serialize([go for go in self._game_objects if go.do_serialize]), f, indent=4)

    def load(self):
        try:
            max_go_id = -1
            max_comp_id = -1

            with open("level.txt", "r") as f:
                game_objects: List[GameObject] = deserialize(json.load(f))
                for go in game_objects:
                    self.add_game_object_to_scene(go)

                    for c in go.components:
                        if c.uid > max_comp_id:
                            max_comp_id = c.uid

                    if go.uid > max_go_id:
                        max_go_id = go.uid
            max_go_id += 1
            max_comp_id += 1
            GameObject.init(max_go_id)
            Component.init(max_comp_id)

            self._level_loaded = True
        except FileNotFoundError:
            pass
