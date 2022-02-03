from components.gizmo import Gizmo
from components.sprite import Sprite
from editor.properties_window import PropertiesWindow
from mxeng.mouse_listener import MouseListener

class TranslateGizmo(Gizmo):
    def __init__(self, arrow_sprite: Sprite, properties_window: PropertiesWindow):
        super().__init__(arrow_sprite, properties_window)
        
    def editor_update(self, dt: float):
        if self.active_game_object is not None:
            if self.x_axis_active and not self.y_axis_active:
                self.active_game_object.transform.position.x = MouseListener.get_world_x()
            if self.y_axis_active and not self.x_axis_active:
                self.active_game_object.transform.position.y = MouseListener.get_world_y()

        super().editor_update(dt)