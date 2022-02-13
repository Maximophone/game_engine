from components.component import Component
from components.state_machine import StateMachine
from physics2d.components.rigid_body_2d import RigidBody2D
from mxeng.key_listener import KeyListener
from util.serialization import serializable
from util.vectors import Vector2

import glfw

@serializable("walk_speed", "jump_boost", "jump_impulse", "slow_down_force", "terminal_velocity")
class PlayerController(Component):
    def __init__(self):
        self.walk_speed: float = 1.9
        self.jump_boost: float = 1.0
        self.jump_impulse: float = 3.0
        self.slow_down_force: float = 0.05
        self.terminal_velocity: Vector2 = Vector2([2.1, 3.1])

        self.on_ground: bool = False
        self.ground_debounce: float = 0.
        self.ground_debounce_time: float = 0.1

        self.rb: RigidBody2D = None
        self.state_machine: StateMachine = None
        self.big_jump_boost_factor: float = 1.05
        self.player_width: float = 0.25
        self.jump_time: int = 0
        self.acceleration: Vector2 = Vector2([0., 0.])
        self.velocity: Vector2 = Vector2([0., 0.])
        self.is_dead: bool = False
        self.enemy_bounce: int = 0
        super().__init__()

    def start(self):
        self.rb: RigidBody2D = self.game_object.get_component(RigidBody2D)
        self.state_machine: StateMachine = self.game_object.get_component(StateMachine)
        self.rb.gravity_scale = 0.

    def update(self, dt: float):
        from mxeng.window import Window
        if KeyListener.is_key_pressed(glfw.KEY_RIGHT) or KeyListener.is_key_pressed(glfw.KEY_D):
            self.game_object.transform.scale.x = self.player_width
            self.acceleration.x = self.walk_speed

            if self.velocity.x < 0:
                self.state_machine.trigger("switch_direction")
                self.velocity.x += self.slow_down_force
            else:
                self.state_machine.trigger("start_running")
        elif KeyListener.is_key_pressed(glfw.KEY_LEFT) or KeyListener.is_key_pressed(glfw.KEY_A):
            self.game_object.transform.scale.x = -self.player_width
            self.acceleration.x = -self.walk_speed

            if self.velocity.x > 0:
                self.state_machine.trigger("switch_direction")
                self.velocity.x -= self.slow_down_force
            else:
                self.state_machine.trigger("start_running")
        else:
            self.acceleration.x = 0
            if self.velocity.x > 0:
                self.velocity.x = max(0, self.velocity.x - self.slow_down_force)
            elif self.velocity.x <0:
                self.velocity.x = min(0, self.velocity.x + self.slow_down_force)

            if self.velocity.x == 0:
                self.state_machine.trigger("stop_running")

        self.acceleration.y = Window.get_physics().gravity.y * 0.7
        
        self.velocity.x += self.acceleration.x * dt
        self.velocity.y += self.acceleration.y * dt
        self.velocity.x = max(min(self.velocity.x, self.terminal_velocity.x), -self.terminal_velocity.x)
        self.velocity.y = max(min(self.velocity.y, self.terminal_velocity.y), -self.terminal_velocity.y)

        self.rb.velocity = self.velocity
        self.rb.angular_velocity = 0.

    