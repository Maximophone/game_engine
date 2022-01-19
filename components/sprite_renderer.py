from mxeng.component import Component
from pyrr import vector4


class SpriteRenderer(Component):
    def __init__(self, color: vector4):
        self._color: vector4 = color
        super().__init__()

    def start(self):
        pass

    def update(self, dt):
        pass

    def get_color(self) -> vector4:
        return self._color

    