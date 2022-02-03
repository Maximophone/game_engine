from physics2d.components.collider import Collider
from util.serialization import serializable
from util.vectors import Vector2

@serializable("half_size")
class Box2DCollider(Collider):
    def __init__(self):
        self.half_size: Vector2 = Vector2([.25, .25])
        super().__init__()

    def editor_update(self, dt: float):
        from renderer.debug_draw import DebugDraw
        center = self.game_object.transform.position + self.offset
        DebugDraw.add_box_2D(center, self.half_size, self.game_object.transform.rotation)