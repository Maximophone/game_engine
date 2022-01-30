from typing import Optional
import OpenGL.GL as gl
from PIL import Image
import numpy as np

from util.serialization import serializable, sproperty

@serializable()
class Texture:
    def __init__(self, filepath: str = None, width: int = None, height: int = None):
        self._filepath = filepath
        self._tex_id: Optional[int] = None
        self.width: int = width
        self.height: int = height
        if filepath is not None:
            self.init()
        elif (width is not None) and (height is not None):
            self.init_generated()

    @sproperty
    def filepath(self) -> str:
        return self._filepath

    @filepath.setter
    def filepath(self, value: str):
        self._filepath = value
        self.init()

    @property
    def tex_id(self) -> Optional[int]:
        return self._tex_id

    def init(self):
        self._tex_id = -1
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

    def init_generated(self):
        self._filepath = "Generated"

        # Generate texture on GPU
        self._tex_id = gl.glGenTextures(1)
        gl.glBindTexture(gl.GL_TEXTURE_2D, self._tex_id)

        gl.glTexImage2D(gl.GL_TEXTURE_2D, 0, gl.GL_RGB, self.width, self.height, 0, gl.GL_RGB, gl.GL_UNSIGNED_BYTE, None) # WARNING: is the last argument 0 or None or a pointer



    def bind(self):
        gl.glBindTexture(gl.GL_TEXTURE_2D, self._tex_id)

    def unbind(self):
        gl.glBindTexture(gl.GL_TEXTURE_2D, 0)

    def __eq__(self, o: "Texture") -> bool:
        if o is None:
            return False
        if not isinstance(o, Texture):
            return False
        return (self.width == o.width) and (self.height == o.height) and (self.tex_id == o.tex_id) and (self.filepath == o.filepath)