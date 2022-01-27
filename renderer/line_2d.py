from pyrr import Vector3
import numpy as np

class Line2D:
    def __init__(self, from_: np.ndarray, to: np.ndarray, color: Vector3, lifetime: int):
        self._from: np.ndarray = from_
        self._to: np.ndarray = to
        self._color: Vector3 = color
        self._lifetime: int = lifetime

    @property
    def from_(self) -> np.ndarray:
        return self._from

    @property
    def to(self) -> np.ndarray:
        return self._to

    @property
    def color(self) -> Vector3:
        return self._color

    @property
    def lifetime(self) -> int:
        return self._lifetime

    def begin_frame(self) -> int:
        self._lifetime -= 1
        return self._lifetime