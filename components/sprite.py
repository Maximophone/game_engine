import numpy as np
from typing import List

from renderer.texture import Texture
from util.serialization import serializable

@serializable("_texture", "_tex_coords")
class Sprite:
    def __init__(self, texture: Texture = None, tex_coords: List[np.ndarray] = None):
        self._texture = texture
        self._tex_coords: List[np.ndarray] = [
            np.array([1,1]),
            np.array([1,0]),
            np.array([0,0]),
            np.array([0,1])
        ] if tex_coords is None else tex_coords

    def get_texture(self):
        return self._texture

    def get_tex_coords(self):
        return self._tex_coords