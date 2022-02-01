from components.non_pickable import NonPickable
from mxeng.game_object import GameObject
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

    def update(self, dt: float, current_scene: Scene):
        self.debounce -= dt
        if MouseListener.mouse_button_down(glfw.MOUSE_BUTTON_LEFT) and self.debounce < 0:
            x = MouseListener.get_screen_x()
            y = MouseListener.get_screen_y()
            if x<0 or x>2560 or y<0 or y>1440:
                return
            game_object_id = self.picking_texture.read_pixel(x, y)
            print(game_object_id)
            picked_object = current_scene.get_game_object(game_object_id)
            print(picked_object)
            if picked_object is not None and picked_object.get_component(NonPickable) is None:
                self._active_game_object = picked_object
            elif picked_object is None:
                self._active_game_object = None
            self.debounce = 0.2

    def imgui(self):
        if self._active_game_object is not None:
            imgui.begin("Properties", True)
            self._active_game_object.imgui()
            imgui.end()


