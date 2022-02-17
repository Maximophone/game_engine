from typing import List
from components.sprite_renderer import SpriteRenderer

from mxeng.game_object import GameObject
from physics2d.components.box_2d_collider import Box2DCollider
from physics2d.components.circle_collider import CircleCollider
from physics2d.components.pillbox_collider import PillboxCollider
from physics2d.components.rigid_body_2d import RigidBody2D

from renderer.picking_texture import PickingTexture

from util.vectors import Color4
import imgui

HIGHLIGHT_COLOR = (0.5, 0.5, 0.8, 0.8)

class PropertiesWindow:
    def __init__(self, picking_texture: PickingTexture):
        self.custom_components: List[type] = []
        self._active_game_object: GameObject = None
        self._active_game_objects_original_color: List[Color4] = []
        self._active_game_objects: List[GameObject] = []
        self.picking_texture: PickingTexture = picking_texture

    @property
    def active_game_object(self) -> GameObject:
        return self._active_game_objects[0] if len(self._active_game_objects) == 1 else None

    @active_game_object.setter
    def active_game_object(self, value: GameObject):
        if value is not None:
            self.clear_selected()
            self._active_game_objects.append(value)
        self._active_game_object = value

    def get_active_game_objects(self) -> List[GameObject]:
        return self._active_game_objects

    def add_active_game_object(self, go: GameObject):
        spr: SpriteRenderer = go.get_component(SpriteRenderer)
        self._active_game_objects.append(go)
        if spr is not None:
            self._active_game_objects_original_color.append(spr.get_color().copy())
            spr.set_color(Color4(HIGHLIGHT_COLOR))
        else:
            self._active_game_objects_original_color.append(Color4())

    def clear_selected(self):
        for color, go in zip(self._active_game_objects_original_color, self._active_game_objects):
            spr: SpriteRenderer = go.get_component(SpriteRenderer)
            if spr is not None:
                spr.set_color(color)
        self._active_game_objects_original_color = []
        self._active_game_objects = []

    def imgui(self):
        if len(self._active_game_objects) == 1 and self._active_game_objects[0] is not None:
            self._active_game_object = self._active_game_objects[0]
            imgui.begin("Properties", True)

            if imgui.begin_popup_context_window("ComponentAdder"):
                if imgui.menu_item("Add Rigid Body")[0]:
                    if self.active_game_object.get_component(RigidBody2D) is None:
                        self.active_game_object.add_component(RigidBody2D())
                if imgui.menu_item("Add Box Collider")[0]:
                    if self.active_game_object.get_component(Box2DCollider) is None:
                        self.active_game_object.add_component(Box2DCollider())
                if imgui.menu_item("Add Circle Collider")[0]:
                    if self.active_game_object.get_component(CircleCollider) is None:
                        self.active_game_object.add_component(CircleCollider())
                if imgui.menu_item("Add Pillbox Collider")[0]:
                    if self.active_game_object.get_component(PillboxCollider) is None:
                        self.active_game_object.add_component(PillboxCollider())
                for component_class in self.custom_components:
                    if imgui.menu_item(f"Add {component_class.__name__}")[0]:
                        if self.active_game_object.get_component(component_class) is None:
                            self.active_game_object.add_component(component_class())
                imgui.end_popup()
            
            self._active_game_object.imgui()
            imgui.end()


