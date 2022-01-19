from typing import List
from mxeng.component import Component
from pyrr import vector4
import numpy as np

from renderer.texture import Texture


class SpriteRenderer(Component):
    def __init__(self, color: vector4 = None, texture: Texture = None):
        self._color: vector4 = color if color is not None else vector4.create(1., 1., 1., 1.)
        self._tex_coords: List[np.ndarray] = [
            np.array([1,1]),
            np.array([1,0]),
            np.array([0,0]),
            np.array([0,1])
        ]
        self._texture: Texture = texture
        super().__init__()

    def start(self):
        pass

    def update(self, dt):
        pass

    def get_color(self) -> vector4:
        return self._color

    def get_texture(self) -> Texture:
        return self._texture
    
    def get_tex_coords(self) -> List[np.ndarray]:
        return self._tex_coords