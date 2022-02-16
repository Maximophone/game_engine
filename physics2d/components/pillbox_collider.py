from physics2d.components.box_2d_collider import Box2DCollider
from physics2d.components.circle_collider import CircleCollider
from physics2d.components.collider import Collider
from physics2d.components.rigid_body_2d import RigidBody2D
from util.serialization import serializable, sproperty
from util.vectors import Vector2

@serializable()
class PillboxCollider(Collider):
    def __init__(self):
        self.top_circle: CircleCollider = CircleCollider()
        self.bottom_circle: CircleCollider = CircleCollider()
        self.box: Box2DCollider = Box2DCollider()
        self.reset_fixture_next_frame: bool = False

        self._width = 0.1
        self._height = 0.2
        super().__init__()

    @sproperty
    def width(self):
        return self._width

    @width.setter
    def width(self, value: float):
        self._width = value
        self.recalculate_colliders()
        self.reset_fixture()

    @sproperty
    def height(self):
        return self._height

    @height.setter
    def height(self, value: float):
        self._height = value
        self.recalculate_colliders()
        self.reset_fixture()

    def start(self):
        self.top_circle.game_object = self.game_object
        self.bottom_circle.game_object = self.game_object
        self.box.game_object = self.game_object
        self.recalculate_colliders()

    def reset_fixture(self):
        from mxeng.window import Window
        if Window.get_physics().is_locked():
            self.reset_fixture_next_frame = True
            return
        self.reset_fixture_next_frame = False
        if self.game_object is not None:
            rb = self.game_object.get_component(RigidBody2D)
            if rb is not None:
                Window.get_physics().reset_pillbox_collider(rb, self)

    def recalculate_colliders(self):
        circle_radius = self.width / 4
        box_height = self.height - 2 * circle_radius
        self.top_circle.radius = circle_radius
        self.bottom_circle.radius = circle_radius
        self.top_circle.offset = self.offset + Vector2([0., box_height / 4.])
        self.bottom_circle.offset = self.offset - Vector2([0., box_height / 4.])
        self.box.half_size = Vector2([self.width / 2. - 0.01, box_height / 2.])
        self.box.offset = self.offset

    def editor_update(self, dt: float):
        self.top_circle.editor_update(dt)
        self.bottom_circle.editor_update(dt)
        self.box.editor_update(dt)

        if self.reset_fixture_next_frame:
            self.reset_fixture()

    def update(self, dt: float):
        if self.reset_fixture_next_frame:
            self.reset_fixture()