from mxeng.component import Component
from mxeng.transform import Transform
from typing import List, Optional

from util.serialization import serializable, sproperty

@serializable("_name", "_components", "transform")
class GameObject:
    def __init__(self, name: str, transform: Transform = None, z_index: int = 0):
        self._name: str = name
        self._components: List[Component] = []
        self.transform = transform or Transform()
        self._z_index: int = z_index
        
    @sproperty
    def z_index(self):
        return self._z_index

    def get_component(self, component_class: type) -> Optional[Component]:
        for c in self._components:
            if isinstance(c, component_class):
                return c
        return None

    def remove_component(self, component_class: type):
        for i in range(len(self._components)):
            c = self._components[i]
            if isinstance(c, component_class):
                self._components.pop(i)
                return

    def add_component(self, component: Component):
        self._components.append(component)
        component.game_object = self

    def update(self, dt):
        for c in self._components:
            c.update(dt)

    def start(self):
        for c in self._components:
            c.start()

    def imgui(self):
        for c in self._components:
            c.imgui()