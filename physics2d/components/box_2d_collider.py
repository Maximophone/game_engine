from components.component import Component
from util.vectors import Vector2

class Box2DCollider(Component):
    def __init__(self):
        self.half_size: Vector2 = Vector2([1., 1.])