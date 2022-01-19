# from components.font_renderer import FontRenderer
# from components.sprite_renderer import SpriteRenderer
# from mxeng.game_object import GameObject
# from renderer.texture import Texture
# from util.timer import Time
from components.sprite_renderer import SpriteRenderer
from mxeng.camera import Camera
from mxeng.game_object import GameObject
from mxeng.scene import Scene
# from renderer.shader import Shader

# import OpenGL.GL as gl
import numpy as np
# import ctypes
from pyrr import vector3, vector4

from mxeng.transform import Transform

class LevelEditorScene(Scene):

    def __init__(self):
        super().__init__()
        # self.first_time = True
        # self._default_shader = None
        # self._test_texture: Texture = None


        # self._vertex_array = np.array([
        #     # position              # color                 # UV coordinates
        #     100.5, -0.5, 0.,        1., 0., 0., 1.,         1, 1, # bottom right
        #     -0.5, 100.5, 0.,        0., 1., 0., 1.,         0, 0, # top left
        #     100.5, 100.5, 0.,       0., 0., 1., 1.,         1, 0, # top right
        #     -0.5, -0.5, 0.,         1., 1., 0., 1.,         0, 1, # bottom left
        # ], dtype=np.float32)
        # self._element_array = np.array([
        #     2, 1, 0, # top right triangle
        #     0, 1, 3, # bottom left triangle
        # ], dtype=np.uint32)

        # self._vao_id: int = -1
        # self._vbo_id: int = -1
        # self._ebo_id: int = -1

        print("Inside Level Editor Scene")

    def init(self):
        self._camera = Camera(vector3.create())

        x_offset = 10
        y_offset = 10

        total_width = 600. - x_offset * 2
        total_height = 300. - y_offset * 2
        size_x = total_width / 100.
        size_y = total_height / 100.

        for x in range(100):
            for y in range(100):
                x_pos = x_offset + (x*size_x)
                y_pos = y_offset + (y*size_y)

                go = GameObject(f"Obj{x}_{y}", Transform(np.array([x_pos, y_pos]), np.array([size_x, size_y])))
                go.add_component(SpriteRenderer(vector4.create(x_pos/total_width, y_pos/total_height, 1., 1.)))
                self.add_game_object_to_scene(go)
        # print("Creating test object")
        # self.test_obj = GameObject("test object")
        # self.test_obj.add_component(SpriteRenderer())
        # self.test_obj.add_component(FontRenderer())
        # self.add_game_object_to_scene(self.test_obj)

        # self._camera = Camera(vector3.create())
        # self._default_shader = Shader("assets/shaders/default.glsl")
        # self._default_shader.compile()
        # self._test_texture = Texture("assets/images/testImage.png")

        # # ===========================================================
        # # Generate VAO, VBO and EBO buffer objects, and send to GPU
        # # ===========================================================

        # self._vao_id = gl.glGenVertexArrays(1)
        # gl.glBindVertexArray(self._vao_id)

        # positions_size: int = 3
        # color_size: int = 4
        # uv_size: int = 2
        # vertex_size_bytes: int = (positions_size + color_size + uv_size) * self._vertex_array.itemsize
        # # Create VBO upload the vertex buffer
        # self._vbo_id = gl.glGenBuffers(1)
        # gl.glBindBuffer(gl.GL_ARRAY_BUFFER, self._vbo_id)
        # gl.glBufferData(gl.GL_ARRAY_BUFFER, self._vertex_array.nbytes, self._vertex_array, gl.GL_STATIC_DRAW)

        # # Create the indices and upload
        # self._ebo_id = gl.glGenBuffers(1)
        # gl.glBindBuffer(gl.GL_ELEMENT_ARRAY_BUFFER, self._ebo_id)
        # gl.glBufferData(gl.GL_ELEMENT_ARRAY_BUFFER, self._element_array.nbytes, self._element_array, gl.GL_STATIC_DRAW)

        # # Add the vertex attribute pointers

        # gl.glEnableVertexAttribArray(0)
        # gl.glVertexAttribPointer(0, positions_size, gl.GL_FLOAT, gl.GL_FALSE, vertex_size_bytes, ctypes.c_void_p(0))
 
        # gl.glEnableVertexAttribArray(1)
        # gl.glVertexAttribPointer(1, color_size, gl.GL_FLOAT, gl.GL_FALSE, vertex_size_bytes, ctypes.c_void_p(positions_size*self._vertex_array.itemsize))

        # gl.glEnableVertexAttribArray(2)
        # gl.glVertexAttribPointer(2, uv_size, gl.GL_FLOAT, gl.GL_FALSE, vertex_size_bytes, ctypes.c_void_p((positions_size+color_size)*self._vertex_array.itemsize))


    def update(self, dt: float):
        # self._default_shader.use()

        # # Upload texture to shader
        # self._default_shader.upload_texture("TEX_SAMPLER", 0)
        # gl.glActiveTexture(gl.GL_TEXTURE0)
        # self._test_texture.bind()

        # self._default_shader.upload_mat4f("uProj", self._camera.get_projection_matrix())
        # self._default_shader.upload_mat4f("uView", self._camera.get_view_matrix())
        # self._default_shader.upload_float("uTime", Time.get_time())

        # # Bind the VAO that we're using
        # gl.glBindVertexArray(self._vao_id)

        # # Enable the vertex attribute pointers
        # gl.glEnableVertexAttribArray(0)
        # gl.glEnableVertexAttribArray(1)

        # gl.glDrawElements(gl.GL_TRIANGLES, len(self._element_array), gl.GL_UNSIGNED_INT, ctypes.c_void_p(0))

        # # Unbind everything
        # gl.glDisableVertexAttribArray(0)
        # gl.glDisableVertexAttribArray(1)

        # gl.glBindVertexArray(0)

        # self._default_shader.detach()

        # if self.first_time:
        #     print("Creating gameObject!")
        #     go = GameObject("game test 2")
        #     go.add_component(SpriteRenderer())
        #     self.add_game_object_to_scene(go)
        # self.first_time = False

        for go in self._game_objects:
            go.update(dt)

        self._renderer.render()

