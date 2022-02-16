from enum import Enum, auto
from this import d
from components.component import Component
from mario.components.ground import Ground
from components.sprite_renderer import SpriteRenderer
from components.state_machine import StateMachine
from mxeng.game_object import GameObject
from physics2d.components.pillbox_collider import PillboxCollider
from physics2d.components.rigid_body_2d import RigidBody2D
from mxeng.key_listener import KeyListener
from physics2d.enums.body_type import BodyType
from physics2d.physics2d import Physics2D
from util.asset_pool import AssetPool
from util.serialization import senum, serializable
from util.vectors import Color4, Vector2

import glfw
from Box2D import b2Contact

@senum
class PlayerState(Enum):
    Small = auto()
    Big = auto()
    Fire = auto()
    Invincible = auto()

@serializable("walk_speed", "jump_boost", "total_jump_time", "jump_impulse", "slow_down_force", "terminal_velocity", "player_state")
class PlayerController(Component):
    def __init__(self):
        self.walk_speed: float = 1.9
        self.jump_boost: float = 80.
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
        self.jump_time: float = 0.
        self.total_jump_time: float = 0.4
        self.acceleration: Vector2 = Vector2([0., 0.])
        self.velocity: Vector2 = Vector2([0., 0.])
        self.is_dead: bool = False
        self.enemy_bounce: int = 0

        self.hurt_invincibility_time_left: float = 0.
        self.hurt_invincibility_time: float = 1.4

        self.dead_min_height: float = 0.
        self.dead_max_height: float = 0.
        self.dead_going_up: bool = True
        self.blink_time: float = 0.
        self.spr: SpriteRenderer = None

        self.playing_win_animation: bool = False
        self.time_to_castle: float = 4.5
        self.walk_time: float = 2.2
        self.sent_event: bool = False

        self.player_state: PlayerState = PlayerState.Small
        super().__init__()

    def start(self):
        self.rb: RigidBody2D = self.game_object.get_component(RigidBody2D)
        self.state_machine: StateMachine = self.game_object.get_component(StateMachine)
        self.rb.gravity_scale = 0.
        self.spr: SpriteRenderer = self.game_object.get_component(SpriteRenderer)

    def update(self, dt: float):
        from mxeng.window import Window
        from mario.prefabs import Prefabs
        from mario.components.fireball import Fireball
        from mario.scenes.level_scene_initializer import LevelSceneInitializer
        if self.playing_win_animation:
            self.check_on_ground()
            if not self.on_ground:
                self.game_object.transform.scale.x = -0.25
                self.game_object.transform.position.y -= dt
                self.state_machine.trigger("stop_running")
                self.state_machine.trigger("stop_jumping")
            else:
                if self.walk_time > 0:
                    self.game_object.transform.scale.x = 0.25
                    self.game_object.transform.position.x += dt
                    self.state_machine.trigger("start_running")
                if not AssetPool.get_sound("mario/assets/sounds/stage_clear.ogg").is_playing:
                    AssetPool.get_sound("mario/assets/sounds/stage_clear.ogg").play()
                self.time_to_castle -= dt
                self.walk_time -= dt

                if self.time_to_castle < 0:
                    Window.queue_change_scene(LevelSceneInitializer())
            return


        if self.is_dead:
            if self.game_object.transform.position.y < self.dead_max_height and self.dead_going_up:
                self.game_object.transform.position.y += dt * self.walk_speed / 2.
            elif self.game_object.transform.position.y >= self.dead_max_height and self.dead_going_up:
                self.dead_going_up = False
            elif self.game_object.transform.position.y > self.dead_min_height and not self.dead_going_up:
                self.rb.body_type = BodyType.Kinematic
                self.acceleration.y = Window.get_physics().gravity.y * 0.7
                self.velocity.y += self.acceleration.y * dt
                self.velocity.y = max(min(self.velocity.y, self.terminal_velocity.y), -self.terminal_velocity.y)
                self.rb.velocity = self.velocity
                self.rb.angular_velocity = 0.
            elif self.game_object.transform.position.y <= self.dead_min_height:
                Window.queue_change_scene(LevelSceneInitializer())
            return

        if self.hurt_invincibility_time_left > 0:
            self.hurt_invincibility_time_left -= dt
            self.blink_time -= dt

            if self.blink_time <= 0:
                self.blink_time = 0.2
                if self.spr.get_color().w == 1:
                    self.spr.set_color(Color4([1., 1., 1., 0.]))
                else:
                    self.spr.set_color(Color4([1., 1., 1., 1.]))
            else:
                if self.spr.get_color().w == 0:
                    self.spr.set_color(Color4([1., 1., 1., 1.]))

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

        # FIREBALLS
        if KeyListener.key_begin_press(glfw.KEY_E) and self.player_state == PlayerState.Fire and Fireball.can_spawn():
            position = self.game_object.transform.position + (Vector2([0.26, 0.]) if self.game_object.transform.scale.x > 0 else Vector2([-0.26, 0.]))
            fireball = Prefabs.generate_fireball(position)
            fireball.get_component(Fireball).going_right = self.game_object.transform.scale.x > 0
            Window.get_scene().add_game_object_to_scene(fireball)


        self.check_on_ground()
        jump_key_pressed = KeyListener.is_key_pressed(glfw.KEY_SPACE) or KeyListener.is_key_pressed(glfw.KEY_UP)
        if jump_key_pressed and (
            self.jump_time > 0 or 
            self.on_ground or
            self.ground_debounce > 0
        ):
            # jump key is being pressed and we are on the ground or jumping
            if (self.on_ground or self.ground_debounce > 0) and self.jump_time <= 0:
                # just pressed the jump key
                AssetPool.get_sound("mario/assets/sounds/jump-small.ogg").play()
                self.jump_time = self.total_jump_time
                self.velocity.y = self.jump_impulse
                print(f"starting jump. total jump time: {self.total_jump_time}. jump impulse: {self.jump_impulse}. jump boost: {self.jump_boost}")
            elif self.jump_time > 0:
                # already jumping
                self.jump_time -= dt
                self.velocity.y = self.jump_time / 2.2 * self.jump_boost
                print(f"jump time: {self.jump_time}. dt: {dt:.03f}")
            else:
                print(self.on_ground, self.ground_debounce, self.jump_time)
                self.velocity.y = 0
            self.ground_debounce = 0
        elif self.enemy_bounce > 0:
            self.enemy_bounce -= 1
            self.velocity.y = self.enemy_bounce / 2.2 * self.jump_boost
        elif not self.on_ground:
            #print("in the air")
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
        inner_player_width = self.player_width * 0.6
        y_val = -0.14 if self.player_state == PlayerState.Small else -0.24

        self.on_ground = Physics2D.check_on_ground(self.game_object, inner_player_width, y_val)

    def set_position(self, new_position: Vector2):
        self.game_object.transform.position = new_position.copy()
        self.rb.set_position(new_position.copy())

    def powerup(self):
        if self.player_state == PlayerState.Small:
            self.player_state = PlayerState.Big
            AssetPool.get_sound("mario/assets/sounds/powerup.ogg").play()
            self.game_object.transform.scale.y = 0.42
            pb: PillboxCollider = self.game_object.get_component(PillboxCollider)
            if pb is not None:
                self.jump_boost *= self.big_jump_boost_factor
                self.walk_speed *= self.big_jump_boost_factor
                pb.height = 0.63
        elif self.player_state == PlayerState.Big:
            self.player_state = PlayerState.Fire
            AssetPool.get_sound("mario/assets/sounds/powerup.ogg").play()
        
        self.state_machine.trigger("powerup")

    def play_win_animation(self, flagpole: GameObject):
        if not self.playing_win_animation:
            self.playing_win_animation = True
            self.velocity = Vector2([0., 0.])
            self.acceleration = Vector2([0., 0.])
            self.rb.velocity = Vector2([0., 0.])
            self.rb.is_sensor = True
            self.rb.body_type = BodyType.Static
            self.game_object.transform.position.x = flagpole.transform.position.x
            AssetPool.get_sound("mario/assets/sounds/flagpole.ogg").play()

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

    def is_hurt_invincible(self) -> bool:
        return self.hurt_invincibility_time_left > 0 or self.playing_win_animation

    def is_invincible(self) -> bool:
        return self.player_state == PlayerState.Invincible or self.is_hurt_invincible() or self.playing_win_animation

    def bounce_on_enemy(self):
        self.enemy_bounce = 8

    def die(self):
        self.state_machine.trigger("die")
        if self.player_state == PlayerState.Small:
            self.velocity = Vector2([0., 0.])
            self.acceleration = Vector2([0., 0.])
            self.rb.velocity = Vector2([0., 0.])
            self.is_dead = True
            self.rb.is_sensor = True
            AssetPool.get_sound("mario/assets/sounds/mario_die.ogg").play()
            self.dead_max_height = self.game_object.transform.position.y + 0.3
            self.rb.body_type = BodyType.Static
            if self.game_object.transform.position.y > 0:
                self.dead_min_height = -0.25
        elif self.player_state == PlayerState.Big:
            self.player_state = PlayerState.Small
            self.game_object.transform.scale.y = 0.25
            pb: PillboxCollider = self.game_object.get_component(PillboxCollider)
            if pb is not None:
                self.jump_boost /= self.big_jump_boost_factor
                self.walk_speed /= self.big_jump_boost_factor
                pb.height = 0.31
            self.hurt_invincibility_time_left = self.hurt_invincibility_time
            AssetPool.get_sound("mario/assets/sounds/pipe.ogg").play()
        elif self.player_state == PlayerState.Fire:
            self.player_state = PlayerState.Big
            self.hurt_invincibility_time_left = self.hurt_invincibility_time
            AssetPool.get_sound("mario/assets/sounds/pipe.ogg").play()


    