from typing import List
import glfw

class KeyListener:
    _instance: "KeyListener" = None

    def __init__(self):
        self._key_pressed: List[bool] = [False]*350

    @staticmethod
    def get() -> "KeyListener":
        if KeyListener._instance is None:
            KeyListener._instance = KeyListener()
        return KeyListener._instance

    @staticmethod
    def key_callback(window: int, key: int, scancode: int, action: int, mods: int):
        if action == glfw.PRESS:
            KeyListener.get()._key_pressed[key] = True
        elif action == glfw.RELEASE:
            KeyListener.get()._key_pressed[key] = False

    @staticmethod
    def is_key_pressed(key_code: int) -> bool:
        assert key_code < len(KeyListener.get()._key_pressed), f"Getting a out of bounds key code: {key_code}"
        return KeyListener.get()._key_pressed[key_code]