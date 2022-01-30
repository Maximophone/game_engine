import OpenGL.GL as gl
from renderer.texture import Texture

class FramebufferException(Exception):
    pass

class Framebuffer:
    def __init__(self, width: int, height: int):
        self.width: int = width
        self.height: int = height

        # Generate framebuffer
        self._fbo_id: int = gl.glGenFramebuffers(1)
        gl.glBindFramebuffer(gl.GL_FRAMEBUFFER, self._fbo_id)

        # Create the texture to render the data to, and attach it to our framebuffer
        self._texture: Texture = Texture(width=width, height=height)

        gl.glFramebufferTexture2D(gl.GL_FRAMEBUFFER, gl.GL_COLOR_ATTACHMENT0, gl.GL_TEXTURE_2D, self._texture.tex_id, 0)

        # Create renderbuffer to store depth info
        rbo_id: int = gl.glGenRenderbuffers(1)
        gl.glBindRenderbuffer(gl.GL_RENDERBUFFER, rbo_id)
        gl.glRenderbufferStorage(gl.GL_RENDERBUFFER, gl.GL_DEPTH_COMPONENT32, width, height)
        gl.glFramebufferRenderbuffer(gl.GL_FRAMEBUFFER, gl.GL_DEPTH_ATTACHMENT, gl.GL_RENDERBUFFER, rbo_id)

        if gl.glCheckFramebufferStatus(gl.GL_FRAMEBUFFER) != gl.GL_FRAMEBUFFER_COMPLETE:
            raise FramebufferException("Error: Framebuffer is not complete")

        gl.glBindFramebuffer(gl.GL_FRAMEBUFFER, 0)

    @property
    def texture_id(self) -> int:
        return self._texture.id

    @property
    def fbo_id(self) -> int:
        return self._fbo_id

    def bind(self):
        gl.glBindFramebuffer(gl.GL_FRAMEBUFFER, self._fbo_id)

    def unbind(self):
        gl.glBindFramebuffer(gl.GL_FRAMEBUFFER, 0)