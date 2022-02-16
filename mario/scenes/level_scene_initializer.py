from pathlib import Path
from mario.components.breakable_brick import BreakableBrick
from components.editor_camera import EditorCamera
from mario.components.game_camera import GameCamera
from components.gizmo_system import GizmoSystem
from components.grid_lines import GridLines
from mario.components.ground import Ground
from components.key_controls import KeyControls
from components.mouse_controls import MouseControls
from components.sprite_renderer import SpriteRenderer

from components.spritesheet import Spritesheet
from components.state_machine import StateMachine
from mario.prefabs import Prefabs
from physics2d.components.box_2d_collider import Box2DCollider
from physics2d.components.rigid_body_2d import RigidBody2D
from physics2d.enums.body_type import BodyType
from scenes.scene import Scene

import imgui

from scenes.scene_initializer import SceneInitializer
from util.asset_pool import AssetPool
from util.vectors import Vector2


class LevelSceneInitializer(SceneInitializer):
    def __init__(self):
        super().__init__()
        self.camera_object = None

    def init(self, scene: Scene):
        from renderer.debug_draw import DebugDraw
        from mxeng.window import Window
        
        self.camera_object = scene.create_game_object("GameCamera")
        self.camera_object.add_component(GameCamera(scene.camera()))
        self.camera_object.start()
      
        scene.add_game_object_to_scene(self.camera_object)

    def load_resources(self, scene: Scene):
        AssetPool.get_shader("assets/shaders/default.glsl")

        AssetPool.add_spritesheet(
            "mario/assets/images/spritesheets/decorationsAndBlocks.png",
            Spritesheet(AssetPool.get_texture("mario/assets/images/spritesheets/decorationsAndBlocks.png"), 16, 16, 81, 0)
        )
        AssetPool.add_spritesheet(
            "mario/assets/images/spritesheet.png",
            Spritesheet(AssetPool.get_texture("mario/assets/images/spritesheet.png"), 16, 16, 26, 0)
        )
        AssetPool.add_spritesheet(
            "mario/assets/images/bigSpritesheet.png",
            Spritesheet(AssetPool.get_texture("mario/assets/images/bigSpritesheet.png"), 16, 32, 42, 0)
        )
        AssetPool.add_spritesheet(
            "mario/assets/images/items.png",
            Spritesheet(AssetPool.get_texture("mario/assets/images/items.png"), 16, 16, 35, 0)
        )
        AssetPool.add_spritesheet(
            "assets/images/gizmos.png",
            Spritesheet(AssetPool.get_texture("assets/images/gizmos.png"), 24, 48, 3, 0)
        )
        AssetPool.add_sound("mario/assets/sounds/1-up.ogg", loops=False)
        AssetPool.add_sound("mario/assets/sounds/bowserfalls.ogg", loops=False)
        AssetPool.add_sound("mario/assets/sounds/bowserfire.ogg", loops=False)
        AssetPool.add_sound("mario/assets/sounds/break_block.ogg", loops=False)
        AssetPool.add_sound("mario/assets/sounds/bump.ogg", loops=False)
        AssetPool.add_sound("mario/assets/sounds/coin.ogg", loops=False)
        AssetPool.add_sound("mario/assets/sounds/fireball.ogg", loops=False)
        AssetPool.add_sound("mario/assets/sounds/fireworks.ogg", loops=False)
        AssetPool.add_sound("mario/assets/sounds/flagpole.ogg", loops=False)
        AssetPool.add_sound("mario/assets/sounds/gameover.ogg", loops=False)
        AssetPool.add_sound("mario/assets/sounds/invincible.ogg", loops=False)
        AssetPool.add_sound("mario/assets/sounds/jump-small.ogg", loops=False)
        AssetPool.add_sound("mario/assets/sounds/jump-super.ogg", loops=False)
        AssetPool.add_sound("mario/assets/sounds/kick.ogg", loops=False)        
        AssetPool.add_sound("mario/assets/sounds/main-theme-overworld.ogg", loops=True)
        AssetPool.add_sound("mario/assets/sounds/mario_die.ogg", loops=False)
        AssetPool.add_sound("mario/assets/sounds/pipe.ogg", loops=False)
        AssetPool.add_sound("mario/assets/sounds/powerup.ogg", loops=False)
        AssetPool.add_sound("mario/assets/sounds/powerup_appears.ogg", loops=False)
        AssetPool.add_sound("mario/assets/sounds/stage_clear.ogg", loops=False)
        AssetPool.add_sound("mario/assets/sounds/stomp.ogg", loops=False)
        AssetPool.add_sound("mario/assets/sounds/vine.ogg", loops=False)
        AssetPool.add_sound("mario/assets/sounds/warning.ogg", loops=False)
        AssetPool.add_sound("mario/assets/sounds/world_clear.ogg", loops=False)

    def imgui(self):
        pass