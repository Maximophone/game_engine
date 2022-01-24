import numpy as np
from typing import List

from renderer.texture import Texture
from util.serialization import serializable, sproperty

@serializable("_texture", "_tex_coords")
class Sprite:
    def __init__(self, texture: Texture = None, tex_coords: List[np.ndarray] = None):
        self._width: float = None
        self._height: float = None
        self._text_id: int = None
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

    @sproperty
    def width(self) -> float:
        return self._width

    @width.setter
    def width(self, value: float):
        self._width = value

    @sproperty
    def height(self) -> float:
        return self._height

    @height.setter
    def height(self, value: float):
        self._height = value

    @property
    def tex_id(self) -> int:
        return -1 if self._texture is None else self._texture.tex_id