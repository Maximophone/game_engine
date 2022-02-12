from typing import List
import glfw

class KeyListener:
    _instance: "KeyListener" = None

    def __init__(self):
        self._key_pressed: List[bool] = [False]*350
        self._key_begin_press: List[bool] = [False]*350

    @staticmethod
    def get() -> "KeyListener":
        if KeyListener._instance is None:
            KeyListener._instance = KeyListener()
        return KeyListener._instance

    @staticmethod
    def end_frame():
        KeyListener.get()._key_begin_press = [False]*350

    @staticmethod
    def key_callback(window: int, key: int, scancode: int, action: int, mods: int):
        if action == glfw.PRESS:
            KeyListener.get()._key_pressed[key] = True
            KeyListener.get()._key_begin_press[key] = True
        elif action == glfw.RELEASE:
            KeyListener.get()._key_pressed[key] = False
            KeyListener.get()._key_begin_press[key] = False

    @staticmethod
    def is_key_pressed(key_code: int) -> bool:
        assert key_code < len(KeyListener.get()._key_pressed), f"Getting a out of bounds key code: {key_code}"
        return KeyListener.get()._key_pressed[key_code]

    @staticmethod
    def key_begin_press(key_code: int) -> bool:
        return KeyListener.get()._key_begin_press[key_code]