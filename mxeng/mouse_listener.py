from typing import List
import glfw
from pyrr import Vector4


class MouseListener:
    _instance: "MouseListener" = None

    def __init__(self, _scroll_x: float = 0., _scroll_y: float = 0., _x_pos: float = 0., _y_pos: float = 0., _last_y: float = 0., _last_x: float = 0., _mouse_button_pressed: List[bool] = None, _is_dragging: bool = False):
        self._scroll_x = _scroll_x
        self._scroll_y = _scroll_y
        self._x_pos = _x_pos
        self._y_pos = _y_pos
        self._last_y = _last_y
        self._last_x = _last_x
        self._mouse_button_pressed = _mouse_button_pressed or [False]*3
        self._is_dragging = _is_dragging


    @staticmethod
    def get() -> "MouseListener":
        if MouseListener._instance is None:
            MouseListener._instance = MouseListener()

        return MouseListener._instance

    @staticmethod
    def mouse_pos_callback(window: int, xpos: float, ypos: float):
        MouseListener.get()._last_x = MouseListener.get()._x_pos
        MouseListener.get()._last_y = MouseListener.get()._y_pos
        MouseListener.get()._x_pos = xpos
        MouseListener.get()._y_pos = ypos
        MouseListener.get()._is_dragging = MouseListener.get()._mouse_button_pressed[0] | MouseListener.get()._mouse_button_pressed[1] | MouseListener.get()._mouse_button_pressed[2]

    @staticmethod
    def mouse_button_callback(window: int, button: int, action: int, mods: int):
        if action == glfw.PRESS:
            if button < len(MouseListener.get()._mouse_button_pressed):
                MouseListener.get()._mouse_button_pressed[button] = True
            else:
                print(f"Mouse press on unknown button: {button}")
        elif action == glfw.RELEASE:
            if button < len(MouseListener.get()._mouse_button_pressed):
                MouseListener.get()._mouse_button_pressed[button] = False
                MouseListener.get()._is_dragging = False
            else:
                print(f"Mouse release on unknown button: {button}")

    @staticmethod
    def mouse_scroll_callback(window: int, x_offset: float, y_offset: float):
        MouseListener.get()._scroll_x = x_offset
        MouseListener.get()._scroll_y = y_offset

    @staticmethod
    def end_frame():
        MouseListener.get()._scroll_x = 0
        MouseListener.get()._scroll_y = 0
        MouseListener.get()._last_x = MouseListener.get()._x_pos
        MouseListener.get()._last_y = MouseListener.get()._y_pos
    
    @staticmethod
    def get_x() -> float:
        return MouseListener.get()._x_pos

    @staticmethod
    def get_y() -> float:
        return MouseListener.get()._y_pos

    @staticmethod
    def get_ortho_x() -> float:
        from mxeng.window import Window
        current_x = MouseListener.get_x()
        current_x = current_x / Window.get_width() * 2 - 1
        current_x = (Window.get_scene().camera().get_inverse_view() * Window.get_scene().camera().get_inverse_projection() * Vector4([current_x, 0, 0, 1])).x
        return current_x

    @staticmethod
    def get_ortho_y() -> float:
        from mxeng.window import Window
        current_y = MouseListener.get_y()
        current_y = current_y / Window.get_height() * 2 - 1
        current_y = (Window.get_scene().camera().get_inverse_view() * Window.get_scene().camera().get_inverse_projection() * Vector4([0, current_y, 0, 1])).y
        return current_y

    @staticmethod
    def get_dx() -> float:
        return MouseListener.get()._last_x - MouseListener.get()._x_pos

    @staticmethod
    def get_dy() -> float:
        return MouseListener.get()._last_y - MouseListener.get()._y_pos

    @staticmethod
    def get_scroll_x() -> float:
        return MouseListener.get()._scroll_x

    @staticmethod
    def get_scroll_y() -> float:
        return MouseListener.get()._scroll_y

    @staticmethod
    def is_dragging() -> bool:
        return MouseListener.get()._is_dragging

    @staticmethod
    def mouse_button_down(button: int) -> bool:
        if button < len(MouseListener.get().mouse_button_pressed):
            return MouseListener.get().mouse_button_pressed[button]
        else:
            print(f"Querying mouse button down on out of bounds button: {button}")
            return False


    


