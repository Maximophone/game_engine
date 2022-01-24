from pyrr import matrix44, vector3

from util.serialization import serializable

@serializable("_projection_matrix", "_view_matrix", "_position")
class Camera:
    def __init__(self, position: vector3):
        self._projection_matrix = matrix44.create_identity()
        self._view_matrix = matrix44.create_identity()
        self._position = position
        self.adjust_projection()

    def adjust_projection(self):
        self._projection_matrix = matrix44.create_orthogonal_projection_matrix(0., 32.*40, 0., 32.*21, 0., 100.)

    def get_view_matrix(self) -> matrix44:
        camera_front = vector3.create(0., 0., -1.)
        camera_up = vector3.create(0., 1., 0.)
        self._view_matrix = matrix44.create_look_at(
            vector3.create(self._position[0], self._position[1], 20.),
            camera_front + vector3.create(self._position[0], self._position[1], 0.),
            camera_up
        )
        return self._view_matrix

    def get_projection_matrix(self) -> matrix44:
        return self._projection_matrix