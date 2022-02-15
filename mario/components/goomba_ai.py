from components.component import Component
from mario.components.player_controller import PlayerController
from components.state_machine import StateMachine
from mxeng.game_object import GameObject
from physics2d.components.rigid_body_2d import RigidBody2D
from physics2d.physics2d import Physics2D
from util.asset_pool import AssetPool
from util.serialization import serializable
from util.vectors import Vector2

from Box2D import b2Contact

@serializable()
class GoombaAI(Component):
    def __init__(self):
        self.on_ground: bool = False
        self.going_right: bool = False
        self.rb: RigidBody2D = None
        self.walk_speed: float = 0.6
        self.velocity = Vector2([0., 0.])
        self.acceleration = Vector2([0., 0.])
        self.terminal_velocity = Vector2([0., 0.])
        self.is_dead: bool = False
        self.time_to_kill: float = 0.5
        self.state_machine: StateMachine = None
        super().__init__()

    def start(self):
        from mxeng.window import Window
        self.state_machine = self.game_object.get_component(StateMachine)
        self.rb = self.game_object.get_component(RigidBody2D)
        self.acceleration.y = Window.get_physics().gravity.y * 0.7

    def update(self, dt: float):
        from mxeng.window import Window
        camera = Window.get_scene().camera()
        if self.game_object.transform.position.x > camera.position.x + camera.projection_size.x * camera.zoom:
            # if goomba not in camera, we do not update it
            return

        if self.is_dead:
            self.time_to_kill -= dt
            if self.time_to_kill <= 0:
                self.game_object.destroy()
            self.rb.velocity = Vector2([0., 0.])
            return

        if self.going_right:
            self.velocity.x = self.walk_speed
        else:
            self.velocity.x = -self.walk_speed

        self.check_on_ground()
        if self.on_ground:
            self.acceleration.y = 0
            self.velocity.y = 0
        else:
            self.acceleration.y = Window.get_physics().gravity.y * 0.7
        
        self.velocity.y += self.acceleration.y * dt
        self.velocity.y = max(min(self.velocity.y, self.terminal_velocity.y), -self.terminal_velocity.y)
        self.rb.velocity = self.velocity

    def check_on_ground(self):
        inner_player_width = 0.25 * 0.7
        y_val = -0.14
        self.on_ground = Physics2D.check_on_ground(self.game_object, inner_player_width, y_val)

    def pre_solve(self, colliding_object: GameObject, contact: b2Contact, hit_normal: Vector2):
        if self.is_dead:
            return
        player_controler: PlayerController = colliding_object.get_component(PlayerController)
        if player_controler is not None:
            # we hit the player
            if not player_controler.is_dead and not player_controler.is_hurt_invincible() and hit_normal.y > 0.58:
                # this hit normal checks if the player jumped on the goomba
                player_controler.bounce_on_enemy()
                self.stomp()
                pass
            elif not player_controler.is_dead and not player_controler.is_invincible():
                # player takes damage
                player_controler.die()
                if not player_controler.is_dead:
                    contact.enabled = False
            elif not player_controler.is_dead and player_controler.is_invincible():
                contact.enabled = False
        elif abs(hit_normal.y) < 0.1:
            # we hit an object
            self.going_right = hit_normal.x < 0

    def stomp(self, play_sound: bool = True):
        self.is_dead = True
        self.velocity = Vector2([0., 0.])
        self.rb.velocity = Vector2([0., 0.])
        self.rb.angular_velocity = 0.
        self.rb.gravity_scale = 0.
        self.state_machine.trigger("squash_me")
        self.rb.is_sensor = True
        if play_sound:
            AssetPool.get_sound("assets/sounds/bump.ogg").play()
