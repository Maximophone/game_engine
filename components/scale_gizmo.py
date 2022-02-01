from components.gizmo import Gizmo
from components.sprite import Sprite
from editor.properties_window import PropertiesWindow
from mxeng.mouse_listener import MouseListener

class ScaleGizmo(Gizmo):
    def __init__(self, scale_sprite: Sprite, properties_window: PropertiesWindow):
        super().__init__(scale_sprite, properties_window)
        
    def update(self, dt: float):
        if self.active_game_object is not None:
            if self.x_axis_active and not self.y_axis_active:
                self.active_game_object.transform.scale.x -= MouseListener.get_world_dx()
            if self.y_axis_active and not self.x_axis_active:
                self.active_game_object.transform.scale.y -= MouseListener.get_world_dy()

        super().update(dt)