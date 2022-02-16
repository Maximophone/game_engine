from mario.components.game_camera import GameCamera
from mario.scenes.load_resources import load_resources
from scenes.scene import Scene
from scenes.scene_initializer import SceneInitializer


class LevelSceneInitializer(SceneInitializer):
    save_path: str = "mario/level.txt"
    def __init__(self):
        super().__init__()
        self.camera_object = None

    def init(self, scene: Scene):
        self.camera_object = scene.create_game_object("GameCamera")
        self.camera_object.add_component(GameCamera(scene.camera()))
        self.camera_object.start()
      
        scene.add_game_object_to_scene(self.camera_object)

    def load_resources(self, scene: Scene):
        load_resources()

    def imgui(self):
        pass