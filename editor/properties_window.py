from components.non_pickable import NonPickable
from mxeng.game_object import GameObject
from physics2d.components.box_2d_collider import Box2DCollider
from physics2d.components.circle_collider import CircleCollider
from physics2d.components.rigid_body_2d import RigidBody2D
from scenes.scene import Scene
from renderer.picking_texture import PickingTexture
from mxeng.mouse_listener import MouseListener
import imgui
import glfw

class PropertiesWindow:
    def __init__(self, picking_texture: PickingTexture):
        self._active_game_object: GameObject = None
        self.picking_texture: PickingTexture = picking_texture
        self.debounce: float = 0.2

    @property
    def active_game_object(self) -> GameObject:
        return self._active_game_object

    @active_game_object.setter
    def active_game_object(self, value: GameObject):
        self._active_game_object = value

    def update(self, dt: float, current_scene: Scene):
        self.debounce -= dt
        if MouseListener.mouse_button_down(glfw.MOUSE_BUTTON_LEFT) and self.debounce < 0:
            x = MouseListener.get_screen_x()
            y = MouseListener.get_screen_y()
            if x<0 or x>2560 or y<0 or y>1440:
                return
            game_object_id = self.picking_texture.read_pixel(x, y)
            picked_object = current_scene.get_game_object(game_object_id)
            if picked_object is not None and picked_object.get_component(NonPickable) is None:
                self._active_game_object = picked_object
            elif picked_object is None:
                self._active_game_object = None
            self.debounce = 0.2

    def imgui(self):
        if self._active_game_object is not None:
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
                imgui.end_popup()
            
            self._active_game_object.imgui()
            imgui.end()


