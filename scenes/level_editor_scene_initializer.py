from components.editor_camera import EditorCamera
from components.gizmo_system import GizmoSystem
from components.grid_lines import GridLines
from components.mouse_controls import MouseControls
from components.sprite_renderer import SpriteRenderer

from components.spritesheet import Spritesheet
from mxeng.game_object import GameObject
from mxeng.prefabs import Prefabs
from scenes.scene import Scene

import imgui

from scenes.scene_initializer import SceneInitializer
from util.asset_pool import AssetPool
from util.vectors import Vector2, Vector3, Color4

class LevelEditorSceneInitializer(SceneInitializer):
    def __init__(self):
        super().__init__()
        self.sprites = None
        self.level_editor_stuff = None

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

        
        # TODO: fix a bug, if I draw this debugdraw line with a lifetime of 1000, it creates a bug where
        # the grid lines do not disappear when I hit play
        #DebugDraw.add_line_2D(Vector2([600., 400.]), Vector2([800, 800]), Vector3([1., 0., 0.]), 1000)
        

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

        for go in scene._game_objects:
            if go.get_component(SpriteRenderer) is not None:
                spr: SpriteRenderer = go.get_component(SpriteRenderer)
                if spr.get_texture() is not None:
                    spr.set_texture(AssetPool.get_texture(spr.get_texture().filepath))

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
                obj = Prefabs.generate_sprite_object(sprite, 0.25, 0.25)
                self.level_editor_stuff.get_component(MouseControls).pickup_object(obj)
            imgui.core.pop_id()

            last_button_pos = imgui.core.get_item_rect_max()
            last_button_x2 = last_button_pos.x
            next_button_x2 = last_button_x2 + item_spacing.x + sprite_width

            if i + 1 < self.sprites.size() and next_button_x2 < window_x2:
                imgui.core.same_line()

        imgui.end()
