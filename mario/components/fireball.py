from components.component import Component
from mario.components.goomba_ai import GoombaAI
from mario.components.player_controller import PlayerController
from mario.components.turtle_ai import TurtleAI
from mxeng.game_object import GameObject
from physics2d.components.rigid_body_2d import RigidBody2D
from physics2d.physics2d import Physics2D
from util.serialization import serializable
from util.vectors import Vector2

from Box2D import b2Contact

@serializable("fireball_speed", "lifetime")
class Fireball(Component):
    fireball_count: int = 0

    def __init__(self):
        self.going_right: bool = False
        self.rb: RigidBody2D = None
        self.fireball_speed: float = 1.7
        self.velocity: Vector2 = Vector2([0., 0.])
        self.acceleration: Vector2 = Vector2([0., 0.])
        self.terminal_velocity: Vector2 = Vector2([2.1, 3.1])
        self.on_ground: bool = False
        self.lifetime: float = 4.
        super().__init__()

    @staticmethod
    def can_spawn():
        return Fireball.fireball_count < 4

    def start(self):
        from mxeng.window import Window
        self.rb = self.game_object.get_component(RigidBody2D)
        self.acceleration.y = Window.get_physics().gravity.y * 0.7
        Fireball.fireball_count += 1

    def update(self, dt: float):
        from mxeng.window import Window

        self.lifetime -= dt

        if self.lifetime <= 0:
            self.disappear()
            return

        if self.going_right:
            self.velocity.x = self.fireball_speed
        else:
            self.velocity.x = -self.fireball_speed

        self.check_on_ground()
        if self.on_ground:
            self.acceleration.y = 1.5
            self.velocity.y = 2.5
        else:
            self.acceleration.y = Window.get_physics().gravity.y * 0.7
        
        self.velocity.y += self.acceleration.y * dt

        self.velocity.y = max(min(self.velocity.y, self.terminal_velocity.y), -self.terminal_velocity.y)
        self.rb.velocity = self.velocity

    def check_on_ground(self):
        inner_player_width = 0.25 * 0.7
        y_val = -0.09
        self.on_ground = Physics2D.check_on_ground(self.game_object, inner_player_width, y_val)

    def begin_collision(self, colliding_object: GameObject, contact: b2Contact, hit_normal: Vector2):
        if abs(hit_normal.x) > 0.8:
            self.going_right = hit_normal.x < 0

        for comp_class in [TurtleAI, GoombaAI]:
            if (comp:=colliding_object.get_component(comp_class)) is not None:
                comp.stomp()
                self.disappear()

    def pre_solve(self, colliding_object: GameObject, contact: b2Contact, hit_normal: Vector2):
        if colliding_object.get_component(PlayerController) is not None or colliding_object.get_component(Fireball) is not None:
            # does not collide with mario or other fireball
            contact.enabled = False

    def disappear(self):
        Fireball.fireball_count -= 1
        self.game_object.destroy()
