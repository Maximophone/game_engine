import ctypes
from typing import List

from pyrr import Matrix33
from renderer.line_2d import Line2D
from renderer.shader import Shader
from util.asset_pool import AssetPool
from util.vectors import Vector2, Color3
from mxeng.window import Window

import numpy as np
import OpenGL.GL as gl


class DebugDraw:
    MAX_LINES: int = 500
    lines: List[Line2D] = []
    # 6 floats per vertex, 2 vertices per line
    vertex_array: Vector2 = np.zeros(MAX_LINES*6*2, dtype=np.float32)
    shader: Shader = AssetPool.get_shader("assets/shaders/debug_line_2d.glsl")

    vao_id: int = -1
    vbo_id: int = -1

    started: bool = False

    @staticmethod
    def start():
        # Generate the VAO
        DebugDraw.vao_id = gl.glGenVertexArrays(1)
        gl.glBindVertexArray(DebugDraw.vao_id)

        # Create the vbo and buffer some memory
        DebugDraw.vbo_id = gl.glGenBuffers(1)
        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, DebugDraw.vbo_id)
        gl.glBufferData(gl.GL_ARRAY_BUFFER, DebugDraw.vertex_array.nbytes, DebugDraw.vertex_array, gl.GL_DYNAMIC_DRAW)

        # Enable the vertex array attributes
        gl.glEnableVertexAttribArray(0)
        gl.glVertexAttribPointer(0, 3, gl.GL_FLOAT, gl.GL_FALSE, 6*np.float32().itemsize, ctypes.c_void_p(0))

        gl.glEnableVertexAttribArray(1)
        gl.glVertexAttribPointer(1, 3, gl.GL_FLOAT, gl.GL_FALSE, 6*np.float32().itemsize, ctypes.c_void_p(3*np.float32().itemsize))

        gl.glLineWidth(2.0)

    @staticmethod
    def begin_frame():
        if not DebugDraw.started:
            DebugDraw.start()
            DebugDraw.started = True

        # Remove dead lines
        to_remove = []
        for i, line in enumerate(DebugDraw.lines):
            if line.begin_frame() < 0:
                to_remove.append(i)
        for i in to_remove[::-1]:
            DebugDraw.lines.pop(i)

    @staticmethod
    def draw():

        if len(DebugDraw.lines) <= 0:
            return

        index = 0
        for line in DebugDraw.lines:
            for i in range(2):
                position = line.from_ if i == 0 else line.to
                color = line.color

                # Load position
                DebugDraw.vertex_array[index] = position[0]
                DebugDraw.vertex_array[index + 1] = position[1]
                DebugDraw.vertex_array[index + 2] = -10.
                
                # Load color
                DebugDraw.vertex_array[index + 3] = color.x
                DebugDraw.vertex_array[index + 4] = color.y
                DebugDraw.vertex_array[index + 5] = color.z
                index += 6

        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, DebugDraw.vbo_id)
        gl.glBufferSubData(gl.GL_ARRAY_BUFFER, 0, DebugDraw.vertex_array.nbytes, DebugDraw.vertex_array[0:len(DebugDraw.lines)*6*2])

        # Use our shader
        DebugDraw.shader.use()
        DebugDraw.shader.upload_mat4f("uProjection", Window.get_scene().camera().get_projection_matrix())
        DebugDraw.shader.upload_mat4f("uView", Window.get_scene().camera().get_view_matrix())

        # Bind the vao
        gl.glBindVertexArray(DebugDraw.vao_id)
        gl.glEnableVertexAttribArray(0)
        gl.glEnableVertexAttribArray(1)

        # Draw the batch
        gl.glDrawArrays(gl.GL_LINES, 0, 2*len(DebugDraw.lines))
        
        # Disable location
        gl.glDisableVertexAttribArray(0)
        gl.glDisableVertexAttribArray(1)
        gl.glBindVertexArray(0)

        DebugDraw.shader.detach()

    @staticmethod
    def rotate(v: Vector2, rotation: float, center: Vector2 = None) -> Vector2:
        center = center if center is not None else Vector2([0, 0])
        return Vector2.from_vector3(Matrix33.from_z_rotation(-rotation/360.*2.*np.pi) * (v - center) + center)

    # ====================
    # Add line2D methods
    # ====================
    @staticmethod
    def add_line_2D(from_: Vector2, to: Vector2, color: Color3 = None, lifetime: int = 1):
        # TODO: add constants for common colors
        color = color if color is not None else Color3([0., 1., 0.])
        if len(DebugDraw.lines) >= DebugDraw.MAX_LINES:
            return
        DebugDraw.lines.append(Line2D(from_, to, color, lifetime))

    # ===================
    # Add Box2D methods
    # ===================
    @staticmethod
    def add_box_2D(center: Vector2, dimensions: Vector2, rotation: float = 0, color: Color3=None, lifetime: int = 1):
        color = color if color is not None else Color3([0., 1., 0.])
        min_ = center - dimensions/2.
        max_ = center + dimensions/2.

        vertices = [
            min_,
            Vector2([min_[0], max_[1]]),
            max_,
            Vector2([max_[0], min_[1]]),
        ]

        if rotation != 0:
            for vert in vertices:
                vert[:] = DebugDraw.rotate(vert, rotation, center)

        DebugDraw.add_line_2D(vertices[0], vertices[1], color, lifetime)
        DebugDraw.add_line_2D(vertices[1], vertices[2], color, lifetime)
        DebugDraw.add_line_2D(vertices[2], vertices[3], color, lifetime)
        DebugDraw.add_line_2D(vertices[3], vertices[0], color, lifetime)


    # ===================
    # Add Circle methods
    # ===================
    @staticmethod
    def add_circle(center: Vector2, radius: float, color: Color3=None, lifetime: int = 1, n_points: int = 16):
        color = color if color is not None else Color3([0., 1., 0.])
        points = []
        increment = 360 / n_points
        current_angle = 0
        for i in range(n_points):
            tmp = DebugDraw.rotate(Vector2([radius, 0]), current_angle)
            points.append((tmp + center)[:2])

            if i > 0:
                DebugDraw.add_line_2D(points[i-1], points[i], color, lifetime)
            
            current_angle += increment

        DebugDraw.add_line_2D(points[-1], points[0], color, lifetime)
        

    