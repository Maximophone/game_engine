from abc import abstractmethod


class Component:
    def __init__(self):
        self.game_object: "GameObject" = None


    @abstractmethod
    def update(self, dt: float):
        pass

    def start(self):
        pass