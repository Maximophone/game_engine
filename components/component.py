from abc import abstractmethod
from enum import Enum
import imgui.core
from pyrr import Vector3, Vector4
import numpy as np
from editor.mx_imgui import MXImGUI

from util.serialization import serializable, sproperty
from util.vectors import Color3, Color4, Vector2

@serializable()
class Component:
    ID_COUNTER: int = 0

    def __init__(self):
        from mxeng.game_object import GameObject
        self._uid: int = -1
        self.game_object: GameObject = None

    def editor_update(self, dt: float):
        pass

    def update(self, dt: float):
        pass

    def start(self):
        pass

    def destroy(self):
        pass

    def imgui(self):
        serial = getattr(self, "__serial")
        for name, value in self.__dict__.items():    
            if name not in serial:
                continue
            typ = type(value)

            if typ == int:
                new_value = MXImGUI.drag_int(f"{name}: ", value)
                setattr(self, name, new_value)
                # changed, new_value = imgui.core.drag_int(f"{name}: ", value)
                # if changed:
                #     setattr(self, name, new_value)
            elif typ == float:
                new_value = MXImGUI.drag_float(f"{name}: ", value)
                setattr(self, name, new_value)
                # changed, new_value = imgui.core.drag_float(f"{name}: ", value)
                # if changed:
                #     setattr(self, name, new_value)
            elif typ == bool:
                changed, new_value = imgui.core.checkbox(f"{name}: ", value)
                if changed:
                    setattr(self, name, new_value)
            elif typ == Vector2:
                MXImGUI.draw_vec2_control(f"{name}: ", value)
                # changed, new_value = imgui.core.drag_float2(f"{name}: ", value[0], value[1])
                # if changed:
                #    setattr(self, name,  Vector2(new_value))
            elif typ == Vector3:
                changed, new_value = imgui.core.drag_float3(f"{name}: ", value[0], value[1], value[2])
                if changed:
                    setattr(self, name, Vector3(new_value))
            elif typ == Vector4:
                changed, new_value = imgui.core.drag_float4(f"{name}: ", value[0], value[1], value[2], value[3])
                if changed:
                    setattr(self, name, Vector4(new_value))
            elif typ == Color3:
                changed, new_color = imgui.color_edit3(f"{name}", *value)
                if changed:
                    setattr(self, name, Color3(new_color))
            elif typ == Color4:
                changed, new_color = imgui.color_edit4(f"{name}", *value)
                if changed:
                    setattr(self, name, Color4(new_color))
            elif isinstance(value, Enum):
                enum_values = list(typ)
                current = enum_values.index(value)
                enum_string = [x.name for x in enum_values]
                clicked, current = imgui.combo(f"{name}", current, enum_string)
                if clicked:
                    setattr(self, name, enum_values[current])


    def generate_id(self):
        if self._uid == -1:
            self._uid = Component.ID_COUNTER
            Component.ID_COUNTER += 1

    @sproperty
    def uid(self):
        return self._uid

    @staticmethod
    def init(max_id: int):
        Component.ID_COUNTER = max_id
