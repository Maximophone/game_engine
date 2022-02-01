import ctypes
import numpy as np
from pyrr import Matrix44, Vector4
from components.sprite_renderer import SpriteRenderer
from renderer.shader import Shader

from typing import List
import OpenGL.GL as gl
from renderer.texture import Texture

from util.asset_pool import AssetPool
from util.vectors import Color4

class RenderBatch:
    # Vertex
    # ======
    # Pos                   Color                           Tex Coords      Tex id
    # float, float,         float, float, float, float,     float, float,   float
    def __init__(self, max_batch_size: int, z_index: int):
        self.POS_SIZE = 2
        self.COLOR_SIZE = 4
        self.TEX_COORDS_SIZE = 2
        self.TEX_ID_SIZE = 1
        self.ENTITY_ID_SIZE = 1
        self.POS_OFFSET = 0
        self.COLOR_OFFSET = self.POS_OFFSET + self.POS_SIZE * np.float32().itemsize
        self.TEX_COORDS_OFFSET = self.COLOR_OFFSET + self.COLOR_SIZE * np.float32().itemsize
        self.TEX_ID_OFFSET = self.TEX_COORDS_OFFSET + self.TEX_COORDS_SIZE * np.float32().itemsize
        self.ENTITY_ID_OFFSET = self.TEX_ID_OFFSET + self.TEX_ID_SIZE * np.float32().itemsize 
        self.VERTEX_SIZE = 10
        self.VERTEX_SIZE_BYTES = self.VERTEX_SIZE * np.float32().itemsize

        self.sprites: List[SpriteRenderer] = [None for _ in range(max_batch_size)]
        self.num_sprites: int = 0
        self.has_room: bool = True
        
        self._tex_slots = np.array([0,1,2,3,4,5,6,7], dtype=np.uint32)
        self._textures: List[Texture] = []
        self.vao_id: int = -1
        self.vbo_id: int = -1
        self.max_batch_size: int = max_batch_size
        self._z_index: int = z_index

        # 4 vertices quads
        self.vertices: np.ndarray = np.array([0.] * max_batch_size * 4 * self.VERTEX_SIZE, dtype=np.float32)

    @property
    def z_index(self) -> int:
        return self._z_index
        
    @property
    def has_texture_room(self) -> bool:
        return len(self._textures) < 8

    def has_texture(self, texture: Texture) -> bool:
        return texture in self._textures

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

        gl.glEnableVertexAttribArray(2)
        gl.glVertexAttribPointer(2, self.TEX_COORDS_SIZE, gl.GL_FLOAT, gl.GL_FALSE, self.VERTEX_SIZE_BYTES, ctypes.c_void_p(self.TEX_COORDS_OFFSET))

        gl.glEnableVertexAttribArray(3)
        gl.glVertexAttribPointer(3, self.TEX_ID_SIZE, gl.GL_FLOAT, gl.GL_FALSE, self.VERTEX_SIZE_BYTES, ctypes.c_void_p(self.TEX_ID_OFFSET))

        gl.glEnableVertexAttribArray(4)
        gl.glVertexAttribPointer(4, self.ENTITY_ID_SIZE, gl.GL_FLOAT, gl.GL_FALSE, self.VERTEX_SIZE_BYTES, ctypes.c_void_p(self.ENTITY_ID_OFFSET))

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

        if spr.get_texture() is not None:
            if spr.get_texture() not in self._textures:
                self._textures.append(spr.get_texture())

        # Add properties to local vertices array
        self.load_vertex_properties(index)
        if self.num_sprites >= self.max_batch_size:
            self.has_room = False

    def render(self):
        from renderer.renderer import Renderer
        from mxeng.window import Window

        rebuffer_data = False
        for i in range(self.num_sprites):
            spr = self.sprites[i]
            if spr.is_dirty():
                self.load_vertex_properties(i)
                spr.set_clean()
                rebuffer_data = True

        if rebuffer_data:
            gl.glBindBuffer(gl.GL_ARRAY_BUFFER, self.vbo_id)
            gl.glBufferSubData(gl.GL_ARRAY_BUFFER, 0, self.vertices.nbytes, self.vertices)

        # Use shader
        shader = Renderer.get_bound_shader()
        shader.use()
        shader.upload_mat4f("uProj", Window.get_scene().camera().get_projection_matrix())
        shader.upload_mat4f("uView", Window.get_scene().camera().get_view_matrix())

        for i in range(len(self._textures)):
            gl.glActiveTexture(gl.GL_TEXTURE0 + i + 1)
            self._textures[i].bind()
        shader.upload_int_array("uTextures", self._tex_slots)

        gl.glBindVertexArray(self.vao_id)
        gl.glEnableVertexAttribArray(0)
        gl.glEnableVertexAttribArray(1)
        gl.glEnableVertexAttribArray(2)
        gl.glEnableVertexAttribArray(3)
        gl.glEnableVertexAttribArray(4)

        gl.glDrawElements(gl.GL_TRIANGLES, self.num_sprites * 6, gl.GL_UNSIGNED_INT, ctypes.c_void_p(0))

        gl.glDisableVertexAttribArray(0)
        gl.glDisableVertexAttribArray(1)
        gl.glDisableVertexAttribArray(2)
        gl.glDisableVertexAttribArray(3)
        gl.glDisableVertexAttribArray(4)
        gl.glBindVertexArray(0)

        for i in range(len(self._textures)):
            self._textures[i].unbind()

        shader.detach()

    def load_vertex_properties(self, index: int):
        sprite: SpriteRenderer = self.sprites[index]

        # Find offset within array (4 vertices per sprite)
        offset: int = index * 4 * self.VERTEX_SIZE

        color: Color4 = sprite.get_color()
        tex_coords = sprite.get_tex_coords()

        tex_id = 0
        if sprite.get_texture() is not None:
            for i, texture in enumerate(self._textures):
                if texture == sprite.get_texture():
                    tex_id = i + 1
                    break
        
        is_rotated = sprite.game_object.transform.rotation != 0.
        transform_matrix = Matrix44.identity()
        if is_rotated:
            transform_matrix *= Matrix44.from_translation(sprite.game_object.transform.position)
            transform_matrix *= Matrix44.from_z_rotation(sprite.game_object.transform.rotation / 360 * np.pi * 2)
            transform_matrix *= Matrix44.from_scale(sprite.game_object.transform.scale)
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
            
            if not is_rotated:
                current_pos = Vector4([
                    sprite.game_object.transform.position.x + (x_add * sprite.game_object.transform.scale.x),
                    sprite.game_object.transform.position.y + (y_add * sprite.game_object.transform.scale.y),
                    0,
                    1
                ])
            else:
                current_pos = transform_matrix * Vector4([x_add, y_add, 0, 1])

            # Load position
            self.vertices[offset] = current_pos.x
            self.vertices[offset + 1] = current_pos.y

            # Load color
            self.vertices[offset + 2] = color[0]
            self.vertices[offset + 3] = color[1]
            self.vertices[offset + 4] = color[2]
            self.vertices[offset + 5] = color[3]

            # Load texture coordinates
            self.vertices[offset + 6] = tex_coords[i][0]
            self.vertices[offset + 7] = tex_coords[i][1]

            # Load texture id
            self.vertices[offset + 8] = tex_id

            # Load entity id
            self.vertices[offset + 9] = sprite.game_object.uid + 1


            offset += self.VERTEX_SIZE