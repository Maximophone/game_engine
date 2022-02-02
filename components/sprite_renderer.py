from typing import List
from components.sprite import Sprite
from components.component import Component
from components.transform import Transform
import numpy as np
import imgui.core

from renderer.texture import Texture
from util.serialization import serializable, sproperty
from util.vectors import Color4

@serializable("_color", "_sprite")
class SpriteRenderer(Component):
    def __init__(self, color: Color4 = None, sprite: Sprite = None):
        self._color: Color4 = color if color is not None else Color4([1., 1., 1., 1.])
        self._sprite: Sprite = sprite if sprite is not None else Sprite()
        self._last_transform: Transform = None
        self._is_dirty = True
        super().__init__()

    def start(self):
        self._last_transform = self.game_object.transform.copy()

    def editor_update(self, dt: float):
        if not self._last_transform == self.game_object.transform:
            self.game_object.transform.copy(to=self._last_transform)
            self._is_dirty = True

    def update(self, dt: float):
        if not self._last_transform == self.game_object.transform:
            self.game_object.transform.copy(to=self._last_transform)
            self._is_dirty = True

    def get_color(self) -> Color4:
        return self._color

    def get_texture(self) -> Texture:
        return self._sprite.get_texture()
    
    def get_tex_coords(self) -> List[np.ndarray]:
        return self._sprite.get_tex_coords()

    def set_sprite(self, sprite: Sprite):
        self._sprite = sprite
        self._is_dirty = True

    def set_color(self, color: Color4):
        if self._color == color:
            return
        self._color[:] = color.copy()
        self._is_dirty = True

    def is_dirty(self) -> bool:
        return self._is_dirty

    def set_dirty(self):
        self._is_dirty = True


    def set_clean(self):
        self._is_dirty = False
