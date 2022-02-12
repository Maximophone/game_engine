from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from mxeng.game_object import GameObject
from enum import Enum
import imgui.core
from pyrr import Vector3, Vector4
from editor.mx_imgui import MXImGUI
from Box2D import b2Contact

from util.serialization import serializable, sproperty
from util.vectors import Color3, Color4, Vector2

@serializable()
class Component:
    ID_COUNTER: int = 0

    def __init__(self):
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

    def begin_collision(self, colliding_object: GameObject, contact: b2Contact, hit_normal: Vector2):
        pass

    def end_collision(self, colliding_object: GameObject, contact: b2Contact, hit_normal: Vector2):
        pass

    def pre_solve(self, colliding_object: GameObject, contact: b2Contact, hit_normal: Vector2):
        pass

    def post_solve(self, colliding_object: GameObject, contact: b2Contact, hit_normal: Vector2):
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
            elif typ == float:
                new_value = MXImGUI.drag_float(f"{name}: ", value)
                setattr(self, name, new_value)
            elif typ == bool:
                changed, new_value = imgui.core.checkbox(f"{name}: ", value)
                if changed:
                    setattr(self, name, new_value)
            elif typ == str:
                new_value = MXImGUI.input_text(f"{name}: ", value)
                setattr(self, name, new_value)
            elif typ == Vector2:
                MXImGUI.draw_vec2_control(f"{name}: ", value)
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
