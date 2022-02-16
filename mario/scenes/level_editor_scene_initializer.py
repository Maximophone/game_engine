from editor.prefabs_window import Prefab, PrefabsWindow, Tab
from editor.sounds_window import SoundsWindow
from components.editor_camera import EditorCamera
from components.gizmo_system import GizmoSystem
from components.grid_lines import GridLines
from components.key_controls import KeyControls
from components.mouse_controls import MouseControls
from mario.prefabs import Prefabs
from mario.scenes.load_resources import load_resources
from scenes.scene import Scene

import imgui

from scenes.scene_initializer import SceneInitializer
from util.asset_pool import AssetPool
from mxeng.direction import Direction


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
        load_resources()
        
    def imgui(self):
        imgui.begin("Level Editor Stuff")
        self.level_editor_stuff.imgui()
        imgui.end()

        self.prefabs_window.imgui()

        self.sounds_window.imgui()
