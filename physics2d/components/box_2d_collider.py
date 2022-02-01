from physics2d.components.collider import Collider
from util.serialization import serializable
from util.vectors import Vector2

@serializable("half_size")
class Box2DCollider(Collider):
    def __init__(self):
        self.half_size: Vector2 = Vector2([1., 1.])
        super().__init__()