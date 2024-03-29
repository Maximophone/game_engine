from typing import List
import numpy as np

from renderer.texture import Texture
from components.sprite import Sprite

class Spritesheet:
    def __init__(self, texture: Texture = None, sprite_width: int = None, sprite_height: int = None, num_sprites: int = None, spacing: int = None):
        self._texture: Texture = texture
        self.sprites: List[Sprite] = []

        current_x = 0
        current_y = texture.height - sprite_height # bottom left corner of top left sprite
        for i in range(num_sprites):
            top_y = (current_y + sprite_height) / texture.height
            right_x = (current_x + sprite_width) / texture.width
            left_x = current_x / texture.width
            bottom_y = current_y / texture.height

            tex_coords = [
                np.array([right_x, top_y]),
                np.array([right_x, bottom_y]),
                np.array([left_x, bottom_y]),
                np.array([left_x, top_y]),
            ]
            sprite = Sprite(self._texture, tex_coords)
            sprite.width = sprite_width
            sprite.height = sprite_height
            self.sprites.append(sprite)
    
            current_x += sprite_width + spacing
            if current_x >= texture.width:
                current_x = 0
                current_y -= sprite_height + spacing

    def get_sprite(self, index: int) -> Sprite:
        return self.sprites[index]

    def size(self) -> int:
        return len(self.sprites)