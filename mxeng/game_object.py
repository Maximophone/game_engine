from components.component import Component
from components.transform import Transform
from typing import List, Optional

from util.serialization import serializable, sproperty
import imgui

@serializable("_name", "_is_dead")
class GameObject:
    ID_COUNTER: int = 0

    def __init__(self, name: str = None):
        self._name: str = name
        self._components: List[Component] = []
        self._do_serialize: bool = True
        self._is_dead: bool = False

        self._uid: int = GameObject.ID_COUNTER
        GameObject.ID_COUNTER += 1

    @property
    def transform(self) -> Transform:
        return self.get_component(Transform)
    
    @property
    def is_dead(self) -> bool:
        return self._is_dead

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

    @property
    def do_serialize(self):
        return self._do_serialize

    def destroy(self):
        self._is_dead = True
        for component in self._components:
            component.destroy()

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

    def editor_update(self, dt: float):
        for c in self._components:
            c.editor_update(dt)

    def update(self, dt: float):
        for c in self._components:
            c.update(dt)

    def start(self):
        for c in self._components:
            c.start()

    def imgui(self):
        imgui.core.text(self._name)
        for c in self._components:
            expanded, visible = imgui.collapsing_header(c.__class__.__name__)
            if expanded:
                c.imgui()

    def set_no_serialize(self):
        self._do_serialize = False