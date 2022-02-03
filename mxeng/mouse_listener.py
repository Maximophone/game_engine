from typing import List
import glfw
from util.vectors import Vector2
from pyrr import Vector4


class MouseListener:
    _instance: "MouseListener" = None

    def __init__(self, _scroll_x: float = 0., _scroll_y: float = 0., _x_pos: float = 0., _y_pos: float = 0., _last_y: float = 0., _last_x: float = 0., _mouse_button_pressed: List[bool] = None, _is_dragging: bool = False):
        self._scroll_x = _scroll_x
        self._scroll_y = _scroll_y
        self._x_pos = _x_pos
        self._y_pos = _y_pos
        self._world_x, self._world_y = 0., 0.
        self._mouse_button_pressed = _mouse_button_pressed or [False]*9
        self._is_dragging = _is_dragging
        self._mouse_button_down: int = 0
        
        self._game_viewport_pos = Vector2([0, 0])
        self._game_viewport_size = Vector2([0, 0])


    @staticmethod
    def get() -> "MouseListener":
        if MouseListener._instance is None:
            MouseListener._instance = MouseListener()

        return MouseListener._instance

    @staticmethod
    def mouse_pos_callback(window: int, xpos: float, ypos: float):
        if MouseListener.get()._mouse_button_down > 0:
            MouseListener.get()._is_dragging = True
        #MouseListener.get()._last_x = MouseListener.get()._x_pos
        #MouseListener.get()._last_y = MouseListener.get()._y_pos
        #MouseListener.get()._last_world_x = MouseListener.get()._world_x
        #MouseListener.get()._last_world_y = MouseListener.get()._world_y
        MouseListener.get()._x_pos = xpos
        MouseListener.get()._y_pos = ypos

    @staticmethod
    def mouse_button_callback(window: int, button: int, action: int, mods: int):
        if action == glfw.PRESS:
            MouseListener.get()._mouse_button_down += 1
            if button < len(MouseListener.get()._mouse_button_pressed):
                MouseListener.get()._mouse_button_pressed[button] = True
            else:
                print(f"Mouse press on unknown button: {button}")
        elif action == glfw.RELEASE:
            MouseListener.get()._mouse_button_down -= 1
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
    
    @staticmethod
    def get_x() -> float:
        return MouseListener.get()._x_pos

    @staticmethod
    def get_y() -> float:
        return MouseListener.get()._y_pos
        
    @staticmethod
    def get_screen() -> Vector2:
        current_x = MouseListener.get_x() - MouseListener.get()._game_viewport_pos.x
        current_x = current_x / MouseListener.get()._game_viewport_size.x * 2 - 1
        current_y = MouseListener.get_y() - MouseListener.get()._game_viewport_pos.y
        current_y = - (current_y / MouseListener.get()._game_viewport_size.y * 2 - 1)
        return Vector2([current_x, current_y])

    @staticmethod
    def get_screen_x() -> float:
        return MouseListener.get_screen().x

    @staticmethod
    def get_screen_y() -> float:
        return MouseListener.get_screen().y

    @staticmethod
    def get_world() -> Vector2:
        from mxeng.window import Window
        screen_pos = MouseListener.get_screen()
        camera = Window.get_scene().camera()
        world_xy = Vector2((camera.get_inverse_view() * camera.get_inverse_projection() * Vector4([screen_pos.x, screen_pos.y, 0, 1])).xy)

        return world_xy

    @staticmethod
    def get_world_x() -> float:
        return MouseListener.get_world().x

    @staticmethod
    def get_world_y() -> float:
        return MouseListener.get_world().y
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
        if button < len(MouseListener.get()._mouse_button_pressed):
            return MouseListener.get()._mouse_button_pressed[button]
        else:
            print(f"Querying mouse button down on out of bounds button: {button}")
            return False

    @staticmethod
    def set_game_viewport_pos(pos: Vector2):
        MouseListener.get()._game_viewport_pos = pos

    @staticmethod
    def set_game_viewport_size(size: Vector2):
        MouseListener.get()._game_viewport_size = size


    


