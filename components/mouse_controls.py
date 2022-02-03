from components.component import Component
from mxeng.game_object import GameObject
from mxeng.mouse_listener import MouseListener

import glfw

from util.settings import Settings


class MouseControls(Component):
    def __init__(self):
        self.holding_object: GameObject = None
        super().__init__()

    def pickup_object(self, go: GameObject):
        from mxeng.window import Window
        self.holding_object = go
        Window.get_scene().add_game_object_to_scene(go)

    def place(self):
        self.holding_object = None

    def editor_update(self, dt: float):
        if self.holding_object is not None:
            self.holding_object.transform.position.x = MouseListener.get_ortho_x()
            self.holding_object.transform.position.y = MouseListener.get_ortho_y()
            self.holding_object.transform.position.x = (self.holding_object.transform.position.x // Settings.GRID_WIDTH) * Settings.GRID_WIDTH
            self.holding_object.transform.position.y = (self.holding_object.transform.position.y // Settings.GRID_HEIGHT) * Settings.GRID_HEIGHT

            if MouseListener.mouse_button_down(glfw.MOUSE_BUTTON_LEFT):
                self.place()