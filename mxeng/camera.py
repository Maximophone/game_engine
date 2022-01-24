from pyrr import matrix44, Vector3

class Camera:
    def __init__(self, position: Vector3 = None):
        self._projection_matrix = matrix44.create_identity()
        self._view_matrix = matrix44.create_identity()
        self._position = position
        self.adjust_projection()

    def adjust_projection(self):
        self._projection_matrix = matrix44.create_orthogonal_projection_matrix(0., 32.*40, 0., 32.*21, 0., 100.)

    def get_view_matrix(self) -> matrix44:
        camera_front = Vector3([0., 0., -1.])
        camera_up = Vector3([0., 1., 0.])
        self._view_matrix = matrix44.create_look_at(
            Vector3([self._position[0], self._position[1], 20.]),
            camera_front + Vector3([self._position[0], self._position[1], 0.]),
            camera_up
        )
        return self._view_matrix

    def get_projection_matrix(self) -> matrix44:
        return self._projection_matrix