from typing import List
from components.sprite import Sprite
from mxeng.component import Component
from pyrr import vector4
import numpy as np

from renderer.texture import Texture


class SpriteRenderer(Component):
    def __init__(self, color: vector4 = None, sprite: Sprite = None):
        self._color: vector4 = color if color is not None else vector4.create(1., 1., 1., 1.)
        self._sprite: Sprite = sprite if sprite is not None else Sprite()
        super().__init__()

    def start(self):
        pass

    def update(self, dt):
        pass

    def get_color(self) -> vector4:
        return self._color

    def get_texture(self) -> Texture:
        return self._sprite.get_texture()
    
    def get_tex_coords(self) -> List[np.ndarray]:
        return self._sprite.get_tex_coords()