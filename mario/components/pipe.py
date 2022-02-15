from components.component import Component
from mario.components.player_controller import PlayerController
from mxeng.direction import Direction
from mxeng.game_object import GameObject
from mxeng.key_listener import KeyListener
from util.asset_pool import AssetPool
from util.serialization import serializable, sproperty

import glfw
from Box2D import b2Contact

from util.vectors import Vector2


@serializable("direction", "is_entrance")
class Pipe(Component):
    def __init__(self, direction: Direction = Direction.Up):
        self.direction: Direction = direction
        self._connecting_pipe_name: str = ""
        self.is_entrance: bool = False
        self.connecting_pipe: GameObject = None
        self.entrance_vector_tolerance: float = 0.6
        self.colliding_player: PlayerController = None
        super().__init__()

    @sproperty
    def connecting_pipe_name(self) -> str:
        return self._connecting_pipe_name

    @connecting_pipe_name.setter
    def connecting_pipe_name(self, value: str):
        from mxeng.window import Window
        self._connecting_pipe_name = value
        self.connecting_pipe = Window.get_scene().get_game_object_by_name(self._connecting_pipe_name)

    def start(self):
        from mxeng.window import Window
        self.connecting_pipe = Window.get_scene().get_game_object_by_name(self._connecting_pipe_name)

    def update(self, dt: float):
        if self.connecting_pipe is None:
            return

        if self.colliding_player is not None:
            player_entering = False
            if self.direction == Direction.Up:
                if (KeyListener.is_key_pressed(glfw.KEY_DOWN) or KeyListener.is_key_pressed(glfw.KEY_S)) and self.is_entrance and self.player_at_entrance():
                    player_entering = True    
            elif self.direction == Direction.Left:
                if (KeyListener.is_key_pressed(glfw.KEY_RIGHT) or KeyListener.is_key_pressed(glfw.KEY_D)) and self.is_entrance and self.player_at_entrance():
                    player_entering = True
            elif self.direction == Direction.Right:
                if (KeyListener.is_key_pressed(glfw.KEY_LEFT) or KeyListener.is_key_pressed(glfw.KEY_A)) and self.is_entrance and self.player_at_entrance():
                    player_entering = True
            elif self.direction == Direction.Down:
                if (KeyListener.is_key_pressed(glfw.KEY_UP) or KeyListener.is_key_pressed(glfw.KEY_W)) and self.is_entrance and self.player_at_entrance():
                    player_entering = True

            if player_entering:
                self.colliding_player.set_position(self.get_player_position(self.connecting_pipe))
                AssetPool.get_sound("assets/sounds/pipe.ogg").play()

    def player_at_entrance(self) -> bool:
        if self.colliding_player is None:
            return False
        
        min_ = self.game_object.transform.position - self.game_object.transform.scale * 0.5
        max_ = self.game_object.transform.position + self.game_object.transform.scale * 0.5
        player_min = self.colliding_player.game_object.transform.position - self.colliding_player.game_object.transform.scale * 0.5
        player_max = self.colliding_player.game_object.transform.position + self.colliding_player.game_object.transform.scale * 0.5

        ret = {
            Direction.Up: player_min.y >= max_.y and player_max.x > min_.x and player_min.x < max_.x,
            Direction.Down: player_max.y <= min_.y and player_max.x > min_.x and player_min.x < max_.x,
            Direction.Right: player_min.x >= max_.x and player_max.y > min_.y and player_min.y < max_.y,
            Direction.Left: player_min.x <= min_.x and player_max.y > min_.y and player_min.y < max_.y,
        }[self.direction]

        return ret

    def begin_collision(self, colliding_object: GameObject, contact: b2Contact, hit_normal: Vector2):
        player_controller: PlayerController = colliding_object.get_component(PlayerController)
        if player_controller is not None:
            self.colliding_player = player_controller

    def end_collision(self, colliding_object: GameObject, contact: b2Contact, hit_normal: Vector2):
        player_controller: PlayerController = colliding_object.get_component(PlayerController)
        if player_controller is not None:
            self.colliding_player = None

    def get_player_position(self, pipe: GameObject) -> Vector2:
        pipe_component: Pipe = pipe.get_component(Pipe)
        if pipe_component is None:
            return Vector2([0., 0.])
        offset = {
            Direction.Up: Vector2([0., 0.5]),
            Direction.Left: Vector2([-0.5, 0.]),
            Direction.Right: Vector2([0.5, 0.]),
            Direction.Down: Vector2([0., -0.5]),
        }[pipe_component.direction]

        return pipe.transform.position + offset