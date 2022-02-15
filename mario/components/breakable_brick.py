from mario.components.block import Block
from mario.components.player_controller import PlayerController, PlayerState
from util.asset_pool import AssetPool
from util.serialization import serializable

@serializable()
class BreakableBrick(Block):
    def player_hit(self, player_controller: PlayerController):
        if not player_controller.player_state == PlayerState.Small:
            AssetPool.get_sound("assets/sounds/break_block.ogg").play()
            self.game_object.destroy()