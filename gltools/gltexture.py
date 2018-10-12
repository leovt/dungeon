import PIL.Image
from pyglet import gl
import logging
import ctypes

def make_texture(filename, indexed=False):
    name = gl.GLuint(0)
    gl.glGenTextures(1, ctypes.pointer(name))
    gl.glBindTexture(gl.GL_TEXTURE_2D, name)
    gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MIN_FILTER, gl.GL_NEAREST)
    gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAG_FILTER, gl.GL_NEAREST)
    gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_WRAP_S, gl.GL_CLAMP_TO_EDGE)
    gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_WRAP_T, gl.GL_CLAMP_TO_EDGE)

    image = PIL.Image.open(filename)
    if indexed:
        assert image.mode == 'P'
    else:
        image = image.convert('RGBA')
    logging.debug('loading %s mode=%s', filename, image.mode)

    width, height = image.size
    if indexed:
        assert len(image.tobytes()) == width * height
        gl.glTexImage2D(gl.GL_TEXTURE_2D,
                 0,  # level
                 gl.GL_R8,
                 width,
                 height,
                 0,
                 gl.GL_RED,
                 gl.GL_UNSIGNED_BYTE,
                 ctypes.create_string_buffer(image.tobytes()))
    else:
        assert len(image.tobytes()) == width * height * 4
        gl.glTexImage2D(gl.GL_TEXTURE_2D,
                 0,  # level
                 gl.GL_RGBA8,
                 width,
                 height,
                 0,
                 gl.GL_RGBA,
                 gl.GL_UNSIGNED_BYTE,
                 ctypes.create_string_buffer(image.tobytes()))
    gl.glBindTexture(gl.GL_TEXTURE_2D, 0)
    return name
