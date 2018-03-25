import OpenGL.GL as GL
import glm
import OpenGL.GL.shaders
from OpenGL.GLU import *
from OpenGL.GLUT import *
import ctypes
import pygame
import numpy

x_road1 = 0
x_road2 = 80

x_sidewalk1 = 0
x_sidewalk2 = 50

transform_road = 0.0
transform_sidewalk = 0.0
skyColorR = 109/255
skyColorG = 238/255
skyColorB = 255/255

skyDarkR = 13/255
skyDarkG = 50/255
skyDarkB = 73/255

skyR = 109/255
skyG = 238/255
skyB = 255/255

plus = False

dR = (- skyDarkR + skyColorR)/1500
dG = (- skyDarkG + skyColorG)/1500
dB = (- skyDarkB + skyColorB)/1500

vertex_shader = """
#version 330

layout (location = 0) in vec4 position;
layout (location = 1) in vec2 aTexCoord;
out vec2 TexCoord;

void main()
{
   
   gl_Position = vec4(position.x, position.y, 0.0, 1.0);
   TexCoord = vec2(aTexCoord.x, aTexCoord.y);
}
"""

vertex_shader_road = """
#version 330

layout (location = 0) in vec4 position;
layout (location = 1) in vec2 aTexCoord;
uniform float transform;
out vec2 TexCoord;

void main()
{
   
   gl_Position = vec4(position.x + transform, position.y, 0.0, 1.0);
   TexCoord = vec2(aTexCoord.x, aTexCoord.y);
}
"""

fragment_shader_road = """
#version 330
void main()
{
   gl_FragColor = vec4(0.24f, 0.24f, 0.24f, 1.0f);
}
"""

fragment_shader_sky = """
#version 330

uniform float r, g, b;

void main()
{
   gl_FragColor = vec4(109.0f/255.0f + r, 238.0f/255.0f + g, 255.0f/255.0f + b, 0.0f);
}
"""

fragment_shader_sidewalk = """
#version 330
void main()
{
   gl_FragColor = vec4(0.0f, 0.0f, 0.0f, 1.0f);
}
"""

fragment_shader_white = """
#version 330
void main()
{
   gl_FragColor = vec4(1.0f, 1.0f, 1.0f, 1.0f);
}
"""

def fx(x):
    return (1 - (2 - 2*x/800))

def fy(y):
    return (1 - (2 - 2*y/600))

background = [-1.0, 1.0, 0.0, 1.0,
              1.0, 1.0, 0.0, 1.0,
              1.0, -1.0, 0.0, 1.0,
              -1.0, -1.0, 0.0, 1.0]

road = [0.0, 200.0, 0.0, 1.0,
        800.0, 200.0, 0.0, 1.0,
        800.0, 0.0, 0.0, 1.0,
        0.0, 0.0, 0.0, 1.0]

road_white = []

sidewalk = [0.0, 200.0, 0.0, 1.0,
        800.0, 200.0, 0.0, 1.0,
        800.0, 230.0, 0.0, 1.0,
        0.0, 230.0, 0.0, 1.0]

sidewalk_white = []

vertices = [ 1,  1, 0.0, 1.0,
            0.0,  0.6, 0.0, 1.0,
             0.0, -0.6, 0.0, 1.0]

vertices2 = [ 0.0,  0.6, 0.0, 1.0,
            -0.6,  0.6, 0.0, 1.0,
             0.0, -0.6, 0.0, 1.0]

background = numpy.array(background, dtype=numpy.float32)			 
vertices = numpy.array(vertices, dtype=numpy.float32)
vertices2 = numpy.array(vertices2, dtype=numpy.float32)

def convert_coordinate():
    global road, sidewalk, road_white, sidewalk_white
    global x_road1, x_road2

    #init white dashed road
    x1 = x_road1
    x2 = x_road2
    for i in range(0,10):
        road_white.append(fx(x1))
        road_white.append(fy(100))
        road_white.append(0.0)
        road_white.append(1.0)

        road_white.append(fx(x2))
        road_white.append(fy(100))
        road_white.append(0.0)
        road_white.append(1.0)

        road_white.append(fx(x1))
        road_white.append(fy(130))
        road_white.append(0.0)
        road_white.append(1.0)

        road_white.append(fx(x2))
        road_white.append(fy(130))
        road_white.append(0.0)
        road_white.append(1.0)
        x1 += 160
        x2 += 160
    
    x1 = x_sidewalk1
    x2 = x_sidewalk2
    for i in range(0,20):
        sidewalk_white.append(fx(x1))
        sidewalk_white.append(fy(200))
        sidewalk_white.append(0.0)
        sidewalk_white.append(1.0)

        sidewalk_white.append(fx(x2))
        sidewalk_white.append(fy(200))
        sidewalk_white.append(0.0)
        sidewalk_white.append(1.0)

        sidewalk_white.append(fx(x1))
        sidewalk_white.append(fy(230))
        sidewalk_white.append(0.0)
        sidewalk_white.append(1.0)

        sidewalk_white.append(fx(x2))
        sidewalk_white.append(fy(230))
        sidewalk_white.append(0.0)
        sidewalk_white.append(1.0)
        x1 += 100
        x2 += 100

    print(road_white)
    for i in range(0, len(road), 4):
        road[i] = fx(road[i])
        road[i+1] = fy(road[i+1])

        sidewalk[i] = fx(sidewalk[i])
        sidewalk[i+1] = fy(sidewalk[i+1])

        
    sidewalk_white = numpy.array(sidewalk_white, dtype=numpy.float32)    
    road_white = numpy.array(road_white, dtype=numpy.float32)
    sidewalk = numpy.array(sidewalk, dtype=numpy.float32)
    road = numpy.array(road, dtype=numpy.float32)
    

def create_object(shader, datas):
    
    # Create a new VAO (Vertex Array Object) and bind it
    vertex_array_object = GL.glGenVertexArrays(1)
    GL.glBindVertexArray( vertex_array_object )
    
    # Generate buffers to hold our vertices
    vertex_buffer = GL.glGenBuffers(1)
    GL.glBindBuffer(GL.GL_ARRAY_BUFFER, vertex_buffer)
    
    # Get the position of the 'position' in parameter of our shader and bind it.
    position = GL.glGetAttribLocation(shader, 'position')
    #GL.glEnableVertexAttribArray(position)
    GL.glEnableVertexAttribArray(position)

    # Describe the position data layout in the buffer
    GL.glVertexAttribPointer(position, 4, GL.GL_FLOAT, False, 0, ctypes.c_void_p(0))
    
    # Send the data over to the buffer
    GL.glBufferData(GL.GL_ARRAY_BUFFER, 4 * len(datas), datas, GL.GL_STATIC_DRAW)
    #GL.glBufferData(GL.GL_ARRAY_BUFFER, 48, vertices2, GL.GL_STATIC_DRAW)
    # Unbind the VAO first (Important)
    GL.glBindVertexArray( 0 )
    
    # Unbind other stuff
    GL.glDisableVertexAttribArray(position)
    GL.glBindBuffer(GL.GL_ARRAY_BUFFER, 0)
    
    return vertex_array_object
    
def display(shader, vertex_array_object):
    global transform_road, transform_sidewalk
    global dR, dG, dB
    global skyColorR, skyColorG, skyColorB
    global skyR, skyG, skyB
    global plus

    GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)

    # sidewalk_white
    GL.glUseProgram(shader[3])

    transLoc = GL.glGetUniformLocation(shader[3], "transform")
    GL.glUniform1f(transLoc, transform_sidewalk)
    transform_sidewalk -= (0.5/800)

    if(transform_sidewalk <= (-1.0-5/800)):
        transform_sidewalk = 0.0

    GL.glBindVertexArray( vertex_array_object[4] )
    GL.glDrawArrays(GL.GL_QUADS, 0, 80)
    GL.glBindVertexArray( 0 )
    GL.glUseProgram(0)

    # road_white
    GL.glUseProgram(shader[3])

    transLoc = GL.glGetUniformLocation(shader[3], "transform")
    GL.glUniform1f(transLoc, transform_road)
    transform_road -= (0.5/800)

    if(transform_road <= (-1.0-160/800)):
        transform_road = 0.0

    GL.glBindVertexArray( vertex_array_object[3] )
    GL.glDrawArrays(GL.GL_QUADS, 0, 40)
    GL.glBindVertexArray( 3 )
    GL.glUseProgram(0)

    # road
    GL.glUseProgram(shader[0])
    GL.glBindVertexArray( vertex_array_object[0] )
    GL.glDrawArrays(GL.GL_POLYGON, 0, 4)
    GL.glBindVertexArray( 0 )
    GL.glUseProgram(0)

    # sidewalk
    GL.glUseProgram(shader[2])
    GL.glBindVertexArray( vertex_array_object[2] )
    GL.glDrawArrays(GL.GL_POLYGON, 0, 4)
    GL.glBindVertexArray( 2 )
    GL.glUseProgram(0)

    # sky
    GL.glUseProgram(shader[1])

    redLoc = GL.glGetUniformLocation(shader[1], "r")
    greenLoc = GL.glGetUniformLocation(shader[1], "g")
    blueLoc = GL.glGetUniformLocation(shader[1], "b")

    if(skyR < skyColorR) and (plus):
        skyR = skyR + dR
        skyG = skyG + dG
        skyB = skyB + dB
        GL.glUniform1f(redLoc, -skyR)
        GL.glUniform1f(greenLoc, -skyG)
        GL.glUniform1f(blueLoc, -skyB)
        if (skyR >= skyColorR):
            plus = False
    else:
        skyR = skyR - dR
        skyG = skyG - dG
        skyB = skyB - dB
        GL.glUniform1f(redLoc, -skyR)
        GL.glUniform1f(greenLoc, -skyG)
        GL.glUniform1f(blueLoc, -skyB)
        if (skyR <= skyDarkR):
            plus = True

    GL.glBindVertexArray( vertex_array_object[1] )
    GL.glDrawArrays(GL.GL_POLYGON, 0, 4)
    GL.glBindVertexArray( 1 )
    GL.glUseProgram(0)

def main():
    global background, sidewalk, road, transform_sidewalk

    convert_coordinate()
    pygame.init()
    screen = pygame.display.set_mode((800, 600), pygame.OPENGL|pygame.DOUBLEBUF)
    GL.glClearColor(0.5, 0.5, 0.5, 1.0)
    GL.glEnable(GL.GL_DEPTH_TEST)

    shader_road = OpenGL.GL.shaders.compileProgram(
        OpenGL.GL.shaders.compileShader(vertex_shader, GL.GL_VERTEX_SHADER),
        OpenGL.GL.shaders.compileShader(fragment_shader_road, GL.GL_FRAGMENT_SHADER)
    )

    shader_road_white = OpenGL.GL.shaders.compileProgram(
        OpenGL.GL.shaders.compileShader(vertex_shader_road, GL.GL_VERTEX_SHADER),
        OpenGL.GL.shaders.compileShader(fragment_shader_white, GL.GL_FRAGMENT_SHADER)
    )

    shader_sidewalk = OpenGL.GL.shaders.compileProgram(
        OpenGL.GL.shaders.compileShader(vertex_shader, GL.GL_VERTEX_SHADER),
        OpenGL.GL.shaders.compileShader(fragment_shader_sidewalk, GL.GL_FRAGMENT_SHADER)
    )

    shader_sky = OpenGL.GL.shaders.compileProgram(
        OpenGL.GL.shaders.compileShader(vertex_shader, GL.GL_VERTEX_SHADER),
        OpenGL.GL.shaders.compileShader(fragment_shader_sky, GL.GL_FRAGMENT_SHADER)
    )

    shaders = []
    shaders.append(shader_road)
    shaders.append(shader_sky)
    shaders.append(shader_sidewalk)
    shaders.append(shader_road_white)

    clock = pygame.time.Clock()
    vertex_array_object = []
    vertex_array_object.append(create_object(shader_road, road))
    vertex_array_object.append(create_object(shader_sky, background))
    vertex_array_object.append(create_object(shader_sidewalk, sidewalk))
    vertex_array_object.append(create_object(shader_road_white, road_white))     
    vertex_array_object.append(create_object(shader_road_white, sidewalk_white))

    while True:
        

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE:
                return
        
        display(shaders, vertex_array_object)
        # vertices[0] += 0.001
        # vertices2[4] -= 0.001
        
        pygame.display.flip()

if __name__ == '__main__':
    try:
        main()
    finally:
        pygame.quit()