import OpenGL.GL as GL
import OpenGL.GL.shaders
from OpenGL.GLU import *
from OpenGL.GLUT import *
from math import *
import ctypes
import pygame
import numpy
from math import *

spokes1_offset_x = (150-400)/400
spokes1_offset_y = (190-300)/300

spokes2_offset_x = -20/400
spokes2_offset_y = -110/300

wheel_rotation_deg = 0

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
skyDarkG = 80/255
skyDarkB = 73/255

skyR = 109/255
skyG = 238/255
skyB = 255/255

plus = False

dR = (- skyDarkR + skyColorR)/10000
dG = (- skyDarkG + skyColorG)/10000
dB = (- skyDarkB + skyColorB)/10000

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

vertex_shader_spoke = """
#version 330

layout (location = 0) in vec4 position;
layout (location = 1) in vec2 aTexCoord;
uniform float sina, cosa, offsetX, offsetY;
out vec2 TexCoord;

void main()
{   
   gl_Position = vec4((position.x * cosa + position.y * sina) + offsetX, (position.x * (-sina) + position.y * cosa) + offsetY, 0.0, 1.0);
   TexCoord = vec2(aTexCoord.x, aTexCoord.y);
}
"""

fragment_shader_outerWheel = """
#version 330

void main()
{
    gl_FragColor = vec4(65.0f/255.0f,65.0f/255.0f,65.0f/255.0f, 1.0f);
}
"""

fragment_shader_window = """
#version 330

void main()
{
   gl_FragColor = vec4(0.0f,198.0f/255.0f,255.0f/255.0f, 1.0f);
}
"""

fragment_shader_car = """
#version 330
void main()
{
   gl_FragColor = vec4(219.0f/255.0f,24.0f/255.0f,76.0f/255.0f, 1.0f);
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
   gl_FragColor = vec4(109.0f/255.0f + r, 238.0f/255.0f + g, 255.0f/255.0f + b, 1.0f);
}
"""

fragment_shader_sidewalk = """
#version 330
void main()
{
   gl_FragColor = vec4(0.0f, 0.0f, 0.0f, 1.0f);
}
"""

fragment_shader_properties = """
#version 330
void main()
{
   gl_FragColor = vec4(15.0f/255.0f,15.0f/255.0f,15.0f/255.0f,1.0f);
}
"""

fragment_shader_foot_step = """
#version 330
void main()
{
   gl_FragColor = vec4(0.06f, 0.06f, 0.06f, 1.0f);
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

rightWheel = []
innerRight = []
leftWheel = []
innerLeft = []    
inRightWheel = []
inLeftWheel = []
inInnerRight = []
inInnerLeft = []

properties = [100.0, 220.0, 0.0, 1.0,
            100.0, 200.0, 0.0, 1.0,
            520.0, 200.0, 0.0, 1.0,
            510.0, 220.0, 0.0, 1.0]

background = [-1.0, 1.0, 0.0, 1.0,
              1.0, 1.0, 0.0, 1.0,
              1.0, -1.0, 0.0, 1.0,
              -1.0, -1.0, 0.0, 1.0]
car = [80.0, 330.0, 0.0, 1.0,
        340.0, 330.0,  0.0, 1.0,
        450.0, 180.0,  0.0, 1.0,
        60.0, 180.0,  0.0, 1.0, 
        60.0, 250.0, 0.0, 1.0]    

carFront = [ 350,270, 0.0, 1.0,
            490,250, 0.0, 1.0,
            510,210,0.0, 1.0,
            510,180,0.0, 1.0,
            350,180, 0.0, 1.0
            ]

carFootStep = [100.0, 220.0, 0.0, 1.0,
				100.0, 200.0, 0.0, 1.0,
				520.0, 200.0, 0.0, 1.0,
				510.0, 220.0, 0.0, 1.0,]

window_1 =[ 76,320, 0.0 , 1.0,
            65,270, 0.0, 1.0,
            92,270, 0.0, 1.0,
            103,320, 0.0, 1.0
        ]
            
window_2 = [110,320, 0.0, 1.0,
            99,270, 0.0, 1.0,
            205,270, 0.0, 1.0,
            210,320, 0.0, 1.0]
            
window_3 = [215,320, 0.0, 1.0,
            220,270, 0.0, 1.0,
            321,270, 0.0, 1.0,
            310,320, 0.0, 1.0]
            
window_4 = [320,320, 0.0, 1.0,
            331,270, 0.0, 1.0,
            390,270, 0.0, 1.0,
            350,320, 0.0, 1.0]

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

spokes = [-80.0, 5.0, 0.0, 1.0,
        -80.0, -5.0, 0.0, 1.0,
        80.0, -5.0, 0.0, 1.0,
        80.0, 5.0, 0.0, 1.0,
        -6.0, 60.0, 0.0, 1.0,
        -6.0, -60.0, 0.0, 1.0,
        6.0, -60.0, 0.0, 1.0,
        6.0, 60.0, 0.0, 1.0]

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
    global road, sidewalk, road_white, sidewalk_white, car, carFront, carFootStep
    global window_1, window_2, window_3, window_4
    global rightWheel, leftWheel, innerRight, innerLeft, inLeftWheel, inRightWheel, inInnerRight, inInnerLeft
    global spokes, properties
    global x_road1, x_road2

    #Inner_InnerWheel
    for i in range(100):    
        cosine = 15 * cos(i*2*pi/32) + 380
        sine = 15 * sin(i*2*pi/32) + 190
        inInnerRight.append(fx(cosine))
        inInnerRight.append(fy(sine))
        inInnerRight.append(0.0)
        inInnerRight.append(1.0)
    
    for i in range(100):    
        cosine = 15 * cos(i*2*pi/32) + 150
        sine = 15 * sin(i*2*pi/32) + 190
        inInnerLeft.append(fx(cosine))
        inInnerLeft.append(fy(sine))
        inInnerLeft.append(0.0)
        inInnerLeft.append(1.0)
    
    #Outer_InnerWheel
    for i in range(100):    
        cosine = 20 * cos(i*2*pi/32) + 380
        sine = 20 * sin(i*2*pi/32) + 190
        inRightWheel.append(fx(cosine))
        inRightWheel.append(fy(sine))
        inRightWheel.append(0.0)
        inRightWheel.append(1.0)
    
    for i in range(100):    
        cosine = 20 * cos(i*2*pi/32) + 150
        sine = 20 * sin(i*2*pi/32) + 190
        inLeftWheel.append(fx(cosine))
        inLeftWheel.append(fy(sine))
        inLeftWheel.append(0.0)
        inLeftWheel.append(1.0)
    
    #Inner Wheel
    for i in range(0, 100):
        cosine = 30 * cos(i*2*pi/32) + 380
        sine = 30 * sin(i*2*pi/32) + 190
        innerRight.append(fx(cosine))
        innerRight.append(fy(sine))
        innerRight.append(0.0)
        innerRight.append(1.0)
        
    for i in range(0, 100):
        cosine = 30 * cos(i*2*pi/32) + 150
        sine = 30 * sin(i*2*pi/32) + 190
        innerLeft.append(fx(cosine))
        innerLeft.append(fy(sine))
        innerLeft.append(0.0)
        innerLeft.append(1.0)
    
    #Outer Wheel
    for i in range(0, 100):
        cosine = 40 * cos(i*2*pi/32) + 380
        sine = 40 * sin(i*2*pi/32) + 190
        rightWheel.append(fx(cosine))
        rightWheel.append(fy(sine))
        rightWheel.append(0.0)
        rightWheel.append(1.0)
        
    for i in range(0, 100):
        cosine = 40 * cos(i*2*pi/32) + 150
        sine = 40 * sin(i*2*pi/32) + 190
        leftWheel.append(fx(cosine))
        leftWheel.append(fy(sine))
        leftWheel.append(0.0)
        leftWheel.append(1.0)

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

        road_white.append(fx(x2))
        road_white.append(fy(130))
        road_white.append(0.0)
        road_white.append(1.0)

        road_white.append(fx(x1))
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

        sidewalk_white.append(fx(x2))
        sidewalk_white.append(fy(230))
        sidewalk_white.append(0.0)
        sidewalk_white.append(1.0)

        sidewalk_white.append(fx(x1))
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

    for i in range(0, len(car), 4):
        car[i] = fx(car[i])
        car[i+1] = fy(car[i+1])
        
        carFront[i] = fx(carFront[i])
        carFront[i+1] = fy(carFront[i+1])

    for i in range(0, len(carFootStep),4):
	    carFootStep[i] = fx(carFootStep[i])
	    carFootStep[i+1] = fy(carFootStep[i+1])
        
    for i in range(0,len(window_1), 4):
        window_1[i] = fx(window_1[i])
        window_1[i+1] = fy(window_1[i+1])
        
        window_2[i] = fx(window_2[i])
        window_2[i+1] = fy(window_2[i+1])
        
        window_3[i] = fx(window_3[i])
        window_3[i+1] = fy(window_3[i+1])
        
        window_4[i] = fx(window_4[i])
        window_4[i+1] = fy(window_4[i+1])

    for i in range(0, len(spokes), 4):
        spokes[i] = spokes[i]/800.0
        spokes[i+1] = spokes[i+1]/600.0
    
    sidewalk_white = numpy.array(sidewalk_white, dtype=numpy.float32)    
    road_white = numpy.array(road_white, dtype=numpy.float32)
    sidewalk = numpy.array(sidewalk, dtype=numpy.float32)
    road = numpy.array(road, dtype=numpy.float32)
    car = numpy.array(car, dtype=numpy.float32)
    carFront = numpy.array(carFront, dtype=numpy.float32)
    carFootStep = numpy.array(carFootStep, dtype=numpy.float32)
    window_1= numpy.array(window_1, dtype=numpy.float32)
    window_2= numpy.array(window_2, dtype=numpy.float32)
    window_3= numpy.array(window_3, dtype=numpy.float32)
    window_4= numpy.array(window_4, dtype=numpy.float32)
    spokes = numpy.array(spokes, dtype=numpy.float32)
    rightWheel = numpy.array(rightWheel, dtype=numpy.float32)
    leftWheel = numpy.array(leftWheel, dtype=numpy.float32)
    innerLeft = numpy.array(innerLeft, dtype=numpy.float32)
    innerRight = numpy.array(innerRight, dtype=numpy.float32)
    inRightWheel = numpy.array(inRightWheel, dtype=numpy.float32)
    inLeftWheel = numpy.array(inLeftWheel, dtype=numpy.float32)
    inInnerRight = numpy.array(inInnerRight, dtype=numpy.float32)
    inInnerLeft = numpy.array(inInnerLeft, dtype=numpy.float32)
    properties = numpy.array(properties, dtype=numpy.float32)

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
    global transform_road, transform_sidewalk, wheel_rotation_deg
    global dR, dG, dB
    global skyColorR, skyColorG, skyColorB
    global skyR, skyG, skyB
    global plus

    GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)
    GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)

    #Inner_InnerWheel
    GL.glUseProgram(shader[8])
    GL.glBindVertexArray( vertex_array_object[19] )
    GL.glDrawArrays(GL.GL_POLYGON, 0, 100)
    GL.glBindVertexArray( 19 )
    GL.glUseProgram(0)
    
    GL.glUseProgram(shader[8])
    GL.glBindVertexArray( vertex_array_object[18] )
    GL.glDrawArrays(GL.GL_POLYGON, 0, 100)
    GL.glBindVertexArray( 18 )
    GL.glUseProgram(0)

    # spokes
    GL.glUseProgram(shader[10])
    
    sinLoc = GL.glGetUniformLocation(shader[10], "sina")
    cosLoc = GL.glGetUniformLocation(shader[10], "cosa")
    offsetXLoc = GL.glGetUniformLocation(shader[10], "offsetX")
    offsetYLoc = GL.glGetUniformLocation(shader[10], "offsetY")
    
    sine = sin(wheel_rotation_deg * 2 * pi/32)
    cosine = cos(wheel_rotation_deg * 2 * pi/32)
    GL.glUniform1f(sinLoc, sine)
    GL.glUniform1f(cosLoc, cosine)
    GL.glUniform1f(offsetXLoc, spokes1_offset_x)
    GL.glUniform1f(offsetYLoc, spokes1_offset_y)

    GL.glBindVertexArray( vertex_array_object[21] )
    GL.glDrawArrays(GL.GL_QUADS, 0, 8)
    GL.glBindVertexArray(0)
    GL.glUseProgram(0)

    GL.glUseProgram(shader[10])
    sinLoc = GL.glGetUniformLocation(shader[10], "sina")
    cosLoc = GL.glGetUniformLocation(shader[10], "cosa")
    offsetXLoc = GL.glGetUniformLocation(shader[10], "offsetX")
    offsetYLoc = GL.glGetUniformLocation(shader[10], "offsetY")
    
    sine = sin(wheel_rotation_deg * 2 * pi/32)
    cosine = cos(wheel_rotation_deg * 2 * pi/32)
    GL.glUniform1f(sinLoc, sine)
    GL.glUniform1f(cosLoc, cosine)
    GL.glUniform1f(offsetXLoc, spokes2_offset_x)
    GL.glUniform1f(offsetYLoc, spokes2_offset_y)
    wheel_rotation_deg = 0 if (wheel_rotation_deg >= 360) else (wheel_rotation_deg + 0.02)

    GL.glBindVertexArray( vertex_array_object[21] )
    GL.glDrawArrays(GL.GL_QUADS, 0, 8)
    GL.glBindVertexArray(0)
    GL.glUseProgram(0)
    
    #Inner_OuterWheel
    GL.glUseProgram(shader[7])
    GL.glBindVertexArray( vertex_array_object[17] )
    GL.glDrawArrays(GL.GL_POLYGON, 0, 100)
    GL.glBindVertexArray( 17 )
    GL.glUseProgram(0)
    
    GL.glUseProgram(shader[7])
    GL.glBindVertexArray( vertex_array_object[16] )
    GL.glDrawArrays(GL.GL_POLYGON, 0, 100)
    GL.glBindVertexArray( 16 )
    GL.glUseProgram(0)
    
    #Inner Wheel
    GL.glUseProgram(shader[8])
    GL.glBindVertexArray( vertex_array_object[15] )
    GL.glDrawArrays(GL.GL_POLYGON, 0, 100)
    GL.glBindVertexArray( 15 )
    GL.glUseProgram(0)
    
    GL.glUseProgram(shader[8])
    GL.glBindVertexArray( vertex_array_object[14] )
    GL.glDrawArrays(GL.GL_POLYGON, 0, 100)
    GL.glBindVertexArray( 14 )
    GL.glUseProgram(0)
    
    # Wheel
    GL.glUseProgram(shader[7])
    GL.glBindVertexArray( vertex_array_object[13] )
    GL.glDrawArrays(GL.GL_POLYGON, 0, 100)
    GL.glBindVertexArray( 13 )
    GL.glUseProgram(0)
    
    GL.glUseProgram(shader[7])
    GL.glBindVertexArray( vertex_array_object[12] )
    GL.glDrawArrays(GL.GL_POLYGON, 0, 100)
    GL.glBindVertexArray( 12 )
    GL.glUseProgram(0)
    
    # Properties
    GL.glUseProgram(shader[9])
    GL.glBindVertexArray( vertex_array_object[20] )
    GL.glDrawArrays(GL.GL_POLYGON, 0, 4)
    GL.glBindVertexArray( 20 )
    GL.glUseProgram(0)

    # Car Foot Step
    GL.glUseProgram(shader[5])
    GL.glBindVertexArray( vertex_array_object[7] )
    GL.glDrawArrays(GL.GL_POLYGON, 0, 4)
    GL.glBindVertexArray( 7 )
    GL.glUseProgram(0)

    # windows
    GL.glUseProgram(shader[6])
    GL.glBindVertexArray( vertex_array_object[11] )
    GL.glDrawArrays(GL.GL_POLYGON, 0, 4)
    GL.glBindVertexArray( 11 )
    GL.glUseProgram(0)
    
    GL.glUseProgram(shader[6])
    GL.glBindVertexArray( vertex_array_object[10] )
    GL.glDrawArrays(GL.GL_POLYGON, 0, 4)
    GL.glBindVertexArray( 10 )
    GL.glUseProgram(0)
    
    GL.glUseProgram(shader[6])
    GL.glBindVertexArray( vertex_array_object[9] )
    GL.glDrawArrays(GL.GL_POLYGON, 0, 4)
    GL.glBindVertexArray( 9 )
    GL.glUseProgram(0)
    
    GL.glUseProgram(shader[6])
    GL.glBindVertexArray( vertex_array_object[8] )
    GL.glDrawArrays(GL.GL_POLYGON, 0, 4)
    GL.glBindVertexArray( 8 )
    GL.glUseProgram(0)
    
    GL.glUseProgram(shader[4])
    GL.glBindVertexArray( vertex_array_object[6] )
    GL.glDrawArrays(GL.GL_POLYGON, 0, 5)
    GL.glBindVertexArray( 6 )
    GL.glUseProgram(0)
    #car
    GL.glUseProgram(shader[4])
    GL.glBindVertexArray( vertex_array_object[5] )
    GL.glDrawArrays(GL.GL_POLYGON, 0, 5)
    GL.glBindVertexArray( 5 )
    GL.glUseProgram(0)
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
    
    shader_car = OpenGL.GL.shaders.compileProgram(
        OpenGL.GL.shaders.compileShader(vertex_shader, GL.GL_VERTEX_SHADER),
        OpenGL.GL.shaders.compileShader(fragment_shader_car, GL.GL_FRAGMENT_SHADER)
    )

    shader_car_footstep = OpenGL.GL.shaders.compileProgram(
        OpenGL.GL.shaders.compileShader(vertex_shader, GL.GL_VERTEX_SHADER),
        OpenGL.GL.shaders.compileShader(fragment_shader_foot_step, GL.GL_FRAGMENT_SHADER)
    )

    shader_spokes = OpenGL.GL.shaders.compileProgram(
        OpenGL.GL.shaders.compileShader(vertex_shader_spoke, GL.GL_VERTEX_SHADER),
        OpenGL.GL.shaders.compileShader(fragment_shader_outerWheel, GL.GL_FRAGMENT_SHADER)
    )
    
    shader_window = OpenGL.GL.shaders.compileProgram(
        OpenGL.GL.shaders.compileShader(vertex_shader, GL.GL_VERTEX_SHADER),
        OpenGL.GL.shaders.compileShader(fragment_shader_window, GL.GL_FRAGMENT_SHADER)
    )
    
    shader_outerWheel = OpenGL.GL.shaders.compileProgram(
        OpenGL.GL.shaders.compileShader(vertex_shader, GL.GL_VERTEX_SHADER),
        OpenGL.GL.shaders.compileShader(fragment_shader_outerWheel, GL.GL_FRAGMENT_SHADER)
    )
    
    shader_innerWheel = OpenGL.GL.shaders.compileProgram(
        OpenGL.GL.shaders.compileShader(vertex_shader, GL.GL_VERTEX_SHADER),
        OpenGL.GL.shaders.compileShader(fragment_shader_white, GL.GL_FRAGMENT_SHADER)
    )
    
    shader_properties = OpenGL.GL.shaders.compileProgram(
        OpenGL.GL.shaders.compileShader(vertex_shader, GL.GL_VERTEX_SHADER),
        OpenGL.GL.shaders.compileShader(fragment_shader_properties, GL.GL_FRAGMENT_SHADER)
    )

    shaders = []
    shaders.append(shader_road)
    shaders.append(shader_sky)
    shaders.append(shader_sidewalk)
    shaders.append(shader_road_white)
    shaders.append(shader_car)
    shaders.append(shader_car_footstep)
    shaders.append(shader_window)
    shaders.append(shader_outerWheel)
    shaders.append(shader_innerWheel)
    shaders.append(shader_properties)
    shaders.append(shader_spokes)

    clock = pygame.time.Clock()
    vertex_array_object = []
    vertex_array_object.append(create_object(shader_road, road))
    vertex_array_object.append(create_object(shader_sky, background))
    vertex_array_object.append(create_object(shader_sidewalk, sidewalk))
    vertex_array_object.append(create_object(shader_road_white, road_white))     
    vertex_array_object.append(create_object(shader_road_white, sidewalk_white))
    vertex_array_object.append(create_object(shader_car, car))
    vertex_array_object.append(create_object(shader_car, carFront))
    vertex_array_object.append(create_object(shader_car_footstep, carFootStep))
    vertex_array_object.append(create_object(shader_window, window_1))
    vertex_array_object.append(create_object(shader_window, window_2))
    vertex_array_object.append(create_object(shader_window, window_3))
    vertex_array_object.append(create_object(shader_window, window_4))
    vertex_array_object.append(create_object(shader_outerWheel,    rightWheel))
    vertex_array_object.append(create_object(shader_outerWheel,    leftWheel))
    vertex_array_object.append(create_object(shader_innerWheel,    innerRight))
    vertex_array_object.append(create_object(shader_innerWheel,    innerLeft))
    vertex_array_object.append(create_object(shader_outerWheel,    inRightWheel))
    vertex_array_object.append(create_object(shader_outerWheel,    inLeftWheel))
    vertex_array_object.append(create_object(shader_innerWheel,    inInnerRight))
    vertex_array_object.append(create_object(shader_innerWheel,    inInnerLeft))
    vertex_array_object.append(create_object(shader_properties,    properties))
    vertex_array_object.append(create_object(shader_spokes, spokes))

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