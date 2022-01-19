import re
from pyrr import matrix44, matrix33, vector4, vector3
import numpy as np

import OpenGL.GL as gl

class Shader:
    def __init__(self, filepath: str):
        self._vertex_id: int = -1
        self._fragment_id: int = -1
        self._shader_program_id: int = -1
        self._being_used: bool = False
        self._vertex_source: str = ""
        self._fragment_source: str = ""
        self._filepath: str = filepath
        with open(filepath, "r") as f:
            source: str = f.read()
        split_string = re.split(r"#type(?: )+[a-zA-Z]+", source)

        # Find the first patter after #type 'pattern'
        index = source.index("#type") + 6
        eol = source.index("\n", index)
        first_pattern: str = source[index:eol].strip()

        # Second pattern
        index = source.index("#type", eol) + 6
        eol = source.index("\n", index)
        second_pattern: str = source[index:eol].strip()

        if first_pattern == "vertex":
            self._vertex_source = split_string[1]
        elif first_pattern == "fragment":
            self._fragment_source = split_string[1]
        else:
            assert False, f"Unexpected token: {first_pattern} in shader file {filepath}"

        if second_pattern == "vertex":
            self._vertex_source = split_string[2]
        elif second_pattern == "fragment":
            self._fragment_source = split_string[2]
        else:
            assert False, f"Unexpected token: {second_pattern} in shader file {filepath}"

    def compile(self):
        # =========================================
        # Compile and link shaders
        # =========================================

        # First load and compile the vertex shader
        self._vertex_id = gl.glCreateShader(gl.GL_VERTEX_SHADER)
        # Pass the shader source to the GPU
        gl.glShaderSource(self._vertex_id, self._vertex_source)
        gl.glCompileShader(self._vertex_id)

        # Check for errors in compilation
        success: int = gl.glGetShaderiv(self._vertex_id, gl.GL_COMPILE_STATUS)
        if success == gl.GL_FALSE:
            print(f"ERROR: {self._filepath}\n\tVertex shader compilation failed")
            print(gl.glGetShaderInfoLog(self._vertex_id))
            assert False, "shader problem"

        # First load and compile the fragment shader
        self._fragment_id = gl.glCreateShader(gl.GL_FRAGMENT_SHADER)
        # Pass the shader source to the GPU
        gl.glShaderSource(self._fragment_id, self._fragment_source)
        gl.glCompileShader(self._fragment_id)

        # Check for errors in compilation
        success: int = gl.glGetShaderiv(self._fragment_id, gl.GL_COMPILE_STATUS)
        if success == gl.GL_FALSE:
            print(f"ERROR: {self._filepath}\n\tFragment shader compilation failed")
            print(gl.glGetShaderInfoLog(self._fragment_id))
            assert False, "shader problem"

        # link shaders and check for errors
        self._shader_program_id = gl.glCreateProgram()
        gl.glAttachShader(self._shader_program_id, self._vertex_id)
        gl.glAttachShader(self._shader_program_id, self._fragment_id)
        gl.glLinkProgram(self._shader_program_id)

        # Check for linking errors
        success: int = gl.glGetProgramiv(self._shader_program_id, gl.GL_LINK_STATUS)
        if success == gl.GL_FALSE:
            print(f"ERROR: {self._filepath}\n\tProgram linking failed")
            print(gl.glGetProgramInfoLog(self._shader_program_id))
            assert False, "shader problem"

    def use(self):
        if not self._being_used:
            # Bind shader program
            gl.glUseProgram(self._shader_program_id)
            self._being_used = True

    def detach(self):
        gl.glUseProgram(0)
        self._being_used = False

    def upload_mat4f(self, var_name: str, mat4: matrix44):
        var_location: int = gl.glGetUniformLocation(self._shader_program_id, var_name)
        self.use()
        gl.glUniformMatrix4fv(var_location, 1, gl.GL_FALSE, mat4)

    def upload_mat3f(self, var_name: str, mat3: matrix33):
        var_location: int = gl.glGetUniformLocation(self._shader_program_id, var_name)
        self.use()
        gl.glUniformMatrix3fv(var_location, 1, gl.GL_FALSE, mat3)

    def upload_vec4f(self, var_name: str, vec4f: vector4):
        var_location: int = gl.glGetUniformLocation(self._shader_program_id, var_name)
        self.use()
        gl.glUniform4f(var_location, *vec4f)

    def upload_vec3f(self, var_name: str, vec3f: vector3):
        var_location: int = gl.glGetUniformLocation(self._shader_program_id, var_name)
        self.use()
        gl.glUniform3f(var_location, *vec3f)

    def upload_vec2f(self, var_name: str, vec2f):
        var_location: int = gl.glGetUniformLocation(self._shader_program_id, var_name)
        self.use()
        gl.glUniform2f(var_location, *vec2f)

    def upload_float(self, var_name: str, val: float):
        var_location: int = gl.glGetUniformLocation(self._shader_program_id, var_name)
        self.use()
        gl.glUniform1f(var_location, val)

    def upload_int(self, var_name: str, val: int):
        var_location: int = gl.glGetUniformLocation(self._shader_program_id, var_name)
        self.use()
        gl.glUniform1i(var_location, val)

    def upload_texture(self, var_name: str, slot: int):
        var_location: int = gl.glGetUniformLocation(self._shader_program_id, var_name)
        self.use()
        gl.glUniform1i(var_location, slot)

    def upload_int_array(self, var_name: str, array: np.ndarray):
        var_location: int = gl.glGetUniformLocation(self._shader_program_id, var_name)
        self.use()
        gl.glUniform1iv(var_location, len(array), array)

    
