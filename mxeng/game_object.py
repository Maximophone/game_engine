from components.component import Component
from mxeng.transform import Transform
from typing import List, Optional

from util.serialization import serializable, sproperty
import imgui

@serializable("_name", "transform")
class GameObject:
    ID_COUNTER: int = 0

    def __init__(self, name: str = None, transform: Transform = None, z_index: int = 0):
        self._name: str = name
        self._components: List[Component] = []
        self.transform = transform or Transform()
        self._z_index: int = z_index

        self._uid: int = GameObject.ID_COUNTER
        GameObject.ID_COUNTER += 1

        
    @sproperty
    def z_index(self):
        return self._z_index

    @sproperty
    def components(self) -> List[Component]:
        return self._components

    @components.setter
    def components(self, value: List[Component]):
        for c in value:
            self.add_component(c)

    @sproperty
    def uid(self):
        return self._uid

    @staticmethod
    def init(max_id: int):
        GameObject.ID_COUNTER = max_id

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
        component.generate_id()
        self._components.append(component)
        component.game_object = self

    def update(self, dt):
        for c in self._components:
            c.update(dt)

    def start(self):
        for c in self._components:
            c.start()

    def imgui(self):
        imgui.core.text(self._name)
        for c in self._components:
            imgui.core.begin_group()
            imgui.core.text(str(c.__class__))
            c.imgui()
            imgui.core.end_group()