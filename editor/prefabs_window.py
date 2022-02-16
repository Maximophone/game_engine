from dataclasses import dataclass
from typing import Callable, List

import imgui
from components.mouse_controls import MouseControls

from components.sprite import Sprite
from mxeng.game_object import GameObject

@dataclass
class Prefab:
    sprite: Sprite
    callback: Callable

@dataclass
class Tab:
    name: str
    prefabs: List[Prefab]

class PrefabsWindow:
    def __init__(self, mouse_controls: MouseControls):
        self.mouse_controls = mouse_controls
        self.tabs: List[Tab] = []

    def imgui(self):
        imgui.begin("Objects")
        for tab in self.tabs:
            if imgui.collapsing_header(tab.name, True)[0]:
                window_pos = imgui.core.get_window_position()
                window_size = imgui.core.get_window_size()
                item_spacing = imgui.core.get_style().item_spacing

                window_x2: float = window_pos.x + window_size.x

                for i, prefab in enumerate(tab.prefabs):
                    sprite_width = prefab.sprite.width * 4
                    sprite_height = prefab.sprite.height * 4
                    id = prefab.sprite.tex_id
                    tex_coords = prefab.sprite.get_tex_coords()

                    imgui.core.push_id(str(i))
                    changed = imgui.core.image_button(id, sprite_width, sprite_height, (tex_coords[2][0], tex_coords[0][1]), (tex_coords[0][0], tex_coords[2][1]))
                    if changed:
                        obj: GameObject = prefab.callback(prefab.sprite)
                        self.mouse_controls.pickup_object(obj)
                    imgui.core.pop_id()

                    last_button_pos = imgui.core.get_item_rect_max()
                    last_button_x2 = last_button_pos.x
                    next_button_x2 = last_button_x2 + item_spacing.x + sprite_width

                    if i + 1 < len(tab.prefabs) and next_button_x2 < window_x2:
                        imgui.core.same_line()
        imgui.end()
