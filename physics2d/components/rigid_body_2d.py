from cmath import pi
from util.serialization import serializable
from util.vectors import Vector2
from components.component import Component
from physics2d.enums.body_type import BodyType

from Box2D import b2Body

@serializable("velocity", "angular_damping", "linear_damping", "mass", "body_type", "fixed_rotation", "is_continuous_collision")
class RigidBody2D(Component):
    def __init__(self):
        self.velocity: Vector2 = Vector2()
        self.angular_damping: float = 0.8
        self.linear_damping: float = 0.9
        self.mass: float = 0
        self.body_type: BodyType = BodyType.Dynamic

        self.fixed_rotation: bool = False
        self.is_continuous_collision: bool = True

        self.raw_body: b2Body = None
        super().__init__()

    def update(self, dt: float):
        if self.raw_body is not None:
            self.game_object.transform.position = Vector2(self.raw_body.position)
            self.game_object.transform.rotation = self.raw_body.angle/2./pi*360.

