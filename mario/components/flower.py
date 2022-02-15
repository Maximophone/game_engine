from components.component import Component
from mario.components.player_controller import PlayerController
from mxeng.game_object import GameObject
from physics2d.components.rigid_body_2d import RigidBody2D
from util.serialization import serializable
from util.asset_pool import AssetPool

from Box2D import b2Contact

from util.vectors import Vector2

@serializable()
class Flower(Component):
    def __init__(self):
        self.rb: RigidBody2D = None
        super().__init__()
    
    def start(self):
        self.rb: RigidBody2D = self.game_object.get_component(RigidBody2D)
        AssetPool.get_sound("assets/sounds/powerup_appears.ogg").play()
        self.rb.is_sensor = True

    def begin_collision(self, colliding_object: GameObject, contact: b2Contact, hit_normal: Vector2):
        player_controller: PlayerController = colliding_object.get_component(PlayerController)
        if player_controller is not None:
            player_controller.powerup()
            self.game_object.destroy()