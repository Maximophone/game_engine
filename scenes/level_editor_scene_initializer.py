from components.editor_camera import EditorCamera
from components.gizmo_system import GizmoSystem
from components.grid_lines import GridLines
from components.mouse_controls import MouseControls
from components.rigid_body import RigidBody

from components.spritesheet import Spritesheet
from mxeng.game_object import GameObject
from mxeng.prefabs import Prefabs
from scenes.scene import Scene

import imgui

from scenes.scene_initializer import SceneInitializer
from util.asset_pool import AssetPool
from util.vectors import Vector2, Vector3

class LevelEditorSceneInitializer(SceneInitializer):
    def __init__(self):
        super().__init__()
        self.obj1: GameObject = None
        self.sprite_index = 0
        self.sprite_flip_time = 0.2
        self.sprite_flip_time_left = 0.
        self.sprites = None
        self.level_editor_stuff = None
        self.t = 0.

    def init(self, scene: Scene):
        from renderer.debug_draw import DebugDraw
        from mxeng.window import Window
        
        self.sprites = AssetPool.get_spritesheet("assets/images/spritesheets/decorationsAndBlocks.png")
        gizmos = AssetPool.get_spritesheet("assets/images/gizmos.png")

        self.level_editor_stuff = scene.create_game_object("LevelEditor")
        self.level_editor_stuff.set_no_serialize()
        self.level_editor_stuff.add_component(MouseControls())
        self.level_editor_stuff.add_component(GridLines())
        self.level_editor_stuff.add_component(EditorCamera(scene._camera))
        self.level_editor_stuff.add_component(GizmoSystem(gizmos))
        scene.add_game_object_to_scene(self.level_editor_stuff)
        
        DebugDraw.add_line_2D(Vector2([600., 400.]), Vector2([800, 800]), Vector3([1., 0., 0.]), 1000)
        

    def load_resources(self, scene: Scene):
        AssetPool.get_shader("assets/shaders/default.glsl")
        AssetPool.add_spritesheet(
            "assets/images/spritesheets/decorationsAndBlocks.png",
            Spritesheet(AssetPool.get_texture("assets/images/spritesheets/decorationsAndBlocks.png"), 16, 16, 81, 0)
        )
        AssetPool.add_spritesheet(
            "assets/images/gizmos.png",
            Spritesheet(AssetPool.get_texture("assets/images/gizmos.png"), 24, 48, 3, 0)
        )

    def imgui(self):
        imgui.begin("Level Editor Stuff")
        self.level_editor_stuff.imgui()
        imgui.end()

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
