import math

from mxeng.game_object import GameObject
from physics2d.components.box_2d_collider import Box2DCollider
from physics2d.components.circle_collider import CircleCollider
from physics2d.components.pillbox_collider import PillboxCollider
from physics2d.enums.body_type import BodyType
from physics2d.mxeng_contact_listener import MxEngContactListener
from physics2d.raycast_info import RaycastInfo
from util.vectors import Vector2
from Box2D import b2World, b2BodyDef, b2_kinematicBody, b2_staticBody, b2_dynamicBody, b2PolygonShape, b2CircleShape, b2Body, b2FixtureDef
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

        self.world.contactListener = MxEngContactListener()

    def add(self, go: GameObject):
        rb: RigidBody2D = go.get_component(RigidBody2D)
        if rb is not None and rb.raw_body is None:
            # if the object has a rb component that doesn't have a raw body, which
            # means it has not been added to the physics yet
            
            body_def: b2BodyDef = b2BodyDef()
            body_def.angle = math.radians(go.transform.rotation)
            body_def.position = go.transform.position.to_b2vec2()
            body_def.angularDamping = rb.angular_damping
            body_def.linearDamping = rb.linear_damping
            body_def.fixedRotation = rb.fixed_rotation
            body_def.bullet = rb.is_continuous_collision
            body_def.gravityScale = rb.gravity_scale
            body_def.angularVelocity = rb.angular_velocity
            body_def.userData = rb.game_object

            if rb.body_type == BodyType.Kinematic:
                body_def.type = b2_kinematicBody
            elif rb.body_type == BodyType.Static:
                body_def.type = b2_staticBody
            elif rb.body_type == BodyType.Dynamic:
                body_def.type = b2_dynamicBody
            
            body: b2Body = self.world.CreateBody(body_def)
            body.mass = rb.mass
            rb.raw_body = body

            circle_collider: CircleCollider = go.get_component(CircleCollider)
            box_2d_collider: Box2DCollider = go.get_component(Box2DCollider)

            if circle_collider is not None:
                self.add_circle_collider(rb, circle_collider)
            if box_2d_collider is not None:
                self.add_box2d_collider(rb, box_2d_collider)

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

    def set_is_sensor(self, rb: RigidBody2D):
        body = rb.raw_body
        if body is None:
            return
        for fixture in body.fixtures:
            fixture.sensor = True

    def set_not_sensor(self, rb: RigidBody2D):
        body = rb.raw_body
        if body is None:
            return
        for fixture in body.fixtures:
            fixture.sensor = False

    def add_box2d_collider(self, rb: RigidBody2D, box_2d_collider: Box2DCollider):
        body = rb.raw_body
        assert body is not None, "Raw body must not be None"

        shape = b2PolygonShape()
        half_size = box_2d_collider.half_size * 0.5
        offset = box_2d_collider.offset
        origin = box_2d_collider.origin
        shape.SetAsBox(half_size.x, half_size.y, offset.to_b2vec2(), 0)

        fixture_def = b2FixtureDef(
            shape = shape,
            density = 1.,
            friction = rb.friction,
            userData = box_2d_collider.game_object,
            isSensor = rb.is_sensor
        )

        body.CreateFixture(fixture_def)

    def reset_box2d_collider(self, rb: RigidBody2D, box_2d_collider: Box2DCollider):
        body = rb.raw_body
        if body is None:
            return

        for fixture in body.fixtures:
            # TODO: is it a problem that we are destroying while iterating?
            body.DestroyFixture(fixture)

        self.add_circle_collider(rb, box_2d_collider)
        body.ResetMassData()

    def add_circle_collider(self, rb: RigidBody2D, circle_collider: CircleCollider):
        body = rb.raw_body
        assert body is not None, "Raw body must not be None"

        shape = b2CircleShape(pos=circle_collider.offset.to_b2vec2(), radius=circle_collider.radius)
    
        fixture_def = b2FixtureDef(
            shape = shape,
            density = 1.,
            friction = rb.friction,
            userData = circle_collider.game_object,
            isSensor = rb.is_sensor
        )

        body.CreateFixture(fixture_def)

    def reset_circle_collider(self, rb: RigidBody2D, circle_collider: CircleCollider):
        body = rb.raw_body
        if body is None:
            return

        for fixture in body.fixtures:
            # TODO: is it a problem that we are destroying while iterating?
            body.DestroyFixture(fixture)

        self.add_circle_collider(rb, circle_collider)
        body.ResetMassData()

    def add_pillbox_collider(self, rb: RigidBody2D, pillbox_collider: PillboxCollider):
        body = rb.raw_body
        assert body is not None, "Raw body must not be None"

        self.add_box2d_collider(rb, pillbox_collider.box)
        self.add_circle_collider(rb, pillbox_collider.top_circle)
        self.add_circle_collider(rb, pillbox_collider.bottom_circle)

    def reset_pillbox_collider(self, rb: RigidBody2D, pillbox_collider: PillboxCollider):
        body = rb.raw_body
        if body is None:
            return

        for fixture in body.fixtures:
            # TODO: is it a problem that we are destroying while iterating?
            body.DestroyFixture(fixture)

        self.add_pillbox_collider(rb, pillbox_collider)
        body.ResetMassData()

    def raycast(self, requesting_object: GameObject, point1: Vector2, point2: Vector2) -> RaycastInfo:
        callback = RaycastInfo(requesting_object)
        self.world.RayCast(callback, point1.to_b2vec2(), point2.to_b2vec2())
        return callback

    def is_locked(self) -> bool:
        return self.world.locked