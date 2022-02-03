from components.component import Component
from util.serialization import serializable

@serializable()
class NonPickable(Component):
    pass