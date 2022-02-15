from components.component import Component
from mario.components.player_controller import PlayerController
from mxeng.game_object import GameObject
from util.serialization import serializable
from util.vectors import Vector2

from Box2D import b2Contact

@serializable("is_top")
class Flagpole(Component):
    def __init__(self, is_top: bool = False):
        self.is_top: bool = is_top
        super().__init__()

    def begin_collision(self, colliding_object: GameObject, contact: b2Contact, hit_normal: Vector2):
        player_controller: PlayerController = colliding_object.get_component(PlayerController)
        if player_controller is not None:
            player_controller.play_win_animation(self.game_object)