from pathlib import Path
from editor.prefabs_window import Prefab, PrefabsWindow, Tab
from editor.sounds_window import SoundsWindow
from mario.components.breakable_brick import BreakableBrick
from components.editor_camera import EditorCamera
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
from mxeng.direction import Direction
from util.vectors import Vector2


class LevelEditorSceneInitializer(SceneInitializer):
    def __init__(self):
        super().__init__()
        self.sprites = None
        self.level_editor_stuff = None

    def init(self, scene: Scene): 
        sprites = AssetPool.get_spritesheet("mario/assets/images/spritesheets/decorationsAndBlocks.png")
        player_sprites = AssetPool.get_spritesheet("mario/assets/images/spritesheet.png")
        item_sprites = AssetPool.get_spritesheet("mario/assets/images/items.png")
        turtle_sprites = AssetPool.get_spritesheet("mario/assets/images/turtle.png")
        pipe_sprites = AssetPool.get_spritesheet("mario/assets/images/pipes.png")
        gizmos = AssetPool.get_spritesheet("assets/images/gizmos.png")

        self.level_editor_stuff = scene.create_game_object("LevelEditor")
        self.level_editor_stuff.set_no_serialize()
        self.level_editor_stuff.add_component(MouseControls())
        self.level_editor_stuff.add_component(KeyControls())
        self.level_editor_stuff.add_component(GridLines())
        self.level_editor_stuff.add_component(EditorCamera(scene._camera))
        self.level_editor_stuff.add_component(GizmoSystem(gizmos))
        scene.add_game_object_to_scene(self.level_editor_stuff)

        self.prefabs_window = PrefabsWindow(self.level_editor_stuff.get_component(MouseControls))
        self.sounds_window = SoundsWindow(AssetPool.get_all_sounds())

        solid_blocks_ids = list(range(34)) + list(range(35, 38)) + list(range(61, sprites.size()))
        self.prefabs_window.tabs.append(
            Tab(
                "Ground Blocks",
                [
                    Prefab(
                        sprites.get_sprite(i),
                        Prefabs.generate_ground_block,
                    )
                    for i in solid_blocks_ids
                ]
                )
        )

        decoration_blocks_ids = [34] + list(range(38, 42)) + list(range(45, 61))
        self.prefabs_window.tabs.append(
            Tab(
                "Decoration Blocks",
                [
                    Prefab(
                        sprites.get_sprite(i),
                        lambda sprite: Prefabs.generate_sprite_object(sprite, 0.25, 0.25)
                    )
                    for i in decoration_blocks_ids
                ]
            )
        )

        pipes_directions = [
            (0, Direction.Down),
            (1, Direction.Up),
            (2, Direction.Right),
            (3, Direction.Left)
        ]

        self.prefabs_window.tabs.append(
            Tab(
                "Prefabs",
                [
                    Prefab(
                        player_sprites.get_sprite(0),
                        lambda sprite: Prefabs.generate_mario()
                    ),
                    Prefab(
                        item_sprites.get_sprite(0),
                        lambda sprite: Prefabs.generate_question_block()
                    ),
                    Prefab(
                        sprites.get_sprite(12),
                        Prefabs.generate_breakable_block
                    ),
                    Prefab(
                        item_sprites.get_sprite(7),
                        lambda sprite: Prefabs.generate_coin()
                    ),
                    Prefab(
                        player_sprites.get_sprite(14),
                        lambda sprite: Prefabs.generate_goomba()
                    ),
                    Prefab(
                        turtle_sprites.get_sprite(0),
                        lambda sprite: Prefabs.generate_turtle()
                    ),
                    Prefab(
                        item_sprites.get_sprite(6),
                        lambda sprite: Prefabs.generate_flag_top()
                    ),
                    Prefab(
                        item_sprites.get_sprite(33),
                        lambda sprite: Prefabs.generate_flag_pole()
                    ),
                    Prefab(
                        pipe_sprites.get_sprite(0),
                        lambda sprite: Prefabs.generate_pipe(Direction.Down)
                    ),
                    Prefab(
                        pipe_sprites.get_sprite(1),
                        lambda sprite: Prefabs.generate_pipe(Direction.Up)
                    ),
                    Prefab(
                        pipe_sprites.get_sprite(2),
                        lambda sprite: Prefabs.generate_pipe(Direction.Right)
                    ),
                    Prefab(
                        pipe_sprites.get_sprite(3),
                        lambda sprite: Prefabs.generate_pipe(Direction.Left)
                    ),
                ]
            )
        )
        

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
            "mario/assets/images/turtle.png",
            Spritesheet(AssetPool.get_texture("mario/assets/images/turtle.png"), 16, 24, 4, 0)
        )
        AssetPool.add_spritesheet(
            "mario/assets/images/pipes.png",
            Spritesheet(AssetPool.get_texture("mario/assets/images/pipes.png"), 32, 32, 6, 0)
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
        imgui.begin("Level Editor Stuff")
        self.level_editor_stuff.imgui()
        imgui.end()

        self.prefabs_window.imgui()

        self.sounds_window.imgui()
