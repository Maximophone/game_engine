from numpy import sign
from components.component import Component
from mxeng.camera import Camera
from mxeng.key_listener import KeyListener
from util.vectors import Vector2
from mxeng.mouse_listener import MouseListener
from pyrr import vector3

import glfw

class EditorCamera(Component):
    def __init__(self, level_editor_camera: Camera):
        self.level_editor_camera = level_editor_camera
        self.click_origin: Vector2 = Vector2([0, 0])
        self.drag_debounce: float = 0.032 # Should be 2 frames at 60 FPS
        self.drag_sensitivity: float = 30.
        self.scroll_sensitivity: float = 0.1
        self.lerp_time: float = 0.
        self.reset: bool = False
        super().__init__()

    def update(self, dt: float):
        if MouseListener.mouse_button_down(glfw.MOUSE_BUTTON_MIDDLE) and self.drag_debounce > 0:
            # Waiting until drag debounce is negative
            self.click_origin = Vector2([MouseListener.get_ortho_x(), MouseListener.get_ortho_y()])
            self.drag_debounce -= dt
            return
        elif MouseListener.mouse_button_down(glfw.MOUSE_BUTTON_MIDDLE):
            mouse_pos = Vector2([MouseListener.get_ortho_x(), MouseListener.get_ortho_y()])
            delta = mouse_pos - self.click_origin
            self.level_editor_camera.position -= delta * dt * self.drag_sensitivity
            self.click_origin = self.click_origin*(1-dt) + mouse_pos*dt

        if not MouseListener.mouse_button_down(glfw.MOUSE_BUTTON_MIDDLE) and self.drag_debounce <= 0:
            self.drag_debounce = 0.032

        if MouseListener.get_scroll_y() != 0.:
            add_value = (abs(MouseListener.get_scroll_y())*self.scroll_sensitivity) ** (1./self.level_editor_camera.zoom)
            add_value *= -sign(MouseListener.get_scroll_y())
            self.level_editor_camera.add_zoom(add_value)

        if KeyListener.is_key_pressed(glfw.KEY_0):
            self.reset = True

        if self.reset:
            self.level_editor_camera.position = self.level_editor_camera.position * (1 - self.lerp_time) + Vector2([0., 0.]) * self.lerp_time
            self.level_editor_camera.zoom = self.level_editor_camera.zoom * (1 - self.lerp_time) + 1.* self.lerp_time
            self.lerp_time += 0.1 * dt

            if abs(self.level_editor_camera.position.x) <= 5. and abs(self.level_editor_camera.position.y) <= 5:
                self.level_editor_camera.position = Vector2([0., 0.])
                self.reset = False
                self.lerp_time = 0.

        