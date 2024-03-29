from pyrr import Vector3, Matrix44
import numpy as np

from util.vectors import Color4, Vector2

class Camera:
    def __init__(self, position: Vector3 = None):
        self._projection_matrix: Matrix44 = Matrix44.identity()
        self._view_matrix: Matrix44 = Matrix44.identity()
        self._inverse_projection: Matrix44 = Matrix44.identity()
        self._inverse_view: Matrix44 = Matrix44.identity()
        self.position = position
        self.zoom = 1.
        self._projection_width: float = 6.
        self._projection_height: float = 3.
        self.clear_color: Color4 = Color4([1., 1., 1., 1.])
        self._projection_size: Vector2 = Vector2([self._projection_width, self._projection_height])
        self.adjust_projection()

    @property
    def projection_size(self) -> Vector2:
        return self._projection_size

    def adjust_projection(self):
        self._projection_matrix = Matrix44.orthogonal_projection(0., self._projection_size.x * self.zoom, 0., self._projection_size.y * self.zoom, 0., 100.)
        self._inverse_projection = self._projection_matrix.inverse

    def get_view_matrix(self) -> Matrix44:
        camera_front = Vector3([0., 0., -1.])
        camera_up = Vector3([0., 1., 0.])
        self._view_matrix = Matrix44.look_at(
            Vector3([self.position[0], self.position[1], 20.]),
            camera_front + Vector3([self.position[0], self.position[1], 0.]),
            camera_up
        )
        self._inverse_view = self._view_matrix.inverse
        return self._view_matrix

    def get_projection_matrix(self) -> Matrix44:
        return self._projection_matrix

    def get_inverse_projection(self) -> Matrix44:
        return self._inverse_projection

    def get_inverse_view(self) -> Matrix44:
        return self._inverse_view

    def add_zoom(self, value: float):
        self.zoom += value