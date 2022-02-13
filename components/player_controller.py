from enum import Enum, auto
from components.component import Component
from components.ground import Ground
from components.state_machine import StateMachine
from mxeng.game_object import GameObject
from physics2d.components.pillbox_collider import PillboxCollider
from physics2d.components.rigid_body_2d import RigidBody2D
from mxeng.key_listener import KeyListener
from util.asset_pool import AssetPool
from util.serialization import senum, serializable
from util.vectors import Color3, Vector2

import glfw
from Box2D import b2Contact

@senum
class PlayerState(Enum):
    Small = auto()
    Big = auto()
    Fire = auto()
    Invincible = auto()

@serializable("walk_speed", "jump_boost", "jump_impulse", "slow_down_force", "terminal_velocity", "player_state")
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

        self.player_state: PlayerState = PlayerState.Small
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

        self.check_on_ground()
        jump_key_pressed = KeyListener.is_key_pressed(glfw.KEY_SPACE) or KeyListener.is_key_pressed(glfw.KEY_UP)
        if jump_key_pressed and (
            self.jump_time > 0 or 
            self.on_ground or
            self.ground_debounce > 0
        ):
            if (self.on_ground or self.ground_debounce > 0) and self.jump_time == 0:
                # just pressed the jump key
                AssetPool.get_sound("assets/sounds/jump-small.ogg").play()
                self.jump_time = 28
                self.velocity.y = self.jump_impulse
            elif self.jump_time > 0:
                self.jump_time -= 1
                self.velocity.y = self.jump_time / 2.2 * self.jump_boost
            else:
                self.velocity.y = 0
            self.ground_debounce = 0
        elif not self.on_ground:
            # we are in the air
            if self.jump_time > 0:
                self.velocity.y *= 0.35
                self.jump_time = 0
            self.ground_debounce -= dt
            self.acceleration.y = Window.get_physics().gravity.y * 0.7
        else:
            # we are on the ground
            self.velocity.y = 0
            self.acceleration.y = 0
            self.ground_debounce = self.ground_debounce_time
        
        self.velocity.x += self.acceleration.x * dt
        self.velocity.y += self.acceleration.y * dt
        self.velocity.x = max(min(self.velocity.x, self.terminal_velocity.x), -self.terminal_velocity.x)
        self.velocity.y = max(min(self.velocity.y, self.terminal_velocity.y), -self.terminal_velocity.y)

        self.rb.velocity = self.velocity
        self.rb.angular_velocity = 0.

        if not self.on_ground:
            self.state_machine.trigger("jump")
        else:
            self.state_machine.trigger("stop_jumping")

    def has_won(self) -> bool:
        return False

    def check_on_ground(self):
        from mxeng.window import Window
        from renderer.debug_draw import DebugDraw
        raycast_begin = self.game_object.transform.position.copy()
        inner_player_width = self.player_width * 0.6
        raycast_begin = raycast_begin - Vector2([inner_player_width/2., 0.])
        y_val = -0.14 if self.player_state == PlayerState.Small else -0.24
        raycast_end = raycast_begin + Vector2([0., y_val])
        info = Window.get_physics().raycast(self.game_object, raycast_begin, raycast_end)

        raycast2_begin = raycast_begin + Vector2([inner_player_width, 0.])
        raycast2_end = raycast_end + Vector2([inner_player_width, 0.])
        info2 = Window.get_physics().raycast(self.game_object, raycast2_begin, raycast2_end)

        self.on_ground = (
            (info.hit and info.hit_object is not None and info.hit_object.get_component(Ground) is not None) or
            (info2.hit and info2.hit_object is not None and info2.hit_object.get_component(Ground) is not None)
        )

        #DebugDraw.add_line_2D(raycast_begin, raycast_end, Color3([1., 0., 0.]))
        #DebugDraw.add_line_2D(raycast2_begin, raycast2_end, Color3([1., 0., 0.]))

    def powerup(self):
        if self.player_state == PlayerState.Small:
            self.player_state = PlayerState.Big
            AssetPool.get_sound("assets/sounds/powerup.ogg").play()
            self.game_object.transform.scale.y = 0.42
            pb: PillboxCollider = self.game_object.get_component(PillboxCollider)
            if pb is not None:
                self.jump_boost *= self.big_jump_boost_factor
                self.walk_speed *= self.big_jump_boost_factor
                pb.height = 0.63
        elif self.player_state == PlayerState.Big:
            self.player_state = PlayerState.Fire
            AssetPool.get_sound("assets/sounds/powerup.ogg").play()
        
        self.state_machine.trigger("powerup")

    def begin_collision(self, colliding_object: GameObject, contact: b2Contact, hit_normal: Vector2):
        if self.is_dead:
            return
        
        if colliding_object.get_component(Ground) is not None:
            if abs(hit_normal.x) > 0.8:
                # are we hitting horizontally
                self.velocity.x = 0
            elif hit_normal.y > 0.8:
                # if hitting bottom of block with player head
                self.velocity.y = 0
                self.acceleration.y = 0
                self.jump_time = 0


    