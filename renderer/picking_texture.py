from typing import List
import OpenGL.GL as gl

from util.vectors import Vector2

class PickingTextureException(Exception):
    pass

class PickingTexture:
    def __init__(self, width: int, height: int):
        if not self.init(width, height):
            raise PickingTextureException("Error initialising picking texture")
        
    def init(self, width: int, height: int) -> bool:
         # Generate framebuffer
        self._fbo_id: int = gl.glGenFramebuffers(1)
        gl.glBindFramebuffer(gl.GL_FRAMEBUFFER, self._fbo_id)
        
        # Create the texture to render the data to, and attach it to our framebuffer
        self.picking_texture_id = gl.glGenTextures(1)
        gl.glBindTexture(gl.GL_TEXTURE_2D, self.picking_texture_id)
        gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_WRAP_S, gl.GL_REPEAT)
        gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_WRAP_T, gl.GL_REPEAT)
        gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAG_FILTER, gl.GL_NEAREST)
        gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MIN_FILTER, gl.GL_NEAREST)
        gl.glTexImage2D(gl.GL_TEXTURE_2D, 0, gl.GL_RGB32F, width, height, 0, gl.GL_RGB, gl.GL_FLOAT, None) # WARNING: None or pointer 0?

        gl.glFramebufferTexture2D(gl.GL_FRAMEBUFFER, gl.GL_COLOR_ATTACHMENT0, gl.GL_TEXTURE_2D, self.picking_texture_id, 0)

        # Create the texture object for the depth buffer
        gl.glEnable(gl.GL_TEXTURE_2D)
        self.depth_texture = gl.glGenTextures(1)
        gl.glBindTexture(gl.GL_TEXTURE_2D, self.depth_texture)
        gl.glTexImage2D(gl.GL_TEXTURE_2D, 0, gl.GL_DEPTH_COMPONENT, width, height, 0, gl.GL_DEPTH_COMPONENT, gl.GL_FLOAT, None) # SAME
        gl.glFramebufferTexture2D(gl.GL_FRAMEBUFFER, gl.GL_DEPTH_ATTACHMENT, gl.GL_TEXTURE_2D, self.depth_texture, 0)

        # Disable the reading
        gl.glReadBuffer(gl.GL_NONE)
        gl.glDrawBuffer(gl.GL_COLOR_ATTACHMENT0)

        # # Create renderbuffer to store depth info
        # rbo_id: int = gl.glGenRenderbuffers(1)
        # gl.glBindRenderbuffer(gl.GL_RENDERBUFFER, rbo_id)
        # gl.glRenderbufferStorage(gl.GL_RENDERBUFFER, gl.GL_DEPTH_COMPONENT32, width, height)
        # gl.glFramebufferRenderbuffer(gl.GL_FRAMEBUFFER, gl.GL_DEPTH_ATTACHMENT, gl.GL_RENDERBUFFER, rbo_id)

        if gl.glCheckFramebufferStatus(gl.GL_FRAMEBUFFER) != gl.GL_FRAMEBUFFER_COMPLETE:
            raise PickingTextureException("Error: Framebuffer is not complete")

        # Unbind the texture and framebuffer
        gl.glBindTexture(gl.GL_TEXTURE_2D, 0)
        gl.glBindFramebuffer(gl.GL_FRAMEBUFFER, 0)

        return True

    def enable_writing(self):
        gl.glBindFramebuffer(gl.GL_DRAW_FRAMEBUFFER, self._fbo_id)

    def disable_writing(self):
        gl.glBindFramebuffer(gl.GL_DRAW_FRAMEBUFFER, 0)

    def read_pixel(self, x: int, y: int) -> int:
        gl.glBindFramebuffer(gl.GL_READ_FRAMEBUFFER, self._fbo_id)
        gl.glReadBuffer(gl.GL_COLOR_ATTACHMENT0)
        
        pixels = gl.glReadPixels(x, y, 1, 1, gl.GL_RGB, gl.GL_FLOAT)
        return int(pixels[0][0][0]) - 1

    def read_pixels(self, start: Vector2, end: Vector2) -> List[float]:
        gl.glBindFramebuffer(gl.GL_READ_FRAMEBUFFER, self._fbo_id)
        gl.glReadBuffer(gl.GL_COLOR_ATTACHMENT0)

        size = (end - start).abs()
        num_pixels = size.x * size.y
        pixels = gl.glReadPixels(start.x, start.y, size.x, size.y, gl.GL_RGB, gl.GL_FLOAT)

        return [p-1 for p in pixels]



