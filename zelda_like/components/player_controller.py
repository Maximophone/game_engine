from components.component import Component
from components.state_machine import StateMachine
from mxeng.direction import Direction
from util.serialization import serializable
from mxeng.key_listener import KeyListener

import math
import glfw

@serializable("walk_speed", "jump_speed", "jump_time", "jump_curve")
class PlayerController(Component):
    def __init__(self):
        self.walk_speed: float = 0.8
        self.jump_speed: float = 1.4
        self.jump_time: float = 0.3
        self.jump_time_left: float = 0.
        self.jump_curve: float = 0.5
        self.state_machine: StateMachine = None
        self.direction: Direction = Direction.Down
        self.jumping: bool = False
        self.jumping_direction: Direction = Direction.Down
        super().__init__()

    def start(self):
        self.state_machine = self.game_object.get_component(StateMachine)

    def update(self, dt: float):

        if not self.jumping:
            if KeyListener.is_key_pressed(glfw.KEY_SPACE):
                self.state_machine.trigger("jump")
                self.jumping = True
                self.jump_time_left = self.jump_time
                self.jumping_direction = self.direction
            elif KeyListener.is_key_pressed(glfw.KEY_ENTER):
                self.state_machine.trigger("attack")
            elif KeyListener.is_key_pressed(glfw.KEY_LEFT):
                self.state_machine.trigger("go_left")
                self.direction = Direction.Left
                self.game_object.transform.position.x -= self.walk_speed * dt
            elif KeyListener.is_key_pressed(glfw.KEY_RIGHT):
                self.state_machine.trigger("go_right")
                self.direction = Direction.Right
                self.game_object.transform.position.x += self.walk_speed * dt
            elif KeyListener.is_key_pressed(glfw.KEY_UP):
                self.state_machine.trigger("go_up")
                self.direction = Direction.Up
                self.game_object.transform.position.y += self.walk_speed * dt
            elif KeyListener.is_key_pressed(glfw.KEY_DOWN):
                self.state_machine.trigger("go_down")
                self.direction = Direction.Down
                self.game_object.transform.position.y -= self.walk_speed * dt
            else:
                self.state_machine.trigger("stop")
        else:
            if self.jumping_direction == Direction.Left:
                self.game_object.transform.position.x -= self.jump_speed * dt
            elif self.jumping_direction == Direction.Right:
                self.game_object.transform.position.x += self.jump_speed * dt
            elif self.jumping_direction == Direction.Down:
                self.game_object.transform.position.y -= self.jump_speed * dt
            elif self.jumping_direction == Direction.Up:
                self.game_object.transform.position.y += self.jump_speed * dt
            correction_term = self.jump_curve * 0.7
            self.game_object.transform.position.y -= self.jump_curve * dt * math.cos(
                self.jump_time_left/self.jump_time*math.pi - correction_term
                )
            self.jump_time_left -= dt
        if self.jumping and self.jump_time_left < 0:
            self.jumping = False
            self.state_machine.trigger("stop")