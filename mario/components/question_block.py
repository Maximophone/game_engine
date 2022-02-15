from enum import Enum, auto
from mario.components.block import Block
from mario.components.game_camera import GameCamera
from components.state_machine import StateMachine
from mario.components.player_controller import PlayerController, PlayerState
from mxeng.game_object import GameObject
from util.serialization import senum, serializable

@senum
class BlockType(Enum):
    Coin = auto()
    Powerup = auto()
    Invincibility = auto()

@serializable("block_type")
class QuestionBlock(Block):
    def __init__(self):
        self.block_type: BlockType = BlockType.Coin
        super().__init__()

    def player_hit(self, player_controller: PlayerController):
        if self.block_type == BlockType.Coin:
            self.do_coin(player_controller)
        elif self.block_type == BlockType.Powerup:
            self.do_powerup(player_controller)
        elif self.block_type == BlockType.Invincibility:
            self.do_invincibility(player_controller)

        state_machine = self.game_object.get_component(StateMachine)
        if state_machine is not None:
            state_machine.trigger("set_inactive")
            self.active = False

    def do_coin(self, player_controller: PlayerController):
        from mxeng.window import Window
        from mario.prefabs import Prefabs
        coin = Prefabs.generate_coin_block()
        coin.transform.position = self.game_object.transform.position.copy()
        coin.transform.position.y += 0.25
        Window.get_scene().add_game_object_to_scene(coin)

    def do_powerup(self, player_controller: PlayerController):
        if player_controller.player_state == PlayerState.Small:
            self.spawn_mushroom()
        else:
            self.spawn_flower()


    def do_invincibility(self, player_controller: PlayerController):
        pass

    def spawn_mushroom(self):
        from mxeng.window import Window
        from mario.prefabs import Prefabs
        mushroom: GameObject = Prefabs.generate_mushroom()
        mushroom.transform.position = self.game_object.transform.position.copy()
        mushroom.transform.position.y += 0.25
        Window.get_scene().add_game_object_to_scene(mushroom)

    def spawn_flower(self):
        from mxeng.window import Window
        from mario.prefabs import Prefabs
        flower: GameObject = Prefabs.generate_flower()
        flower.transform.position = self.game_object.transform.position.copy()
        flower.transform.position.y += 0.25
        Window.get_scene().add_game_object_to_scene(flower)
