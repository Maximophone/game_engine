# from components.font_renderer import FontRenderer
# from components.sprite_renderer import SpriteRenderer
# from mxeng.game_object import GameObject
# from renderer.texture import Texture
# from util.timer import Time
import pickle

import math
from components.grid_lines import GridLines
from components.mouse_controls import MouseControls
from components.rigid_body import RigidBody
from components.sprite import Sprite
from components.sprite_renderer import SpriteRenderer
from components.spritesheet import Spritesheet
from mxeng.camera import Camera
from mxeng.game_object import GameObject
from mxeng.mouse_listener import MouseListener
from mxeng.prefabs import Prefabs
from scenes.scene import Scene
# from renderer.shader import Shader

# import OpenGL.GL as gl
import numpy as np
# import ctypes
from pyrr import Vector3
import imgui

from mxeng.transform import Transform
from util.asset_pool import AssetPool
from util.vectors import Color3, Vector2

class LevelEditorScene(Scene):

    def __init__(self):
        super().__init__()
        self.obj1: GameObject = None
        self.sprite_index = 0
        self.sprite_flip_time = 0.2
        self.sprite_flip_time_left = 0.
        self.sprites = None
        self.level_editor_stuff = GameObject("LevelEditor", Transform(), 0)
        self.t = 0.

    def init(self):
        from renderer.debug_draw import DebugDraw
        self.level_editor_stuff.add_component(MouseControls())
        self.level_editor_stuff.add_component(GridLines())
        self.load_resources()
        self._camera = Camera(Vector3([0., 0., 0.]))
        self.sprites = AssetPool.get_spritesheet("assets/images/spritesheets/decorationsAndBlocks.png")
        
        DebugDraw.add_line_2D(Vector2([600., 400.]), Vector2([800, 800]), Vector3([1., 0., 0.]), 1000)
        
        if self._level_loaded:
            if len(self._game_objects):
                self._active_game_object = self._game_objects[-1]
            return

    
    def load_resources(self):
        AssetPool.get_shader("assets/shaders/default.glsl")
        AssetPool.add_spritesheet(
            "assets/images/spritesheets/decorationsAndBlocks.png",
            Spritesheet(AssetPool.get_texture("assets/images/spritesheets/decorationsAndBlocks.png"), 16, 16, 81, 0)
        )

    def update(self, dt: float):
        from renderer.debug_draw import DebugDraw
        self.level_editor_stuff.update(dt)
        
        DebugDraw.add_circle(Vector2([50, 50]), 64)
        DebugDraw.add_box_2D(Vector2([100, 100]), Vector2([50, 100]), 60, Color3([0.5, 0.2, 0]))

        for go in self._game_objects:
            go.update(dt)

        self._renderer.render()

    def imgui(self):
        imgui.begin("Test window")
        
        window_pos = imgui.core.get_window_position()
        window_size = imgui.core.get_window_size()
        item_spacing = imgui.core.get_style().item_spacing

        window_x2: float = window_pos.x + window_size.x
        for i in range(self.sprites.size()):
            sprite = self.sprites.get_sprite(i)
            sprite_width = sprite.width * 4
            sprite_height = sprite.height * 4
            id = sprite.tex_id
            tex_coords = sprite.get_tex_coords()

            imgui.core.push_id(str(i))
            changed = imgui.core.image_button(id, sprite_width, sprite_height, (tex_coords[2][0], tex_coords[0][1]), (tex_coords[0][0], tex_coords[2][1]))
            if changed:
                obj = Prefabs.generate_sprite_object(sprite, 32, 32)
                obj.add_component(RigidBody())
                self.level_editor_stuff.get_component(MouseControls).pickup_object(obj)
            imgui.core.pop_id()

            last_button_pos = imgui.core.get_item_rect_max()
            last_button_x2 = last_button_pos.x
            next_button_x2 = last_button_x2 + item_spacing.x + sprite_width

            if i + 1 < self.sprites.size() and next_button_x2 < window_x2:
                imgui.core.same_line()

        imgui.end()
