from typing import Optional
import numpy as np
from editor.mx_imgui import MXImGUI

from util.serialization import serializable
from util.vectors import Vector2
from components.component import Component

@serializable("position", "scale", "rotation", "z_index")
class Transform(Component):
    def __init__(self, position: Vector2 = None, scale: Vector2 = None):
        self.position = position if position is not None else Vector2([0.,0.])
        self.scale = scale if scale is not None else Vector2([1.,1.])
        self.rotation: float = 0.
        self.z_index: int = 0
        super().__init__()

    def copy(self, to: "Transform" = None) -> Optional["Transform"]:
        if to is None:
            return Transform(self.position.copy(), self.scale.copy())
        else:
            to.position[:] = self.position.copy()
            to.scale[:] = self.scale.copy()

    def __eq__(self, o: object):
        if o is None or not isinstance(o, Transform):
            return False
        return (o.position == self.position) and (o.scale == self.scale) and (o.rotation == self.rotation) and (o.z_index == self.z_index)