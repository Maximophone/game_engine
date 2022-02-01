from util.vectors import Vector2
from Box2D import b2World

class Physics2D:
    def __init__(self):
        self.gravity: Vector2 = Vector2([0., -10.])
        self.world: b2World = b2World(self.gravity)
        
        self.physics_time: float = 0.
        self.physics_time_step: float = 1./60
        self.velocity_iterations: int = 8
        self.position_iterations: int = 3

    def update(self, dt: float):
        self.physics_time += dt
        if self.physics_time >= 0:
            # trick to run at constant timesteps
            self.physics_time -= self.physics_time_step
            self.world.Step(self.physics_time_step, self.velocity_iterations, self.position_iterations)