from pyrr import Vector3, Vector4
from mxeng.component import Component

from util.serialization import serializable

@serializable("_collider_type", "_friction", "_velocity")
class RigidBody(Component):
    def __init__(self):
        self._collider_type: int = 0
        self._friction: float = 0.8
        self._velocity: Vector3 = Vector3([0, 0.5, 0])
        self._tmp: Vector4 = Vector4([0, 0, 0, 0])