from physics2d.components.collider import Collider
from util.serialization import serializable

@serializable("radius")
class CircleCollider(Collider):
    def __init__(self):
        self.radius: float = 1.
        super().__init__()

    def editor_update(self, dt: float):
        from renderer.debug_draw import DebugDraw
        center = self.game_object.transform.position + self.offset
        DebugDraw.add_circle(center, self.radius)