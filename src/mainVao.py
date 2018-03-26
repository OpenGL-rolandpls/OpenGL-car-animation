# IF-3260: Computer Graphics
# Vertex Array Objects

#Libraries and Packages
import sys
import OpenGL.GL.shaders
import OpenGL.GL as GL
import ctypes
import pygame
import numpy

from math import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

#Shaders
vShader = """
#version 330
in vec4 position;
void main(){
	gl_Position = position;
}
"""
fShader = """
#version 330
void main()
{
   gl_FragColor = vec4(1.0f, 1.0f, 1.0f, 1.0f);
}
"""

backgroundVertices = [
	0, 0,
	800, 0,
	800, 600,
	0, 600,
]

def createObject(shader, data):
	VAO = glGenVertexArrays(1)
	glBindVertexArray(VAO)
	
	VBO = glGenBuffers(1)
	glBindBuffer(GL_ARRAY_BUFFER, VBO)
	
	position = glGetAttribLocation(shader, 'position')
	glEnableVertexAttribArray(position)
	
	glVertexAttribPointer(position, 4, GL_FLOAT, GL_FALSE, 0, ctypes.c_void_p(0))
	glBufferData(GL_ARRAY_BUFFER, 48, data, GL_STATIC_DRAW)
	glBindVertexArray( 0 )
	
	# Unbind other stuff
	glDisableVertexAttribArray(position)
	glBindBuffer(GL.GL_ARRAY_BUFFER, 0)
	
	return VAO
	
def display(shader, vertex_array_object):
	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
	glUseProgram(shader[0])
	glBindVertexArray( vertex_array_object[0] )
	glDrawArrays(GL_TRIANGLES, 0, 3)
	glBindVertexArray( 0 )
	glUseProgram(0)

	glUseProgram(shader[1])
	glBindVertexArray( vertex_array_object[1] )
	glDrawArrays(GL_TRIANGLES, 0, 3)
	glBindVertexArray( 0 )
	glUseProgram(0)

def main():
	pygame.init()
	screen = pygame.display.set_mode((512, 512), pygame.OPENGL|pygame.DOUBLEBUF)
	GL.glClearColor(0.5, 0.5, 0.5, 1.0)
	GL.glEnable(GL.GL_DEPTH_TEST)

	shader = OpenGL.GL.shaders.compileProgram(
		OpenGL.GL.shaders.compileShader(vShader, GL_VERTEX_SHADER),
		OpenGL.GL.shaders.compileShader(fShader, GL_FRAGMENT_SHADER)
	)

	shaders = []
	shaders.append(shader)
	vertex_array_object = []
	vertex_array_object.append(createObject(shader, backgroundVertices))
	
	while True:
		display(shaders, vertex_array_object)
	
main()
	