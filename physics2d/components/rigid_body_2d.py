from cmath import pi
from util.serialization import serializable, sproperty
from util.vectors import Vector2
from components.component import Component
from physics2d.enums.body_type import BodyType

from Box2D import b2Body

@serializable("angular_damping", "linear_damping", "mass", "body_type", "fixed_rotation", "is_continuous_collision", "friction")
class RigidBody2D(Component):
    def __init__(self):
        self._velocity: Vector2 = Vector2()
        self.angular_damping: float = 0.8
        self.linear_damping: float = 0.9
        self.mass: float = 0
        self.body_type: BodyType = BodyType.Dynamic
        self.friction: float = 0.1
        self._angular_velocity: float = 0.
        self._gravity_scale: float = 1.0
        self._is_sensor: bool = False

        self.fixed_rotation: bool = False
        self.is_continuous_collision: bool = True

        self.raw_body: b2Body = None
        super().__init__()

    @sproperty
    def velocity(self) -> Vector2:
        return self._velocity

    @velocity.setter
    def velocity(self, value: Vector2):
        self._velocity = value
        if self.raw_body is not None:
            self.raw_body.linearVelocity = value.to_b2vec2()

    @sproperty
    def angular_velocity(self) -> float:
        return self._angular_velocity

    @angular_velocity.setter
    def angular_velocity(self, value: float):
        self._angular_velocity = value
        if self.raw_body is not None:
            self.raw_body.angularVelocity = value

    @sproperty
    def gravity_scale(self) -> float:
        return self._gravity_scale

    @gravity_scale.setter
    def gravity_scale(self, value: float):
        self._gravity_scale = value
        if self.raw_body is not None:
            self.raw_body.gravityScale = value

    @sproperty
    def is_sensor(self) -> bool:
        return self._is_sensor

    @is_sensor.setter
    def is_sensor(self, value: bool):
        from mxeng.window import Window
        self._is_sensor = value
        if self.raw_body is not None:
            if value:
                Window.get_physics().set_is_sensor(self)
            else:
                Window.get_physics().set_not_sensor(self)

    def add_velocity(self, force_to_add: Vector2):
        if self.raw_body is not None:
            self.raw_body.ApplyForceToCenter(force_to_add.to_b2vec2())

    def add_impulse(self, impulse: Vector2):
        if self.raw_body is not None:
            self.raw_body.ApplyLinearImpulse(impulse.to_b2vec2(), self.raw_body.worldCenter)

    def update(self, dt: float):
        if self.raw_body is not None:
            self.game_object.transform.position = Vector2(self.raw_body.position)
            self.game_object.transform.rotation = self.raw_body.angle/2./pi*360.

