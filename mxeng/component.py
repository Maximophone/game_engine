from abc import abstractmethod
import imgui.core
from pyrr import Vector3, Vector4
import numpy as np

from util.serialization import serializable


class Component:
    def __init__(self):
        self.game_object: "GameObject" = None

    def update(self, dt: float):
        pass

    def start(self):
        pass

    def imgui(self):
        serial = getattr(self, "__serial")
        for name, value in self.__dict__.items():    
            if name not in serial:
                continue
            typ = type(value)

            if typ == int:
                changed, new_value = imgui.core.drag_int(f"{name}: ", value)
                if changed:
                    setattr(self, name, new_value)
            elif typ == float:
                changed, new_value = imgui.core.drag_float(f"{name}: ", value)
                if changed:
                    setattr(self, name, new_value)
            elif typ == bool:
                changed, new_value = imgui.core.checkboc(f"{name}: ", value)
                if changed:
                    setattr(self, name, new_value)
            elif typ == Vector3:
                changed, new_value = imgui.core.drag_float3(f"{name}: ", value[0], value[1], value[2])
                if changed:
                    setattr(self, name, Vector3(new_value))
            elif typ == Vector4:
                changed, new_value = imgui.core.drag_float4(f"{name}: ", value[0], value[1], value[2], value[3])
                if changed:
                    setattr(self, name, Vector4(new_value))