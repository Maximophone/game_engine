from components.component import Component
from components.non_pickable import NonPickable
from components.sprite_renderer import SpriteRenderer
from mxeng.game_object import GameObject
from mxeng.key_listener import KeyListener
from mxeng.mouse_listener import MouseListener

import glfw

from util.settings import Settings
from util.vectors import Color4


class MouseControls(Component):
    def __init__(self):
        self.holding_object: GameObject = None
        self.debounce_time = 0.05
        self.debounce = self.debounce_time
        super().__init__()

    def pickup_object(self, go: GameObject):
        from mxeng.window import Window
        if self.holding_object is not None:
            self.holding_object.destroy()
        self.holding_object = go
        self.holding_object.get_component(SpriteRenderer).set_color(Color4([0.8, 0.8, 0.8, 0.5]))
        self.holding_object.add_component(NonPickable())
        Window.get_scene().add_game_object_to_scene(go)

    def place(self):
        from mxeng.window import Window
        new_obj = self.holding_object.copy()
        new_obj.get_component(SpriteRenderer).set_color(Color4([1., 1., 1., 1.]))
        new_obj.remove_component(NonPickable)
        Window.get_scene().add_game_object_to_scene(new_obj)

    def editor_update(self, dt: float):
        self.debounce -= dt
        if self.holding_object is not None:
            self.holding_object.transform.position.x = MouseListener.get_world_x()
            self.holding_object.transform.position.y = MouseListener.get_world_y()
            self.holding_object.transform.position.x = (self.holding_object.transform.position.x // Settings.GRID_WIDTH) * Settings.GRID_WIDTH + Settings.GRID_WIDTH/2
            self.holding_object.transform.position.y = (self.holding_object.transform.position.y // Settings.GRID_HEIGHT) * Settings.GRID_HEIGHT + Settings.GRID_HEIGHT/2

            if MouseListener.mouse_button_down(glfw.MOUSE_BUTTON_LEFT):
                self.place()
                self.debounce = self.debounce_time

            if KeyListener.is_key_pressed(glfw.KEY_ESCAPE):
                self.holding_object.destroy()
                self.holding_object = None