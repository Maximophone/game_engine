from components.component import Component
from util.serialization import serializable
from util.vectors import Vector2
from util.asset_pool import AssetPool

@serializable("top_y", "coin_speed")
class CoinBlock(Component):
    def __init__(self):
        self.top_y = Vector2([0., 0.])
        self.coin_speed: float = 1.4
        super().__init__()

    def start(self):
        self.top_y = self.game_object.transform.position + Vector2([0., 0.5])
        AssetPool.get_sound("assets/sounds/coin.ogg").play()

    def update(self, dt: float):
        if self.game_object.transform.position.y < self.top_y.y:
            self.game_object.transform.position.y += dt * self.coin_speed
            # TODO: Fix this
            # self.game_object.transform.scale.x -= (0.05 * dt) % -1
        else:
            self.game_object.destroy()
