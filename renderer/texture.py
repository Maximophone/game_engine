import OpenGL.GL as gl
from PIL import Image
import numpy as np

class Texture:
    def __init__(self, filepath: str):
        self._filepath = filepath
        self._tex_id: int = -1
        self.width: int = 0
        self.height: int = 0

        # Generate texture on GPU
        self._tex_id = gl.glGenTextures(1)
        gl.glBindTexture(gl.GL_TEXTURE_2D, self._tex_id)

        # Set texture parameters
        # Repeat image in both directions
        gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_WRAP_S, gl.GL_REPEAT)
        gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_WRAP_T, gl.GL_REPEAT)

        # When stretching the image, pixelate
        gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MIN_FILTER, gl.GL_NEAREST)

        # When shrinking an image, pixelate
        gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAG_FILTER, gl.GL_NEAREST)

        with Image.open(self._filepath) as image:
            self.width = image.width
            self.height = image.height
            img_data = np.array(list(image.transpose(Image.FLIP_TOP_BOTTOM).convert("RGBA").getdata()), np.uint8)

            gl.glTexImage2D(gl.GL_TEXTURE_2D, 0, gl.GL_RGBA, image.width, image.height, 0, gl.GL_RGBA, gl.GL_UNSIGNED_BYTE, img_data)

    def bind(self):
        gl.glBindTexture(gl.GL_TEXTURE_2D, self._tex_id)

    def unbind(self):
        gl.glBindTexture(gl.GL_TEXTURE_2D, 0)