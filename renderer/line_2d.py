from util.vectors import Color3, Vector2

class Line2D:
    def __init__(self, from_: Vector2, to: Vector2, color: Color3, lifetime: int):
        self._from: Vector2 = from_
        self._to: Vector2 = to
        self._color: Color3 = color
        self._lifetime: int = lifetime

    @property
    def from_(self) -> Vector2:
        return self._from

    @property
    def to(self) -> Vector2:
        return self._to

    @property
    def color(self) -> Color3:
        return self._color

    @property
    def lifetime(self) -> int:
        return self._lifetime

    def begin_frame(self) -> int:
        self._lifetime -= 1
        return self._lifetime