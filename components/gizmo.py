from components.component import Component
from components.non_pickable import NonPickable
from components.sprite import Sprite
from components.sprite_renderer import SpriteRenderer
from editor.properties_window import PropertiesWindow
from mxeng.mouse_listener import MouseListener
from util.serialization import serializable
from util.vectors import Color4, Vector2
from mxeng.game_object import GameObject
from mario.prefabs import Prefabs
from mxeng.key_listener import KeyListener

import glfw

@serializable("x_axis_offset", "y_axis_offset", "_using", "x_axis_active", "y_axis_active")
class Gizmo(Component):
    def __init__(self, arrow_sprite: Sprite, properties_window: PropertiesWindow):
        from mxeng.window import Window
        self.x_axis_color: Color4 = Color4([1, 0.3, 0.3, 1])
        self.x_axis_color_hover: Color4 = Color4([1, 0, 0, 1])
        self.y_axis_color: Color4 = Color4([0.3, 1, 0.3, 1])
        self.y_axis_color_hover: Color4 = Color4([0, 1, 0, 1])
        self.x_axis_offset: Vector2 = Vector2([24/80, -6/80])
        self.y_axis_offset: Vector2 = Vector2([-7/80, 21/80])

        self.gizmo_width: float = 16 / 80
        self.gizmo_height: float = 48 / 80

        self.x_axis_active: bool = False
        self.y_axis_active: bool = False

        self._using: bool = False

        self.properties_window: PropertiesWindow = properties_window

        self.x_axis_object: GameObject = Prefabs.generate_sprite_object(arrow_sprite, self.gizmo_width, self.gizmo_height)
        self.y_axis_object: GameObject = Prefabs.generate_sprite_object(arrow_sprite, self.gizmo_width, self.gizmo_height)
        self.x_axis_object.add_component(NonPickable())
        self.y_axis_object.add_component(NonPickable())
        self.x_axis_sprite: SpriteRenderer = self.x_axis_object.get_component(SpriteRenderer)
        self.y_axis_sprite: SpriteRenderer = self.y_axis_object.get_component(SpriteRenderer)

        self.active_game_object: GameObject = None

        Window.get_scene().add_game_object_to_scene(self.x_axis_object)
        Window.get_scene().add_game_object_to_scene(self.y_axis_object)
        super().__init__()
        
    def start(self):
        self.x_axis_object.transform.rotation = 90
        self.y_axis_object.transform.rotation = 180
        self.x_axis_object.transform.z_index = 100
        self.y_axis_object.transform.z_index = 100
        self.x_axis_object.set_no_serialize()
        self.y_axis_object.set_no_serialize()

    def editor_update(self, dt: float):
        from mxeng.window import Window
        if not self._using:
            return

        self.active_game_object = self.properties_window.active_game_object
        if self.active_game_object is not None:
            self.set_active()
        else:
            self.set_inactive()
            return

        x_axis_hot = self.check_x_hover_state()
        y_axis_hot = self.check_y_hover_state()
        
        if (x_axis_hot or self.x_axis_active) and MouseListener.is_dragging() and MouseListener.mouse_button_down(glfw.MOUSE_BUTTON_LEFT):
            self.x_axis_active = True
            self.y_axis_active = False
        elif (y_axis_hot or self.y_axis_active) and MouseListener.is_dragging() and MouseListener.mouse_button_down(glfw.MOUSE_BUTTON_LEFT):
            self.y_axis_active = True
            self.x_axis_active = False
        else:
            self.x_axis_active = False
            self.y_axis_active = False

        self.x_axis_object.transform.position = self.active_game_object.transform.position.copy() + self.x_axis_offset
        self.y_axis_object.transform.position = self.active_game_object.transform.position.copy() + self.y_axis_offset

    def update(self, dt: float):
        if self._using:
            self.set_inactive()
        self.x_axis_object.get_component(SpriteRenderer).set_color(Color4([0., 0., 0., 0.]))
        self.y_axis_object.get_component(SpriteRenderer).set_color(Color4([0., 0., 0., 0.]))

    def set_active(self):
        self.x_axis_sprite.set_color(self.x_axis_color)
        self.y_axis_sprite.set_color(self.y_axis_color)

    def set_inactive(self):
        self.x_axis_sprite.set_color(Color4([0, 0, 0, 0]))
        self.y_axis_sprite.set_color(Color4([0, 0, 0, 0]))
        
    def check_x_hover_state(self) -> bool:
        mouse_pos = MouseListener.get_world()
        if ( 
            mouse_pos.x <= self.x_axis_object.transform.position.x + self.gizmo_height/2. and 
            mouse_pos.x >= self.x_axis_object.transform.position.x - self.gizmo_width/2. and
            mouse_pos.y >= self.x_axis_object.transform.position.y - self.gizmo_height/2. and
            mouse_pos.y <= self.x_axis_object.transform.position.y + self.gizmo_width/2.
            ):
            self.x_axis_sprite.set_color(self.x_axis_color_hover)
            return True
        else:
            self.x_axis_sprite.set_color(self.x_axis_color)
            return False

    def check_y_hover_state(self) -> bool:
        mouse_pos = MouseListener.get_world()
        if ( 
            mouse_pos.x <= self.y_axis_object.transform.position.x + self.gizmo_width/2. and 
            mouse_pos.x >= self.y_axis_object.transform.position.x - self.gizmo_width/2. and
            mouse_pos.y <= self.y_axis_object.transform.position.y + self.gizmo_height/2. and
            mouse_pos.y >= self.y_axis_object.transform.position.y - self.gizmo_height/2.
            ):
            self.y_axis_sprite.set_color(self.y_axis_color_hover)
            return True
        else:
            self.y_axis_sprite.set_color(self.y_axis_color)
            return False
    
    def set_using(self):
        self._using = True

    def set_not_using(self):
        self._using = False
        self.set_inactive()