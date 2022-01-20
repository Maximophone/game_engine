from typing import List
from components.sprite_renderer import SpriteRenderer

from renderer.render_batch import RenderBatch
from mxeng.game_object import GameObject
from renderer.texture import Texture


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
            if batch.has_room and batch.z_index == sprite.game_object.z_index:
                tex: Texture = sprite.get_texture()
                if tex is None or batch.has_texture(tex) or batch.has_texture_room:
                    batch.add_sprite(sprite)
                    added = True
                    break
        if not added:
            new_batch = RenderBatch(self.max_batch_size, sprite.game_object.z_index)
            new_batch.start()
            self.batches.append(new_batch)
            new_batch.add_sprite(sprite)
            self.batches = sorted(self.batches, key=lambda x: x.z_index)

    def render(self):
        for batch in self.batches:
            batch.render()