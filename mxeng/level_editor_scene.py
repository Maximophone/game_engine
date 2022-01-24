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
import imgui

from mxeng.transform import Transform
from util.asset_pool import AssetPool
from util.serialization import serializable, serialize

@serializable("obj1", "sprite_index", "sprite_flip_time", "sprite_flip_time_left", "sprites")
class LevelEditorScene(Scene):

    def __init__(self):
        super().__init__()
        self.obj1: GameObject = None
        self.sprite_index = 0
        self.sprite_flip_time = 0.2
        self.sprite_flip_time_left = 0.
        self.sprites = None

    def init(self):
        self.load_resources()

        self._camera = Camera(vector3.create())

        self.sprites = AssetPool.get_spritesheet("assets/images/spritesheet.png")

        self.obj1 = GameObject("object 1", Transform(np.array([200., 100.]), np.array([256., 256.])), z_index=2)
        #self.obj1.add_component(SpriteRenderer(sprite=self.sprites.get_sprite(0)))
        self.obj1.add_component(SpriteRenderer(color=np.array([1., 0., 0., 1.])))#sprite=Sprite(AssetPool.get_texture("assets/images/blendImage1.png"))))
        self.add_game_object_to_scene(self.obj1)
        
        obj2 = GameObject("object 2", Transform(np.array([400., 100.]), np.array([256., 256.])), z_index=2)
        #obj2.add_component(SpriteRenderer(sprite=self.sprites.get_sprite(15)))
        obj2.add_component(SpriteRenderer(sprite=Sprite(AssetPool.get_texture("assets/images/blendImage2.png"))))
        self.add_game_object_to_scene(obj2)

        self._active_game_object = self.obj1

        print(serialize(self))
    
    def load_resources(self):
        AssetPool.get_shader("assets/shaders/default.glsl")
        AssetPool.add_spritesheet(
            "assets/images/spritesheet.png",
            Spritesheet(AssetPool.get_texture("assets/images/spritesheet.png"), 16, 16, 26, 0)
        )

    def update(self, dt: float):

        # self.sprite_flip_time_left -= dt
        # if self.sprite_flip_time_left <= 0:
        #     self.sprite_flip_time_left = self.sprite_flip_time
        #     self.sprite_index = (self.sprite_index + 1) % 4
        #     self.obj1.get_component(SpriteRenderer).set_sprite(self.sprites.get_sprite(self.sprite_index))

        # self.obj1.transform.position[0] += 10*dt
        for go in self._game_objects:
            go.update(dt)

        self._renderer.render()

    def imgui(self):
        imgui.begin("Test window")
        imgui.text("Some random text")
        imgui.end()
