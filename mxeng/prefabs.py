from components.sprite import Sprite
from components.sprite_renderer import SpriteRenderer
from mxeng.game_object import GameObject
from components.transform import Transform

from util.vectors import Vector2

class Prefabs:
    @staticmethod
    def generate_sprite_object(sprite: Sprite, size_x: float, size_y: float) -> GameObject:
        from mxeng.window import Window
        block = Window.get_scene().create_game_object(
            "Sprite_Object_Gen", 
            Transform(
                Vector2([0., 0.]),
                Vector2([size_x, size_y])
            ))
        renderer = SpriteRenderer(sprite=sprite)
        block.add_component(renderer)
        return block


