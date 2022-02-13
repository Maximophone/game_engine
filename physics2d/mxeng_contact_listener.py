from typing import Tuple
from Box2D import b2ContactListener, b2Contact, b2ContactImpulse, b2Manifold, b2WorldManifold

from mxeng.game_object import GameObject
from util.vectors import Vector2

class MxEngContactListener(b2ContactListener):
    def __init__(self):
        super().__init__()

    def get_objects_and_normals(self, contact: b2Contact) -> Tuple[GameObject, GameObject, Vector2, Vector2]:
        object_a: GameObject = contact.fixtureA.userData
        object_b: GameObject = contact.fixtureB.userData
        world_manifold: b2WorldManifold = contact.worldManifold
        a_normal = Vector2([world_manifold.normal.x, world_manifold.normal.y])
        b_normal = -a_normal
        
        return object_a, object_b, a_normal, b_normal


    def BeginContact(self, contact: b2Contact):
        object_a, object_b, a_normal, b_normal = self.get_objects_and_normals(contact)
        for c in object_a.components:
            c.begin_collision(object_b, contact, a_normal)

        for c in object_b.components:
            c.begin_collision(object_a, contact, b_normal)


    def EndContact(self, contact: b2Contact):
        object_a, object_b, a_normal, b_normal = self.get_objects_and_normals(contact)
        for c in object_a.components:
            c.end_collision(object_b, contact, a_normal)

        for c in object_b.components:
            c.end_collision(object_a, contact, b_normal)

    def PreSolve(self, contact: b2Contact, old_manifold: b2Manifold):
        object_a, object_b, a_normal, b_normal = self.get_objects_and_normals(contact)
        for c in object_a.components:
            c.pre_solve(object_b, contact, a_normal)

        for c in object_b.components:
            c.pre_solve(object_a, contact, b_normal)

    def PostSolve(self, contact: b2Contact, impulse: b2ContactImpulse):
        object_a, object_b, a_normal, b_normal = self.get_objects_and_normals(contact)
        for c in object_a.components:
            c.post_solve(object_b, contact, a_normal)

        for c in object_b.components:
            c.post_solve(object_a, contact, b_normal)
