from components.sprite import Sprite
from util.serialization import serializable

@serializable("sprite", "frame_time")
class Frame:
    def __init__(self, sprite: Sprite = None, time: float = 0.):
        self.sprite: Sprite = sprite
        self.frame_time = time
