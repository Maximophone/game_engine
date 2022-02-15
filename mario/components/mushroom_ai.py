from components.component import Component
from mario.components.ground import Ground
from mario.components.player_controller import PlayerController
from mxeng.game_object import GameObject
from physics2d.components.rigid_body_2d import RigidBody2D
from util.serialization import serializable
from util.vectors import Vector2
from util.asset_pool import AssetPool

from Box2D import b2Contact

@serializable()
class MushroomAI(Component):
    def __init__(self):
        self.going_right: bool = True
        self.rb: RigidBody2D = None
        self.speed: Vector2 = Vector2([1., 0.])
        self.max_speed: float = 0.8
        self.hit_player: bool = False
        super().__init__()

    def start(self):
        self.rb = self.game_object.get_component(RigidBody2D)
        AssetPool.get_sound("assets/sounds/powerup_appears.ogg").play()

    def update(self, dt: float):
        if self.going_right and abs(self.rb.velocity.x) < self.max_speed:
            self.rb.add_velocity(self.speed)
        elif not self.going_right and abs(self.rb.velocity.x) < self.max_speed:
            self.rb.add_velocity(Vector2([-self.speed.x, self.speed.y]))

    def pre_solve(self, colliding_object: GameObject, contact: b2Contact, hit_normal: Vector2):
        player_controller = colliding_object.get_component(PlayerController)
        if player_controller is not None:
            # mushroom hit the player
            contact.enabled = False
            if not self.hit_player:
                player_controller.powerup()
                self.game_object.destroy()
                self.hit_player = True
            return
        elif colliding_object.get_component(Ground) is None:
            # only colliding with the ground
            contact.enabled = False
            return
        if abs(hit_normal.y) < 0.1:
            self.going_right = hit_normal.x < 0
        
        