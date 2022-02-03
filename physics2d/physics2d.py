import math

from mxeng.game_object import GameObject
from physics2d.components.box_2d_collider import Box2DCollider
from physics2d.components.circle_collider import CircleCollider
from physics2d.enums.body_type import BodyType
from util.vectors import Vector2
from Box2D import b2World, b2BodyDef, b2Vec2, b2_kinematicBody, b2_staticBody, b2_dynamicBody, b2PolygonShape, b2Body
from physics2d.components.rigid_body_2d import RigidBody2D

from numpy import float32

class Physics2D:
    def __init__(self):
        self.gravity: Vector2 = Vector2([0., -10.])
        self.world: b2World = b2World(self.gravity.xy)
        
        self.physics_time: float = 0.
        self.physics_time_step: float = 1./60
        self.velocity_iterations: int = 8
        self.position_iterations: int = 3

    def add(self, go: GameObject):
        rb: RigidBody2D = go.get_component(RigidBody2D)
        if rb is not None and rb.raw_body is None:
            # if the object has a rb component that doesn't have a raw body, which
            # means it has not been added to the physics yet
            
            body_def: b2BodyDef = b2BodyDef()
            body_def.angle = math.radians(go.transform.rotation)
            body_def.position = b2Vec2(float(go.transform.position.x), float(go.transform.position.y))
            body_def.angularDamping = rb.angular_damping
            body_def.linearDamping = rb.linear_damping
            body_def.fixedRotation = rb.fixed_rotation
            body_def.bullet = rb.is_continuous_collision

            if rb.body_type == BodyType.Kinematic:
                body_def.type = b2_kinematicBody
            elif rb.body_type == BodyType.Static:
                body_def.type = b2_staticBody
            elif rb.body_type == BodyType.Dynamic:
                body_def.type = b2_dynamicBody
            
            shape = b2PolygonShape()
            circle_collider: CircleCollider = go.get_component(CircleCollider)
            box_2d_collider: Box2DCollider = go.get_component(Box2DCollider)

            if circle_collider is not None:
                shape.radius = circle_collider.radius
            elif box_2d_collider is not None:
                half_size = box_2d_collider.half_size * 0.5
                offset = box_2d_collider.offset
                origin = box_2d_collider.origin
                shape.SetAsBox(half_size.x, half_size.y, b2Vec2(float(origin.x), float(origin.y)), 0)

                body_def.position = body_def.position + b2Vec2(float(offset.x), float(offset.y))

            body: b2Body = self.world.CreateBody(body_def)
            rb.raw_body = body
            body.CreateFixture(shape=shape, density=rb.mass)

    def destroy_game_object(self, go: GameObject):
        rb: RigidBody2D = go.get_component(RigidBody2D)
        if rb is not None:
            if rb.raw_body is not None:
                self.world.DestroyBody(rb.raw_body)
                rb.raw_body = None

    def update(self, dt: float):
        self.physics_time += dt
        if self.physics_time >= 0:
            # trick to run at constant timesteps
            self.physics_time -= self.physics_time_step
            self.world.Step(self.physics_time_step, self.velocity_iterations, self.position_iterations)
