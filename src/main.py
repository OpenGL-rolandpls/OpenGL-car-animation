import sys
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

x_road1 = 0
x_road2 = 80

x_sidewalk1 = 0
x_sidewalk2 = 50

# The display() method does all the work; it has to call the appropriate
# OpenGL functions to actually display something.
def display():
	global x_road1
	global x_road2

	global x_sidewalk1
	global x_sidewalk2
	
	# Clear the color and depth buffers
	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
	refresh2d(800,600)
	
	# ... render stuff in here ...
	# background
	glColor3f(109/255,238/255,255/255)
	glBegin(GL_POLYGON)
	glVertex2f(0,0)
	glVertex2f(800,0)
	glVertex2f(800,600)
	glVertex2f(0,600)
	glEnd()

	# jalan
	glColor3f(61/255,61/255,61/255)
	glBegin(GL_POLYGON)
	glVertex2f(0,200)
	glVertex2f(800,200)
	glVertex2f(800,0)
	glVertex2f(0,0)
	glEnd()

	x1 = x_road1
	x2 = x_road2
	for i in range(0,20):
		glColor3f(1,1,1)
		glBegin(GL_POLYGON)
		glVertex2f(x1,100)
		glVertex2f(x2,100)
		glVertex2f(x2,130)
		glVertex2f(x1,130)
		glEnd()
		x1 += 160
		x2 += 160

	# trotoar
	glColor3f(0,0,0)
	glBegin(GL_POLYGON)
	glVertex2f(0,200)
	glVertex2f(800,200)
	glVertex2f(800,230)
	glVertex2f(0,230)
	glEnd()

	x1 = x_sidewalk1
	x2 = x_sidewalk2
	for i in range(0,20):
		glColor3f(1,1,1)
		glBegin(GL_POLYGON)
		glVertex2f(x1,200)
		glVertex2f(x2,200)
		glVertex2f(x2,230)
		glVertex2f(x1,230)
		glEnd()
		x1 += 100
		x2 += 100

	# badan mobil
	glColor3f(219/255,24/255,76/255)
	glBegin(GL_POLYGON)
	glVertex2f(80,330)
	glVertex2f(340,330)
	glVertex2f(450,180)
	glVertex2f(60,180)
	glVertex2f(60,250)
	glEnd()

	glColor3f(219/255,24/255,76/255)
	glBegin(GL_POLYGON)
	glVertex2f(350,270)
	glVertex2f(490,250)
	glVertex2f(510,210)
	glVertex2f(510,180)
	glVertex2f(350,180)
	glEnd()
	# Copy the off-screen buffer to the screen.
	glutSwapBuffers()
	
	x_road1 = (x_road1 + 0.5)%80
	x_road2 = (x_road2 + 0.5)%160
	
	glutPostRedisplay()

def refresh2d(width, height):
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0.0, width, 0.0, height, 0.0, 1.0)
    glMatrixMode (GL_MODELVIEW)
    glLoadIdentity()	
	
glutInit()
glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)

glutInitWindowSize(800,600)
glutInitWindowPosition(100,100)
glutCreateWindow(b'Happy Car')

glutDisplayFunc(display)

glutMainLoop()