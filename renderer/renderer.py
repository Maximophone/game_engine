from typing import List
from components.sprite_renderer import SpriteRenderer

from renderer.render_batch import RenderBatch
from mxeng.game_object import GameObject
from renderer.shader import Shader
from renderer.texture import Texture


class Renderer:
    max_batch_size: int = 1000
    batches: List[RenderBatch] = []
    current_shader: Shader = None

    @staticmethod
    def add(go: GameObject):
        sprite: SpriteRenderer = go.get_component(SpriteRenderer)
        if sprite is not None:
            Renderer.add_sprite(sprite)

    @staticmethod
    def add_sprite(sprite: SpriteRenderer):
        added = False
        for batch in Renderer.batches:
            if batch.has_room and batch.z_index == sprite.game_object.transform.z_index:
                tex: Texture = sprite.get_texture()
                if tex is None or batch.has_texture(tex) or batch.has_texture_room:
                    batch.add_sprite(sprite)
                    added = True
                    break
        if not added:
            new_batch = RenderBatch(Renderer.max_batch_size, sprite.game_object.transform.z_index)
            new_batch.start()
            Renderer.batches.append(new_batch)
            new_batch.add_sprite(sprite)
            Renderer.batches = sorted(Renderer.batches, key=lambda x: x.z_index)

    @staticmethod
    def bind_shader(shader: Shader):
        Renderer.current_shader = shader

    @staticmethod
    def get_bound_shader() -> Shader:
        return Renderer.current_shader

    @staticmethod
    def render():
        for batch in Renderer.batches:
            batch.render()

