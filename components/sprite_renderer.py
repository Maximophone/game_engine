from mxeng.component import Component


class SpriteRenderer(Component):
    def __init__(self):
        super().__init__()
        self.first_time = True
    def start(self):
        print("I am starting")

    def update(self, dt):
        if self.first_time:
            print("I am updating")
        self.first_time = False

    