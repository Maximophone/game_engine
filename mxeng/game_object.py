from components.component import Component
from components.sprite_renderer import SpriteRenderer
from components.transform import Transform
from typing import List, Optional
from util.asset_pool import AssetPool

from util.serialization import deserialize, serializable, serialize, sproperty
import imgui

@serializable("name", "_is_dead")
class GameObject:
    ID_COUNTER: int = 0

    def __init__(self, name: str = None):
        self.name: str = name
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

    def copy(self) -> "GameObject":
        # TODO Come up with a better solution
        new_obj: GameObject = deserialize(serialize(self))
        new_obj.generate_uid()
        for c in new_obj.components:
            c.generate_id()

        spr: SpriteRenderer = new_obj.get_component(SpriteRenderer)
        if spr is not None and spr.get_texture() is not None:
            spr.set_texture(AssetPool.get_texture(spr.get_texture().filepath))
        return new_obj

    def generate_uid(self):
        self._uid = GameObject.ID_COUNTER
        GameObject.ID_COUNTER += 1

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
        imgui.core.text(self.name)
        for c in self._components:
            expanded, visible = imgui.collapsing_header(c.__class__.__name__)
            if expanded:
                c.imgui()

    def set_no_serialize(self):
        self._do_serialize = False