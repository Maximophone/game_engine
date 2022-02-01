from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from scenes.scene import Scene

class SceneInitializer:
    def init(self, scene: Scene):
        pass

    def load_resources(self, scene: Scene):
        pass

    def imgui(self):
        pass