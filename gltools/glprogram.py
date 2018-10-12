import logging
import ctypes
from pyglet import gl

def shader(stype, src):
    '''
    create and compile a shader of type stype with source code src
    return the shader (the return value of glCreateShader)
    '''
    handle = gl.glCreateShader(stype)
    buffer = ctypes.create_string_buffer(src)
    buf_pointer = ctypes.cast(ctypes.pointer(ctypes.pointer(buffer)), ctypes.POINTER(ctypes.POINTER(ctypes.c_char)))
    length = ctypes.c_int(len(src) + 1)
    gl.glShaderSource(handle, 1, buf_pointer, ctypes.byref(length))
    gl.glCompileShader(handle)
    success = gl.GLint(0)
    gl.glGetShaderiv(handle, gl.GL_COMPILE_STATUS, ctypes.pointer(success))
    length = gl.GLint(0)
    gl.glGetShaderiv(handle, gl.GL_INFO_LOG_LENGTH, ctypes.pointer(length))
    buffer = ctypes.create_string_buffer(length.value)
    gl.glGetShaderInfoLog(handle, length, None, buffer)
    log = buffer.value[:length.value].decode('ascii')
    for line in log.splitlines():
        logging.debug('GLSL: ' + line)

    if not success:
        raise Exception('Compiling of the shader failed.')
    return handle

class GlProgram:
    def __init__(self, vertex_shader, fragment_shader):
        self.handle = gl.glCreateProgram()
        logging.debug('GLProgram.__init__: self.handle = %r', self.handle)
        gl.glAttachShader(self.handle, shader(gl.GL_VERTEX_SHADER, vertex_shader))
        gl.glAttachShader(self.handle, shader(gl.GL_FRAGMENT_SHADER, fragment_shader))
        gl.glLinkProgram(self.handle)
        #call use() early so some programm errors are caught early
        self.use()

    def use(self):
        gl.glUseProgram(self.handle)

    def vertex_attrib_pointer(self, buffer, name, size, dtype=gl.GL_FLOAT, normalized=False, stride=0, offset=0):
        self.use()
        loc = gl.glGetAttribLocation(self.handle, ctypes.create_string_buffer(name))
        if loc < 0:
            logging.warning('Attribute %s is not in the shader.', name)
            return
        gl.glEnableVertexAttribArray(loc)
        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, buffer)
        gl.glVertexAttribPointer(loc, size, dtype, normalized, stride, ctypes.c_void_p(offset))

    def uniform1i(self, name, value):
        self.use()
        loc = gl.glGetUniformLocation(self.handle, ctypes.create_string_buffer(name))
        if loc < 0:
            logging.warning('Uniform %s is not in the shader.', name)
            return
        gl.glUniform1i(loc, value)

    def uniform2f(self, name, v0, v1):
        self.use()
        loc = gl.glGetUniformLocation(self.handle, ctypes.create_string_buffer(name))
        if loc < 0:
            logging.warning('Uniform %s is not in the shader.', name)
            return
        gl.glUniform2f(loc, v0, v1)
