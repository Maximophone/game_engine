
from typing import List
from components.component import Component
from components.state_machine import StateMachine
from mxeng.game_object import GameObject
from mxeng.key_listener import KeyListener
from util.settings import Settings
from util.vectors import Vector2

import glfw

class KeyControls(Component):
    def __init__(self):
        self.debounce_time: float = 0.2
        self.debounce: float = 0.
        super().__init__()

    def editor_update(self, dt: float):
        from mxeng.window import Window
        self.debounce -= dt
        properties_window = Window.get_imgui_layer().properties_window
        active_game_object = properties_window.active_game_object
        active_game_objects: List[GameObject] = properties_window.get_active_game_objects()

        multiplier = 0.1 if KeyListener.is_key_pressed(glfw.KEY_LEFT_SHIFT) else 1.

        if KeyListener.is_key_pressed(glfw.KEY_LEFT_CONTROL) and KeyListener.key_begin_press(glfw.KEY_D) and active_game_object is not None:
            new_object = active_game_object.copy()
            Window.get_scene().add_game_object_to_scene(new_object)

            new_object.transform.position += Vector2([Settings.GRID_WIDTH, 0.])
            properties_window.active_game_object = new_object
            if new_object.get_component(StateMachine) is not None:
                new_object.get_component(StateMachine).refresh_textures()
        elif KeyListener.is_key_pressed(glfw.KEY_LEFT_CONTROL) and KeyListener.key_begin_press(glfw.KEY_D) and len(active_game_objects) > 1:
            game_objects = [x for x in active_game_objects]
            properties_window.clear_selected()
            for go in game_objects:
                copy = go.copy()
                Window.get_scene().add_game_object_to_scene(copy)
                properties_window.add_active_game_object(copy)
                if copy.get_component(StateMachine) is not None:
                    copy.get_component(StateMachine).refresh_textures()
        elif KeyListener.key_begin_press(glfw.KEY_DELETE):
            for go in active_game_objects:
                go.destroy()
            properties_window.clear_selected()
        elif KeyListener.is_key_pressed(glfw.KEY_PAGE_DOWN) and self.debounce < 0:
            self.debounce = self.debounce_time
            for go in active_game_objects:
                go.transform.z_index -= 1
        elif KeyListener.is_key_pressed(glfw.KEY_PAGE_UP) and self.debounce < 0:
            self.debounce = self.debounce_time
            for go in active_game_objects:
                go.transform.z_index += 1
        elif KeyListener.is_key_pressed(glfw.KEY_UP) and self.debounce < 0:
            self.debounce = self.debounce_time
            for go in active_game_objects:
                go.transform.position.y += Settings.GRID_HEIGHT * multiplier
        elif KeyListener.is_key_pressed(glfw.KEY_DOWN) and self.debounce < 0:
            self.debounce = self.debounce_time
            for go in active_game_objects:
                go.transform.position.y -= Settings.GRID_HEIGHT * multiplier
        elif KeyListener.is_key_pressed(glfw.KEY_LEFT) and self.debounce < 0:
            self.debounce = self.debounce_time
            for go in active_game_objects:
                go.transform.position.x -= Settings.GRID_WIDTH * multiplier
        elif KeyListener.is_key_pressed(glfw.KEY_RIGHT) and self.debounce < 0:
            self.debounce = self.debounce_time
            for go in active_game_objects:
                go.transform.position.x += Settings.GRID_WIDTH * multiplier
        
        
        
        

