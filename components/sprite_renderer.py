from typing import List
from components.sprite import Sprite
from mxeng.component import Component
from mxeng.transform import Transform
from pyrr import vector4
import numpy as np
import imgui.core

from renderer.texture import Texture
from util.serialization import serializable, sproperty

@serializable("_color", "_sprite", "_is_dirty")
class SpriteRenderer(Component):
    def __init__(self, color: vector4 = None, sprite: Sprite = None):
        self._color: vector4 = color if color is not None else vector4.create(1., 1., 1., 1.)
        self._sprite: Sprite = sprite if sprite is not None else Sprite()
        self._last_transform: Transform = None
        self._is_dirty = True
        super().__init__()

    def start(self):
        self._last_transform = self.game_object.transform.copy()

    def update(self, dt):
        # print(self._last_transform.position, self.game_object.transform.position)
        if not self._last_transform == self.game_object.transform:
            self.game_object.transform.copy(to=self._last_transform)
            self._is_dirty = True

    def imgui(self):
        changed, new_color = imgui.color_edit4("Color picker", *self.get_color())
        if changed:
            self.set_color(np.array(new_color))

    def get_color(self) -> vector4:
        return self._color

    def get_texture(self) -> Texture:
        return self._sprite.get_texture()
    
    def get_tex_coords(self) -> List[np.ndarray]:
        return self._sprite.get_tex_coords()

    def set_sprite(self, sprite: Sprite):
        self._sprite = sprite
        self._is_dirty = True

    def set_color(self, color: vector4):
        if all(self._color == color):
            return
        self._color[:] = color.copy()
        self._is_dirty = True

    def is_dirty(self) -> bool:
        return self._is_dirty

    def set_clean(self):
        self._is_dirty = False
