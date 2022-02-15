from components.component import Component
from mario.components.player_controller import PlayerController
from mxeng.game_object import GameObject
from util.asset_pool import AssetPool
from util.serialization import serializable

from Box2D import b2Contact

from util.vectors import Vector2

@serializable()
class Coin(Component):
    def __init__(self):
        self.play_anim: bool = False
        self.top_y: float = 0.
        self.coin_speed: float = 1.4
        super().__init__()

    def start(self):
        self.top_y = self.game_object.transform.position.y + 0.5

    def update(self, dt: float):
        if self.play_anim:
            # coin has been caught
            if self.game_object.transform.position.y < self.top_y:
                self.game_object.transform.position.y += dt * self.coin_speed
            else:
                self.game_object.destroy()


    def pre_solve(self, colliding_object: GameObject, contact: b2Contact, hit_normal: Vector2):
        if colliding_object.get_component(PlayerController) is not None:
            # colliding with the player
            AssetPool.get_sound("assets/sounds/coin.ogg").play()
            self.play_anim = True
            contact.enabled = False