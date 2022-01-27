from typing import Optional
import numpy as np

from util.serialization import serializable
from util.vectors import Vector2

@serializable("position", "scale")
class Transform:
    def __init__(self, position: Vector2 = None, scale: Vector2 = None):
        self.position = position if position is not None else Vector2([0.,0.])
        self.scale = scale if scale is not None else Vector2([1.,1.])

    def copy(self, to: "Transform" = None) -> Optional["Transform"]:
        if to is None:
            return Transform(self.position.copy(), self.scale.copy())
        else:
            to.position[:] = self.position.copy()
            to.scale[:] = self.scale.copy()

    def __eq__(self, o: object):
        if o is None or not isinstance(o, Transform):
            return False
        return (o.position == self.position) and (o.scale == self.scale) 