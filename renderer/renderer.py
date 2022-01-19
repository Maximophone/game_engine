from typing import List
from components.sprite_renderer import SpriteRenderer

from renderer.render_batch import RenderBatch
from mxeng.game_object import GameObject


class Renderer:
    def __init__(self):
        self.max_batch_size: int = 1000
        self.batches: List[RenderBatch] = []

    def add(self, go: GameObject):
        sprite: SpriteRenderer = go.get_component(SpriteRenderer)
        if sprite is not None:
            self.add_sprite(sprite)

    def add_sprite(self, sprite: SpriteRenderer):
        added = False
        for batch in self.batches:
            if batch.has_room:
                batch.add_sprite(sprite)
                added = True
                break
        if not added:
            new_batch = RenderBatch(self.max_batch_size)
            new_batch.start()
            self.batches.append(new_batch)
            new_batch.add_sprite(sprite)

    def render(self):
        for batch in self.batches:
            batch.render()