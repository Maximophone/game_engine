from pathlib import Path
from components.breakable_brick import BreakableBrick
from components.editor_camera import EditorCamera
from components.gizmo_system import GizmoSystem
from components.grid_lines import GridLines
from components.ground import Ground
from components.key_controls import KeyControls
from components.mouse_controls import MouseControls
from components.sprite_renderer import SpriteRenderer

from components.spritesheet import Spritesheet
from components.state_machine import StateMachine
from mxeng.prefabs import Prefabs
from physics2d.components.box_2d_collider import Box2DCollider
from physics2d.components.rigid_body_2d import RigidBody2D
from physics2d.enums.body_type import BodyType
from scenes.scene import Scene

import imgui

from scenes.scene_initializer import SceneInitializer
from util.asset_pool import AssetPool
from util.vectors import Vector2


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
        self.level_editor_stuff.add_component(KeyControls())
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
            "assets/images/spritesheet.png",
            Spritesheet(AssetPool.get_texture("assets/images/spritesheet.png"), 16, 16, 26, 0)
        )
        AssetPool.add_spritesheet(
            "assets/images/bigSpritesheet.png",
            Spritesheet(AssetPool.get_texture("assets/images/bigSpritesheet.png"), 16, 32, 42, 0)
        )
        AssetPool.add_spritesheet(
            "assets/images/items.png",
            Spritesheet(AssetPool.get_texture("assets/images/items.png"), 16, 16, 35, 0)
        )
        AssetPool.add_spritesheet(
            "assets/images/gizmos.png",
            Spritesheet(AssetPool.get_texture("assets/images/gizmos.png"), 24, 48, 3, 0)
        )
        AssetPool.add_sound("assets/sounds/1-up.ogg", loops=False)
        AssetPool.add_sound("assets/sounds/bowserfalls.ogg", loops=False)
        AssetPool.add_sound("assets/sounds/bowserfire.ogg", loops=False)
        AssetPool.add_sound("assets/sounds/break_block.ogg", loops=False)
        AssetPool.add_sound("assets/sounds/bump.ogg", loops=False)
        AssetPool.add_sound("assets/sounds/coin.ogg", loops=False)
        AssetPool.add_sound("assets/sounds/fireball.ogg", loops=False)
        AssetPool.add_sound("assets/sounds/fireworks.ogg", loops=False)
        AssetPool.add_sound("assets/sounds/flagpole.ogg", loops=False)
        AssetPool.add_sound("assets/sounds/gameover.ogg", loops=False)
        AssetPool.add_sound("assets/sounds/invincible.ogg", loops=False)
        AssetPool.add_sound("assets/sounds/jump-small.ogg", loops=False)
        AssetPool.add_sound("assets/sounds/jump-super.ogg", loops=False)
        AssetPool.add_sound("assets/sounds/kick.ogg", loops=False)        
        AssetPool.add_sound("assets/sounds/main-theme-overworld.ogg", loops=True)
        AssetPool.add_sound("assets/sounds/mario_die.ogg", loops=False)
        AssetPool.add_sound("assets/sounds/pipe.ogg", loops=False)
        AssetPool.add_sound("assets/sounds/powerup.ogg", loops=False)
        AssetPool.add_sound("assets/sounds/powerup_appears.ogg", loops=False)
        AssetPool.add_sound("assets/sounds/stage_clear.ogg", loops=False)
        AssetPool.add_sound("assets/sounds/stomp.ogg", loops=False)
        AssetPool.add_sound("assets/sounds/vine.ogg", loops=False)
        AssetPool.add_sound("assets/sounds/warning.ogg", loops=False)
        AssetPool.add_sound("assets/sounds/world_clear.ogg", loops=False)
        

        for go in scene._game_objects:

            if go.get_component(SpriteRenderer) is not None:
                spr: SpriteRenderer = go.get_component(SpriteRenderer)
                if spr.get_texture() is not None:
                    spr.set_texture(AssetPool.get_texture(spr.get_texture().filepath))

            if go.get_component(StateMachine) is not None:
                state_machine: StateMachine = go.get_component(StateMachine)
                state_machine.refresh_textures()

    def imgui(self):
        imgui.begin("Level Editor Stuff")
        self.level_editor_stuff.imgui()
        imgui.end()

        imgui.begin("Objects")

        solid_blocks_ids = list(range(34)) + list(range(35, 38)) + list(range(61, self.sprites.size()))
        if imgui.collapsing_header("Solid Blocks", True)[0]:
            window_pos = imgui.core.get_window_position()
            window_size = imgui.core.get_window_size()
            item_spacing = imgui.core.get_style().item_spacing

            window_x2: float = window_pos.x + window_size.x
            for i in solid_blocks_ids:
    
                sprite = self.sprites.get_sprite(i)
                sprite_width = sprite.width * 4
                sprite_height = sprite.height * 4
                id = sprite.tex_id
                tex_coords = sprite.get_tex_coords()

                imgui.core.push_id(str(i))
                changed = imgui.core.image_button(id, sprite_width, sprite_height, (tex_coords[2][0], tex_coords[0][1]), (tex_coords[0][0], tex_coords[2][1]))
                if changed:
                    obj = Prefabs.generate_sprite_object(sprite, 0.25, 0.25)
                    rb = RigidBody2D()
                    rb.body_type = BodyType.Static
                    obj.add_component(rb)
                    b2d = Box2DCollider()
                    b2d.half_size = Vector2([0.25, 0.25]
                    )
                    obj.add_component(b2d)
                    obj.add_component(Ground())
                    if i == 12:
                        # Breakable bricks
                        obj.add_component(BreakableBrick())
                    self.level_editor_stuff.get_component(MouseControls).pickup_object(obj)
                imgui.core.pop_id()

                last_button_pos = imgui.core.get_item_rect_max()
                last_button_x2 = last_button_pos.x
                next_button_x2 = last_button_x2 + item_spacing.x + sprite_width


                if i + 1 < self.sprites.size() and next_button_x2 < window_x2:
                    imgui.core.same_line()

        decoration_blocks_ids = [34] + list(range(38, 42)) + list(range(45, 61))
        if imgui.collapsing_header("Decoration Blocks", True)[0]:
            window_pos = imgui.core.get_window_position()
            window_size = imgui.core.get_window_size()
            item_spacing = imgui.core.get_style().item_spacing

            window_x2: float = window_pos.x + window_size.x
            for i in decoration_blocks_ids:
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

        if imgui.collapsing_header("Prefabs", True)[0]:
            uid = 0
            # MARIO
            player_sprites = AssetPool.get_spritesheet("assets/images/spritesheet.png")
            sprite = player_sprites.get_sprite(0)
            sprite_width = sprite.width * 4
            sprite_height = sprite.height * 4
            id = sprite.tex_id
            tex_coords = sprite.get_tex_coords()

            imgui.push_id(str(uid))
            uid+=1
            changed = imgui.image_button(id, sprite_width, sprite_height, (tex_coords[2][0], tex_coords[0][1]), (tex_coords[0][0], tex_coords[2][1]))
            if changed:
                obj = Prefabs.generate_mario()
                self.level_editor_stuff.get_component(MouseControls).pickup_object(obj)
            imgui.pop_id()
            imgui.same_line()

            # QUESTION BLOCK
            item_sprites = AssetPool.get_spritesheet("assets/images/items.png")
            sprite = item_sprites.get_sprite(0)
            id = sprite.tex_id
            tex_coords = sprite.get_tex_coords()

            imgui.push_id(str(uid))
            uid+=1
            changed = imgui.image_button(id, sprite_width, sprite_height, (tex_coords[2][0], tex_coords[0][1]), (tex_coords[0][0], tex_coords[2][1]))
            if changed:
                obj = Prefabs.generate_question_block()
                self.level_editor_stuff.get_component(MouseControls).pickup_object(obj)
            imgui.pop_id()
            imgui.same_line()
            
            # GOOMBA
            
            sprite = player_sprites.get_sprite(14)
            id = sprite.tex_id
            tex_coords = sprite.get_tex_coords()
            imgui.push_id(str(uid))
            uid+=1

            changed = imgui.image_button(id, sprite_width, sprite_height, (tex_coords[2][0], tex_coords[0][1]), (tex_coords[0][0], tex_coords[2][1]))
            if changed:
                obj = Prefabs.generate_goomba()
                self.level_editor_stuff.get_component(MouseControls).pickup_object(obj)
            imgui.pop_id()


        if imgui.collapsing_header("Sounds", True)[0]:
            sounds = AssetPool.get_all_sounds()

            for i, sound in enumerate(sounds):
                sound_path = sound.filepath
                if imgui.button(Path(sound_path).name):
                    if not sound.is_playing:
                        sound.play()

                    else:
                        sound.stop()
                if i%5:
                    imgui.same_line()

        imgui.end()

