from components.component import Component
from mxeng.game_object import GameObject
from mxeng.mouse_listener import MouseListener

import glfw


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

    def update(self, dt: float):
        if self.holding_object is not None:
            self.holding_object.transform.position[0] = MouseListener.get_ortho_x() - 16
            self.holding_object.transform.position[1] = MouseListener.get_ortho_y() - 16

            if MouseListener.mouse_button_down(glfw.MOUSE_BUTTON_LEFT):
                self.place()