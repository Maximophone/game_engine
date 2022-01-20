# from components.font_renderer import FontRenderer
# from components.sprite_renderer import SpriteRenderer
# from mxeng.game_object import GameObject
# from renderer.texture import Texture
# from util.timer import Time
from components.sprite import Sprite
from components.sprite_renderer import SpriteRenderer
from components.spritesheet import Spritesheet
from mxeng.camera import Camera
from mxeng.game_object import GameObject
from mxeng.scene import Scene
# from renderer.shader import Shader

# import OpenGL.GL as gl
import numpy as np
# import ctypes
from pyrr import vector3, vector4

from mxeng.transform import Transform
from util.asset_pool import AssetPool

class LevelEditorScene(Scene):

    def __init__(self):
        super().__init__()
        print("Inside Level Editor Scene")

    def init(self):
        self.load_resources()

        self._camera = Camera(vector3.create())

        sprites = AssetPool.get_spritesheet("assets/images/spritesheet.png")

        obj1 = GameObject("object 1", Transform(np.array([100, 100]), np.array([256, 256])))
        obj1.add_component(SpriteRenderer(sprite=sprites.get_sprite(0)))
        self.add_game_object_to_scene(obj1)
        
        obj2 = GameObject("object 2", Transform(np.array([400, 100]), np.array([256, 256])))
        obj2.add_component(SpriteRenderer(sprite=sprites.get_sprite(15)))
        self.add_game_object_to_scene(obj2)
    
    def load_resources(self):
        AssetPool.get_shader("assets/shaders/default.glsl")
        AssetPool.add_spritesheet(
            "assets/images/spritesheet.png",
            Spritesheet(AssetPool.get_texture("assets/images/spritesheet.png"), 16, 16, 26, 0)
        )

    def update(self, dt: float):
        for go in self._game_objects:
            go.update(dt)

        self._renderer.render()

