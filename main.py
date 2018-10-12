import sys
import logging.config
import ctypes

import pyglet
from pyglet import gl
from pyglet.window import key

import shaders
from gltools.glprogram import GlProgram
from gltools import gltexture

from dungeon_map import DungeonMap

class Application:
    def __init__(self, window):
        self.window = window
        self.initialize_gl()

        self.dungeon_map = DungeonMap()

    def update(self, dt):
        pass

    def initialize_gl(self):
        self.program = GlProgram(shaders.vertex_sprite, shaders.fragment_sprite)
        self.program.uniform2f(b'offset', 0, 0)
        self.program.uniform2f(b'scale', 30, 20)

        self.buffer = gl.GLuint(0)
        gl.glGenBuffers(1, ctypes.pointer(self.buffer))

        gl.glActiveTexture(gl.GL_TEXTURE0)
        self.sprite_texture = gltexture.make_texture('sprites.png')
        gl.glBindTexture(gl.GL_TEXTURE_2D, self.sprite_texture)
        self.program.uniform1i(b'tex', 0)

        gl.glEnable(gl.GL_BLEND)
        gl.glEnable(gl.GL_DEPTH_TEST)
        gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)

    def on_resize(self, width, height):
        gl.glViewport(0, 0, width, height)
        TILE_SIZE = 40
        self.program.uniform2f(b'scale', width/TILE_SIZE*0.5, height/TILE_SIZE*0.5)
        self.vp_width = width
        self.vp_height = height

    def on_draw(self):
        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)

        STRIDE = 8

        self.program.use()
        self.program.vertex_attrib_pointer(self.buffer, b'position', 4, stride=STRIDE * ctypes.sizeof(gl.GLfloat))
        self.program.vertex_attrib_pointer(self.buffer, b'tex_coord', 4, stride=STRIDE * ctypes.sizeof(gl.GLfloat), offset=4 * ctypes.sizeof(gl.GLfloat))

        nb_vertices = 0
        data = []
        data = (gl.GLfloat * (STRIDE * nb_vertices))(*data)

        gl.glBufferData(gl.GL_ARRAY_BUFFER, ctypes.sizeof(data), data, gl.GL_DYNAMIC_DRAW)
        gl.glDrawArrays(gl.GL_TRIANGLES, 0, nb_vertices)

    def on_key_press(self, symbol, modifiers):
        logging.debug('Key Press {} {}'.format(symbol, modifiers))
        if symbol == key.I:
            logging.info('FPS: {}'.format(pyglet.clock.get_fps()))

def initialize_gl(context):
    logging.info('OpenGL Version {}'.format(context.get_info().get_version()))
    gl.glClearColor(0.5, 0.5, 0.35, 1)

def main():
    logging.config.fileConfig('logging.conf')
    try:
        window = pyglet.window.Window(resizable=True)
        initialize_gl(window.context)

        app = Application(window)
        window.push_handlers(app)

        pyglet.clock.schedule_interval(app.update, 0.01)
        pyglet.app.run()

    except:
        logging.exception('Uncaught Exception')
        sys.exit(1)

if __name__ == '__main__':
    main()
