import ctypes
import numpy as np
from components.sprite_renderer import SpriteRenderer
from renderer.shader import Shader

from pyrr import vector4

from typing import List
import OpenGL.GL as gl

class RenderBatch:
    # Vertex
    # ======
    # Pos                   Color
    # float, float,         float, float, float, float
    def __init__(self, max_batch_size: int):
        self.POS_SIZE = 2
        self.COLOR_SIZE = 4
        self.POS_OFFSET = 0
        self.COLOR_OFFSET = self.POS_OFFSET + self.POS_SIZE * np.float32().itemsize
        self.VERTEX_SIZE = 6
        self.VERTEX_SIZE_BYTES = self.VERTEX_SIZE * np.float32().itemsize

        self.sprites: List[SpriteRenderer] = [None for _ in range(max_batch_size)]
        self.num_sprites: int = 0
        self.has_room: bool = True
        

        self.vao_id: int = -1
        self.vbo_id: int = -1
        self.max_batch_size: int = max_batch_size
        self.shader: Shader = Shader("assets/shaders/default.glsl")
        self.shader.compile()

        # 4 vertices quads
        self.vertices: np.ndarray = np.array([0.] * max_batch_size * 4 * self.VERTEX_SIZE, dtype=np.float32)

    def start(self):
        # Generate and bind a vertex array object
        self.vao_id = gl.glGenVertexArrays(1)
        gl.glBindVertexArray(self.vao_id)

        # Allocate space for the vertices
        self.vbo_id = gl.glGenBuffers(1)
        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, self.vbo_id)
        gl.glBufferData(gl.GL_ARRAY_BUFFER, self.vertices.nbytes, self.vertices, gl.GL_DYNAMIC_DRAW)

        # Create and upload indices buffer
        ebo_id = gl.glGenBuffers(1)
        indices = np.array(self.generate_indices(), dtype=np.uint32)
        
        gl.glBindBuffer(gl.GL_ELEMENT_ARRAY_BUFFER, ebo_id)
        gl.glBufferData(gl.GL_ELEMENT_ARRAY_BUFFER, indices.nbytes, indices, gl.GL_STATIC_DRAW)
        #gl.glBufferData(gl.GL_ELEMENT_ARRAY_BUFFER, element_array.nbytes, element_array, gl.GL_STATIC_DRAW)

        # Enable the buffer attribute pointers
        gl.glEnableVertexAttribArray(0)
        gl.glVertexAttribPointer(0, self.POS_SIZE, gl.GL_FLOAT, gl.GL_FALSE, self.VERTEX_SIZE_BYTES, ctypes.c_void_p(self.POS_OFFSET))
        
        gl.glEnableVertexAttribArray(1)
        gl.glVertexAttribPointer(1, self.COLOR_SIZE, gl.GL_FLOAT, gl.GL_FALSE, self.VERTEX_SIZE_BYTES, ctypes.c_void_p(self.COLOR_OFFSET))
        

    def generate_indices(self) -> List[int]:
        # 6 indices per quad (3 per triangle)
        elements = [0] * 6 * self.max_batch_size
        for i in range(self.max_batch_size):
            self.load_element_indices(elements, i)

        return elements

    def load_element_indices(self, elements: List[int], index: int):
        offset_array_index = 6 * index
        offset = 4 * index  # 4 unique numbers are used per quad (4 vertices)
        # 3, 2, 0, 0, 2, 1          7, 6, 7, 7, 6, 5
        # Triangle 1
        elements[offset_array_index] = offset + 3
        elements[offset_array_index + 1] = offset + 2
        elements[offset_array_index + 2] = offset + 0

        # Triangle 2
        elements[offset_array_index + 3] = offset + 0
        elements[offset_array_index + 4] = offset + 2
        elements[offset_array_index + 5] = offset + 1

    def add_sprite(self, spr: SpriteRenderer):
        # Get index and add renderObject
        index: int = self.num_sprites
        self.sprites[index] = spr
        self.num_sprites += 1

        # Add properties to local vertices array
        self.load_vertex_properties(index)
        if self.num_sprites >= self.max_batch_size:
            self.has_room = False

    def render(self):
        from mxeng.window import Window
        # For now we will rebuffer all data every frame
        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, self.vbo_id)
        gl.glBufferSubData(gl.GL_ARRAY_BUFFER, 0, self.vertices.nbytes, self.vertices)

        # Use shader
        self.shader.use()
        self.shader.upload_mat4f("uProj", Window.get_scene().camera().get_projection_matrix())
        self.shader.upload_mat4f("uView", Window.get_scene().camera().get_view_matrix())

        gl.glBindVertexArray(self.vao_id)
        gl.glEnableVertexAttribArray(0)
        gl.glEnableVertexAttribArray(1)

        gl.glDrawElements(gl.GL_TRIANGLES, self.num_sprites * 6, gl.GL_UNSIGNED_INT, ctypes.c_void_p(0))

        gl.glDisableVertexAttribArray(0)
        gl.glDisableVertexAttribArray(1)
        gl.glBindVertexArray(0)

        self.shader.detach()

    def load_vertex_properties(self, index: int):
        sprite: SpriteRenderer = self.sprites[index]

        # Find offset within array (4 vertices per sprite)
        offset: int = index * 4 * self.VERTEX_SIZE

        color: vector4 = sprite.get_color()

        # Add vertices with the appropriate properties
        x_add: float = 1.
        y_add: float = 1.
        for i in range(4):
            if i == 1:
                y_add = 0.
            elif i == 2:
                x_add = 0.
            elif i == 3:
                y_add = 1.
            
            # Load position
            self.vertices[offset] = sprite.game_object.transform.position[0] + (x_add * sprite.game_object.transform.scale[0])
            self.vertices[offset + 1] = sprite.game_object.transform.position[1] + (y_add * sprite.game_object.transform.scale[1])

            # Load color
            self.vertices[offset + 2] = color[0]
            self.vertices[offset + 3] = color[1]
            self.vertices[offset + 4] = color[2]
            self.vertices[offset + 5] = color[3]

            offset += self.VERTEX_SIZE