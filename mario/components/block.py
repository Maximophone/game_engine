from components.component import Component
from mario.components.player_controller import PlayerController
from mxeng.game_object import GameObject
from util.asset_pool import AssetPool
from util.serialization import serializable
from util.vectors import Vector2

from Box2D import b2Contact

@serializable()
class Block(Component):
    def __init__(self):
        self.bop_going_up: bool = True
        self.do_bop_animation: bool = False
        self.bop_start: Vector2 = Vector2([0., 0.])
        self.top_bop_location: Vector2 = Vector2([0., 0.])
        self.active: bool = True
        self.bop_speed: float = 0.4
        super().__init__()

    def start(self):
        self.bop_start = self.game_object.transform.position.copy()
        self.top_bop_location = self.bop_start + Vector2([0., 0.02])

    def update(self, dt: float):
        if self.do_bop_animation:
            if self.bop_going_up:
                if self.game_object.transform.position.y < self.top_bop_location.y:
                    self.game_object.transform.position.y += self.bop_speed * dt
                else:
                    self.bop_going_up = False
            else:
                if self.game_object.transform.position.y > self.bop_start.y:
                    self.game_object.transform.position.y -= self.bop_speed * dt
                else:
                    self.game_object.transform.position.y = self.bop_start.y
                    self.bop_going_up = True
                    self.do_bop_animation = False

    def begin_collision(self, colliding_object: GameObject, contact: b2Contact, hit_normal: Vector2):
        player_controller = colliding_object.get_component(PlayerController)
        if self.active and player_controller is not None and hit_normal.y < -0.8:
            # player hit the bottom of the block
            self.do_bop_animation = True
            AssetPool.get_sound("assets/sounds/bump.ogg").play()
            self.player_hit(player_controller)

    def player_hit(self, player_controller: PlayerController):
        pass