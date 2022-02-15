from components.component import Component
from mario.components.goomba_ai import GoombaAI
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
class TurtleAI(Component):
    def __init__(self):
        self.going_right: bool = False
        self.rb: RigidBody2D = None
        self.walk_speed: float = 0.6
        self.velocity: Vector2 = Vector2([0., 0.])
        self.acceleration: Vector2 = Vector2([0., 0.])
        self.terminal_velocity: Vector2 = Vector2([2.1, 3.1])
        self.on_ground: bool = False
        self.is_dead: bool = False
        self.is_moving: bool = False
        self.state_machine: StateMachine = None
        self.moving_debounce: float = 0.32
        super().__init__()

    def start(self):
        from mxeng.window import Window
        self.state_machine = self.game_object.get_component(StateMachine)
        self.rb = self.game_object.get_component(RigidBody2D)
        self.acceleration.y = Window.get_physics().gravity.y * 0.7

    def update(self, dt: float):
        from mxeng.window import Window
        camera = Window.get_scene().camera()
        self.moving_debounce -= dt
        if self.game_object.transform.position.x > camera.position.x + camera.projection_size.x * camera.zoom:
            # turtle is outside of camera
            return
        
        if not self.is_dead or self.is_moving:
            if self.going_right:
                self.game_object.transform.scale.x = -0.25
                self.velocity.x = self.walk_speed
            else:
                self.game_object.transform.scale.x = 0.25
                self.velocity.x = -self.walk_speed
        else:
            self.velocity.x = 0

        self.check_on_ground()
        if self.on_ground:
            self.acceleration.y = 0
            self.velocity.y = 0
        else:
            self.acceleration.y = Window.get_physics().gravity.y * 0.7
        self.velocity.y += self.acceleration.y * dt
        self.velocity.y = max(min(self.velocity.y, self.terminal_velocity.y), -self.terminal_velocity.y)
        self.rb.velocity = self.velocity

        if self.game_object.transform.position.x < camera.position.x - 0.5 or self.game_object.transform.position.y < -20.:
            # fallen off or behind camera
            self.game_object.destroy()

    def check_on_ground(self):
        inner_player_width = 0.25 * 0.7
        y_val = -0.2
        self.on_ground = Physics2D.check_on_ground(self.game_object, inner_player_width, y_val)

    def stomp(self):
        self.is_dead = True
        self.is_moving = False
        self.velocity = Vector2([0., 0.])
        self.rb.velocity = Vector2([0., 0.])
        self.rb.angular_velocity = 0.
        self.rb.gravity_scale = 0.
        self.state_machine.trigger("squash_me")
        AssetPool.get_sound("assets/sounds/bump.ogg").play()
        
    def begin_collision(self, colliding_object: GameObject, contact: b2Contact, hit_normal: Vector2):
        player_controller: PlayerController = colliding_object.get_component(PlayerController)
        if player_controller is not None:
            if not self.is_dead and not player_controller.is_dead and not player_controller.is_hurt_invincible() and hit_normal.y > 0.58:
                # turtle being hit in the head
                player_controller.bounce_on_enemy()
                self.stomp()
                self.walk_speed *= 3.0
            elif self.moving_debounce < 0 and not player_controller.is_dead and not player_controller.is_hurt_invincible() and (self.is_moving or not self.is_dead) and hit_normal.y < 0.58:
                # player has bounced away, is not dead or invincible, turtle moving or not dead and horizontal contact
                player_controller.die()
            elif not player_controller.is_dead and not player_controller.is_hurt_invincible():
                # player has hit turtle while dead or moving
                if self.is_dead and hit_normal.x > 0.58:
                    player_controller.bounce_on_enemy()
                    self.is_moving = not self.is_moving
                    self.going_right = hit_normal.x < 0
                elif self.is_dead and not self.is_moving:
                    self.is_moving = True
                    self.going_right = hit_normal.x < 0
                    self.moving_debounce = 0.32
        elif abs(hit_normal.y) < 0.1 and not colliding_object.is_dead:
            self.going_right = hit_normal.x < 0
            if self.is_moving and self.is_dead:
                AssetPool.get_sound("assets/sounds/bump.ogg").play()


    def pre_solve(self, colliding_object: GameObject, contact: b2Contact, hit_normal: Vector2):
        goomba: GoombaAI = colliding_object.get_component(GoombaAI)
        if self.is_dead and self.is_moving and goomba is not None:
            goomba.stomp()
            contact.enabled = False
            AssetPool.get_sound("assets/sounds/kick.ogg").play()
