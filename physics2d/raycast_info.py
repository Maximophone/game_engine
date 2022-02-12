from Box2D import b2RayCastCallback, b2Fixture, b2Vec2
from numpy import fix
from mxeng.game_object import GameObject

from util.vectors import Vector2

class RaycastInfo(b2RayCastCallback):
    def __init__(self, requesting_object: GameObject):
        self.fixture: b2Fixture = None
        self.point: Vector2 = Vector2()
        self.normal: Vector2 = Vector2()
        self.fraction: float = 0.
        self.hit: bool = False
        self.hit_object: GameObject = None
        self.requesting_object: GameObject = requesting_object

    def ReportFixture(self, fixture: b2Fixture, point: b2Vec2, normal: b2Vec2, fraction: float) -> float:
        if fixture.userData == self.requesting_object:
            return 1.
        self.fixture = fixture
        self.point = Vector2(point)
        self.normal = Vector2(normal)
        self.fraction = fraction
        self.hit = fraction != 0.
        self.hit_object = fixture.userData

        return fraction
        