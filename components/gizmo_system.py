from components.component import Component
from components.spritesheet import Spritesheet
from components.translate_gizmo import TranslateGizmo
from components.scale_gizmo import ScaleGizmo
from mxeng.key_listener import KeyListener

import glfw

from util.serialization import serializable

@serializable("using_gizmo")
class GizmoSystem(Component):
    def __init__(self, gizmo_sprites: Spritesheet):
        self.gizmos: Spritesheet = gizmo_sprites
        self.using_gizmo: int = 0
        super().__init__()

    def start(self):
        from mxeng.window import Window
        self.game_object.add_component(TranslateGizmo(self.gizmos.get_sprite(1), Window.get_imgui_layer().properties_window))
        self.game_object.add_component(ScaleGizmo(self.gizmos.get_sprite(2), Window.get_imgui_layer().properties_window))

    def editor_update(self, dt: float):
        if self.using_gizmo == 0:
            self.game_object.get_component(TranslateGizmo).set_using()
            self.game_object.get_component(ScaleGizmo).set_not_using()
        elif self.using_gizmo == 1:
            self.game_object.get_component(ScaleGizmo).set_using()
            self.game_object.get_component(TranslateGizmo).set_not_using()

        if KeyListener.is_key_pressed(glfw.KEY_E):
            self.using_gizmo = 0
        elif KeyListener.is_key_pressed(glfw.KEY_R):
            self.using_gizmo = 1

