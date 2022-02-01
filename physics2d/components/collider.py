from util.serialization import serializable
from util.vectors import Vector2
from components.component import Component

@serializable("offset", "origin")
class Collider(Component):
    def __init__(self):
        self.offset: Vector2 = Vector2()
        self.origin: Vector2 = Vector2() # WARNING: should this be in box 2d collider
        super().__init__()