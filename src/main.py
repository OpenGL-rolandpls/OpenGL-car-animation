import sys
from math import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

x_road1 = 0
x_road2 = 80

x_sidewalk1 = 0
x_sidewalk2 = 50

skyColorR = 109/255
skyColorG = 238/255
skyColorB = 255/255

skyDarkR = 13/255
skyDarkG = 13/255
skyDarkB = 73/255

plus = False

dR = (- skyDarkR + skyColorR)/1500
dG = (- skyDarkG + skyColorG)/1500
dB = (- skyDarkB + skyColorB)/1500

skyR = 109/255
skyG = 238/255
skyB = 255/255

wheel = 0
# The display() method does all the work; it has to call the appropriate
# OpenGL functions to actually display something.
def display():
	global x_road1
	global x_road2
	global skyColorR, skyColorG, skyColorB
	global skyR, skyG, skyB
	global skyDarkR, skyDarkG, skyDarkB
	global dR, dG, dB
	global plus
	global x_sidewalk1
	global x_sidewalk2
	global wheel
	
	# Clear the color and depth buffers
	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
	refresh2d(800,600)
	
	# ... render stuff in here ...
	# background
	glColor3f(skyR, skyG, skyB)
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
	
	glColor3f(0/255,198/255,255/255)
	glBegin(GL_POLYGON)
	glVertex2f(74,320)
	glVertex2f(63,270)
	glVertex2f(90,270)
	glVertex2f(90,320)
	glEnd()
	
	glColor3f(0/255,198/255,255/255)
	glBegin(GL_QUADS)
	glVertex2f(76,320)
	glVertex2f(65,270)
	glVertex2f(92,270)
	glVertex2f(103,320)
	
	glVertex2f(110,320)
	glVertex2f(99,270)
	glVertex2f(205,270)
	glVertex2f(210,320)
	
	glVertex2f(215,320)
	glVertex2f(220,270)
	glVertex2f(321,270)
	glVertex2f(310,320)
	
	glVertex2f(320,320)
	glVertex2f(331,270)
	glVertex2f(390,270)
	glVertex2f(350,320)
	glEnd()
	
	glColor3f(15/255,15/255,15/255)
	glBegin(GL_QUADS)
	glVertex2f(100,220)
	glVertex2f(100,200)
	glVertex2f(520,200)
	glVertex2f(510,220)
	glEnd()
	
	#wheel-1 
	glPushMatrix()
	glTranslate(150,190,0)
	glRotated(wheel,0,0,1)
	glColor3f(65/255,65/255,65/255)	
	glBegin(GL_POLYGON)    
	for i in range(100):    
		cosine = 40 * cos(i*2*pi/32)
		sine = 40 * sin(i*2*pi/32)
		glVertex2f(cosine,sine)
	glEnd()
	
	glColor3f(255/255,255/255,255/255)	
	glBegin(GL_POLYGON)    
	for i in range(100):    
		cosine = 30 * cos(i*2*pi/32)
		sine = 30 * sin(i*2*pi/32)
		glVertex2f(cosine,sine)
	glEnd()
	
	glColor3f(65/255,65/255,65/255)
	glBegin(GL_QUADS)
	glVertex2f(-35,3)
	glVertex2f(-35,-3)
	glVertex2f(35,-3)
	glVertex2f(35,3)

	glVertex2f(-3,35)
	glVertex2f(-3,-35)
	glVertex2f(3,-35)
	glVertex2f(3,35)
	glEnd()
	
	glColor3f(65/255,65/255,65/255)	
	glBegin(GL_POLYGON)    
	for i in range(100):    
		cosine = 20 * cos(i*2*pi/32)
		sine = 20 * sin(i*2*pi/32)
		glVertex2f(cosine,sine)
	glEnd()
	
	glColor3f(255/255,255/255,255/255)	
	glBegin(GL_POLYGON)    
	for i in range(100):    
		cosine = 15 * cos(i*2*pi/32)
		sine = 15 * sin(i*2*pi/32)
		glVertex2f(cosine,sine)
	glEnd()
	glPopMatrix()
	
	#wheel-2
	glPushMatrix()
	glTranslate(380,190,0)
	glRotated(wheel,0,0,1)
	glColor3f(65/255,65/255,65/255)	
	glBegin(GL_POLYGON)    
	for i in range(100):    
		cosine = 40 * cos(i*2*pi/32)
		sine = 40 * sin(i*2*pi/32)
		glVertex2f(cosine,sine)
	glEnd()
	
	glColor3f(255/255,255/255,255/255)	
	glBegin(GL_POLYGON)    
	for i in range(100):    
		cosine = 30 * cos(i*2*pi/32)
		sine = 30 * sin(i*2*pi/32)
		glVertex2f(cosine,sine)
	glEnd()
	
	glColor3f(65/255,65/255,65/255)
	glBegin(GL_QUADS)
	glVertex2f(-35,3)
	glVertex2f(-35,-3)
	glVertex2f(35,-3)
	glVertex2f(35,3)

	glVertex2f(-3,35)
	glVertex2f(-3,-35)
	glVertex2f(3,-35)
	glVertex2f(3,35)
	glEnd()
	
	glColor3f(65/255,65/255,65/255)	
	glBegin(GL_POLYGON)    
	for i in range(100):    
		cosine = 20 * cos(i*2*pi/32)
		sine = 20 * sin(i*2*pi/32)
		glVertex2f(cosine,sine)
	glEnd()
	
	glColor3f(255/255,255/255,255/255)	
	glBegin(GL_POLYGON)    
	for i in range(100):    
		cosine = 15 * cos(i*2*pi/32)
		sine = 15 * sin(i*2*pi/32)
		glVertex2f(cosine,sine)
	glEnd()
	glPopMatrix()
	
	# Copy the off-screen buffer to the screen.
	glutSwapBuffers()
	
	if(skyR < skyColorR) and (plus):
		skyR = skyR + dR
		skyG = skyG + dG
		skyB = skyB + dB
		if (skyR == skyColorR):
			plus = False
	else:
		skyR = skyR - dR
		skyG = skyG - dG
		skyB = skyB - dB
		if (skyR < skyDarkR):
			plus = True
	x_road1 = (x_road1 - 0.5)
	if(x_road1 == -160):
		x_road1 = 0
	x_road2 = (x_road2 - 0.5)
	if(x_road2 == -80):
		x_road2 = 80
	x_sidewalk1 = (x_sidewalk1 - 0.5)
	if(x_sidewalk1 == -100):
		x_sidewalk1 = 0
	x_sidewalk2 = (x_sidewalk2 - 0.5)
	if(x_sidewalk2 == -50):
		x_sidewalk2 = 50
	
	wheel -= 0.4
	wheel %= 360
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