from numpy import size
from components.editor_camera import EditorCamera
from components.gizmo_system import GizmoSystem
from components.grid_lines import GridLines
from components.key_controls import KeyControls
from components.mouse_controls import MouseControls
from components.spritesheet import Spritesheet
from mario.prefabs import MarioPrefabs
from scenes.scene_initializer import SceneInitializer
from scenes.scene import Scene
from editor.prefabs_window import Prefab, PrefabsWindow, Tab

from util.asset_pool import AssetPool

class LevelEditorSceneInitializer(SceneInitializer):
    save_path: str = "zelda_like/level.txt"

    def init(self, scene: Scene):
        gizmos = AssetPool.get_spritesheet("assets/images/gizmos.png")
        self.level_editor = scene.create_game_object("LevelEditor")
        self.level_editor.set_no_serialize()
        self.level_editor.add_component(MouseControls())
        self.level_editor.add_component(KeyControls())
        self.level_editor.add_component(GridLines())
        self.level_editor.add_component(EditorCamera(scene._camera))
        self.level_editor.add_component(GizmoSystem(gizmos))
        scene.add_game_object_to_scene(self.level_editor)

        self.prefabs_window = PrefabsWindow(self.level_editor.get_component(MouseControls))

        tiles_sprites = AssetPool.get_spritesheet("assets/NinjaAdventure/Backgrounds/Tilesets/TilesetFloor.png")
        self.prefabs_window.tabs.append(
            Tab(
                "Tiles",
                [
                    Prefab(
                        tiles_sprites.get_sprite(i),
                        lambda sprite: MarioPrefabs.generate_sprite_object(sprite, 0.25, 0.25)
                        )
                    for i in range(tiles_sprites.size())]
            )
        )

    def load_resources(self, scene: Scene):
        AssetPool.add_spritesheet(
            "assets/images/gizmos.png",
            Spritesheet(AssetPool.get_texture("assets/images/gizmos.png"), 24, 48, 3, 0)
        )
        AssetPool.add_spritesheet(
            "assets/NinjaAdventure/Backgrounds/Tilesets/TilesetFloor.png",
            Spritesheet(AssetPool.get_texture("assets/NinjaAdventure/Backgrounds/Tilesets/TilesetFloor.png"), 16, 16, 22*22, 0)
        )

    def imgui(self):
        self.prefabs_window.imgui()
