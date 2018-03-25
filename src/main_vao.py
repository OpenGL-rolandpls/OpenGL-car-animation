import OpenGL.GL as GL
import glm
import OpenGL.GL.shaders
from OpenGL.GLU import *
from OpenGL.GLUT import *
import ctypes
import pygame
import numpy

transform = 0.0
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
uniform float transform;
out vec2 TexCoord;

void main()
{
   
   gl_Position = vec4(position.x + transform, position.y, 0.0, 1.0);
   TexCoord = vec2(aTexCoord.x, aTexCoord.y);
}
"""

fragment_shader = """
#version 330
void main()
{
   gl_FragColor = vec4(1.0f, 1.0f, 1.0f, 1.0f);
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

background = [-1.0, 1.0, 0.0, 1.0,
              1.0, 1.0, 0.0, 1.0,
              1.0, -1.0, 0.0, 1.0,
              -1.0, -1.0, 0.0, 1.0]

vertices = [ 1,  1, 0.0, 1.0,
            0.0,  0.6, 0.0, 1.0,
             0.0, -0.6, 0.0, 1.0]

vertices2 = [ 0.0,  0.6, 0.0, 1.0,
            -0.6,  0.6, 0.0, 1.0,
             0.0, -0.6, 0.0, 1.0]

background = numpy.array(background, dtype=numpy.float32)			 
vertices = numpy.array(vertices, dtype=numpy.float32)
vertices2 = numpy.array(vertices2, dtype=numpy.float32)

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
    global transform
    global dR, dG, dB
    global skyColorR, skyColorG, skyColorB
    global skyR, skyG, skyB
    global plus

    GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)

    GL.glUseProgram(shader[0])
    
    transLoc = GL.glGetUniformLocation(shader[0], "transform")
    GL.glUniform1f(transLoc, transform)
    transform += 0.0001

    GL.glBindVertexArray( vertex_array_object[0] )
    GL.glDrawArrays(GL.GL_TRIANGLES, 0, 3)
    GL.glBindVertexArray( 0 )
    GL.glUseProgram(0)

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
    GL.glBindVertexArray( 0 )
    GL.glUseProgram(0)
    

def main():
    global vertices2
    global vertices 

    pygame.init()
    screen = pygame.display.set_mode((800, 600), pygame.OPENGL|pygame.DOUBLEBUF)
    GL.glClearColor(0.5, 0.5, 0.5, 1.0)
    GL.glEnable(GL.GL_DEPTH_TEST)

    shader = OpenGL.GL.shaders.compileProgram(
        OpenGL.GL.shaders.compileShader(vertex_shader, GL.GL_VERTEX_SHADER),
        OpenGL.GL.shaders.compileShader(fragment_shader, GL.GL_FRAGMENT_SHADER)
    )

    shader_sky = OpenGL.GL.shaders.compileProgram(
        OpenGL.GL.shaders.compileShader(vertex_shader, GL.GL_VERTEX_SHADER),
        OpenGL.GL.shaders.compileShader(fragment_shader_sky, GL.GL_FRAGMENT_SHADER)
    )
    shaders = []
    shaders.append(shader)
    shaders.append(shader_sky)
    
    clock = pygame.time.Clock()
    
    while True:
        vertex_array_object = []
        vertex_array_object.append(create_object(shader, vertices))
        vertex_array_object.append(create_object(shader_sky, background))     
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