import ctypes
from typing import List

from pyrr import Vector3, Vector4
from renderer.line_2d import Line2D
from renderer.shader import Shader
from util.asset_pool import AssetPool
from mxeng.window import Window

import numpy as np
import OpenGL.GL as gl


class DebugDraw:
    MAX_LINES: int = 500
    lines: List[Line2D] = []
    # 6 floats per vertex, 2 vertices per line
    vertex_array: np.ndarray = np.zeros(MAX_LINES*6*2, dtype=np.float32)
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
        gl.glDrawArrays(gl.GL_LINES, 0, 6*2*len(DebugDraw.lines))
        
        # Disable location
        gl.glDisableVertexAttribArray(0)
        gl.glDisableVertexAttribArray(1)
        gl.glBindVertexArray(0)

        DebugDraw.shader.detach()

    # ====================
    # Add line2D methods
    # ====================
    @staticmethod
    def add_line_2D(from_: np.ndarray, to: np.ndarray, color: Vector3 = None, lifetime: int = 1):
        # TODO: add constants for common colors
        color = color if color is not None else Vector3([0., 1., 0.])
        if len(DebugDraw.lines) >= DebugDraw.MAX_LINES:
            return
        DebugDraw.lines.append(Line2D(from_, to, color, lifetime))

