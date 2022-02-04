from typing import List

from components.sprite import Sprite
from components.frame import Frame
from util.asset_pool import AssetPool
from util.serialization import serializable

@serializable("title", "animation_frames", "default_sprite", "does_loop")
class AnimationState:
    def __init__(self, title: str = ""):
        self.title: str = title
        self.animation_frames: List[Frame] = []
        self.default_sprite: Sprite = Sprite()
        self.time_tracker: float = 0.
        self.current_sprite: int = 0
        self.does_loop: bool = False

    def refresh_textures(self):
        for frame in self.animation_frames:
            frame.sprite._texture = AssetPool.get_texture(frame.sprite.get_texture().filepath)

    def add_frame(self, sprite: Sprite, frame_time: float):
        self.animation_frames.append(Frame(sprite, frame_time))

    def update(self, dt: float):
        if self.current_sprite < len(self.animation_frames):
            self.time_tracker -= dt
            if self.time_tracker <= 0:
                if not (self.current_sprite == len(self.animation_frames) - 1 and not self.does_loop):
                    self.current_sprite = (self.current_sprite + 1) % len(self.animation_frames)
                self.time_tracker = self.animation_frames[self.current_sprite].frame_time

    def get_current_sprite(self) -> Sprite:
        if self.current_sprite < len(self.animation_frames):
            return self.animation_frames[self.current_sprite].sprite
        return self.default_sprite
