from mxeng.component import Component
from components.sprite_renderer import SpriteRenderer

class FontRenderer(Component):
    def start(self):
        if self.game_object.get_component(SpriteRenderer) is not None:
            print("Found font renderer!")
    
    def update(self, dt: float):
        pass