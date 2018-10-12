vertex_sprite = b'''
#version 130
attribute vec4 position;
attribute vec4 tex_coord;

out vec4 frag_tex_coord;

uniform vec2 scale;
uniform vec2 offset;

void main()
{
    gl_Position = vec4((position.x-offset.x) * scale.x,
                       (position.y-offset.y) * scale.y,
                       position.z / 256.0,
                       1.0);
    frag_tex_coord = tex_coord;
}
'''

fragment_sprite = b'''
#version 130

uniform sampler2D tex;
varying vec4 frag_tex_coord;

out vec4 FragColor;

void main()
{
    FragColor = texture2D(tex, frag_tex_coord.xy);
}
'''
