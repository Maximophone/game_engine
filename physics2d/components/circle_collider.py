from components.component import Component

class CircleCollider(Component):
    def __init__(self):
        self.radius: float = 1.
        super().__init__()