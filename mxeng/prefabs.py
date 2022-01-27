from components.sprite import Sprite
from components.sprite_renderer import SpriteRenderer
from mxeng.game_object import GameObject
from mxeng.transform import Transform

import numpy as np

class Prefabs:
    @staticmethod
    def generate_sprite_object(sprite: Sprite, size_x: float, size_y: float) -> GameObject:
        block = GameObject(
            "Sprite_Object_Gen",
            Transform(
                np.array([0, 0]),
                np.array([size_x, size_y])
            )
        )
        renderer = SpriteRenderer(sprite=sprite)
        block.add_component(renderer)
        return block


