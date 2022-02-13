from components.component import Component
from components.player_controller import PlayerController
from mxeng.camera import Camera
from mxeng.game_object import GameObject
from util.serialization import serializable
from util.vectors import Color4

@serializable()
class GameCamera(Component):
    def __init__(self, game_camera: Camera):
        self.player: GameObject = None
        self.game_camera: Camera = game_camera
        self.highest_x: float = 0.
        self.underground_y_level: float = 0.
        self.camera_buffer: float = 1.5
        self.player_buffer: float = 0.25 # player height

        self.sky_color = Color4([92/255, 148/255, 252/255, 1.])
        self.underground_color = Color4([0., 0., 0., 1.])
        super().__init__()

    def start(self):
        from mxeng.window import Window
        self.player = Window.get_scene().get_game_object_with(PlayerController)
        self.game_camera.clear_color = self.sky_color
        self.underground_y_level = self.game_camera.position.y - self.game_camera.projection_size.y - self.camera_buffer

    def update(self, dt: float):
        if self.player is not self.player.get_component(PlayerController).has_won():
            self.game_camera.position.x = max(self.player.transform.position.x - 2.5, self.highest_x)
            self.highest_x = max(self.highest_x, self.game_camera.position.x)

            if self.player.transform.position.y < -self.player_buffer:
                # player is below ground
                self.game_camera.position.y = self.underground_y_level
                self.game_camera.clear_color = self.underground_color
            elif self.player.transform.position.y >= 0.:
                self.game_camera.position.y = 0.
                self.game_camera.clear_color = self.sky_color