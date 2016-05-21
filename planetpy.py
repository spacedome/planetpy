# Julien Brenneck

from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *
from math import sin, cos, pi, sqrt
import sys
import time
import random


def satellite(size=.1):
    """ Creates a small, blocky satellite out of primitives """
    glPushMatrix()
    glScale(size, size, size)
    glPushMatrix()
    glScale(.01, 1, 1)
    glTranslatef(0, 0, -1.2)
    glutSolidCube(1)
    glTranslatef(0, 0, 2.4)
    glutSolidCube(1)
    glPopMatrix()
    glScale(.5, 1.6, .5)
    glutSolidCube(1)
    glPopMatrix()


starBool = False
starList = glGenLists(0)


def stars(num=50000):
    """
    Creates a displayList of random points, when drawn in
    the solar system function it looks like stars. Includes the sun, as it
    does not move and is more effeciently stored in a displayList
    """
    global starBool
    global starList
    starList = glGenLists(1)
    starBool = True
    glEnable(GL_LIGHTING)
    glNewList(starList, GL_COMPILE)
    # Sun
    glLightfv(GL_LIGHT0, GL_DIFFUSE, (1, 1, 1))
    glLightfv(GL_LIGHT0, GL_POSITION, (0, 10, 0, 1))
    glLightfv(GL_LIGHT0, GL_SPOT_DIRECTION, (0, -1, 0))
    glColor3f(.8, .8, 0)
    glMaterial(GL_FRONT, GL_SPECULAR, [.7, .7, .7, 1])
    glMaterialf(GL_FRONT, GL_SHININESS, 5)
    glMaterialfv(GL_FRONT, GL_EMISSION, [.8, .5, 0, 1])
    glutSolidSphere(1, 25, 25)
    glDisable(GL_LIGHTING)
    glScale(13, 13, 13)
    # Stars
    glBegin(GL_POINTS)
    for i in range(num):
        c = random.random()
        glColor3f(c, c, c)
        u = 2*random.random()-1
        theta = 2*pi*random.random()
        x = sqrt(1-u**2)*cos(theta)
        y = sqrt(1-u**2)*sin(theta)
        glVertex3f(x*(50*random.random()+1),
                   u*(50*random.random()+1),
                   y*(50*random.random()+1))
    glEnd()
    glEnable(GL_LIGHTING)
    glEndList()


orbitBool = False
orbitList = []


def orbits(detail=150):
    """
    Creates a displayList for lines showing planetary oribits.
    specific to these planets.
    """
    global orbitBool
    global orbitList1
    # global orbitList2
    orbitList.append(glGenLists(1))
    orbitBool = True
    glNewList(orbitList[0], GL_COMPILE)
    glDisable(GL_LIGHTING)
    glPushMatrix()
    glBegin(GL_LINES)
    glColor4f(0, .9, .7, .3)
    for i in range(detail):
        glVertex3f(cos(2*pi*i/detail)*3.5+cos(2*pi*i/detail)/2,
                   cos(2*pi*i/detail)*2,
                   sin(2*pi*i/detail)*(-3.5)+cos(2*pi*i/detail)/2)
    glEnd()
    glPopMatrix()
    glColor4f(.9, .4, 0, .5)
    glPushMatrix()
    glBegin(GL_LINES)
    for i in range(detail):
        glVertex3f(sin(2*pi*i/detail)*7+cos(2*pi*i/detail)/4,
                   sin(2*pi*i/detail)/2,
                   cos(2*pi*i/detail)*(-7)+cos(2*pi*i/detail)/4)
    glEnd()
    glPopMatrix()
    glColor4f(1, 1, 1, .2)
    glPushMatrix()
    glBegin(GL_LINES)
    for i in range(detail):
        glVertex3f(cos(2*pi*i/detail)*(-12)+sin(2*pi*i/detail),
                   cos(2*pi*i/detail)/2,
                   sin(2*pi*i/detail)*(-12)+cos(2*pi*i/detail))
    glEnd()
    glPopMatrix()
    glColor4f(1, 1, 1, .2)
    glPushMatrix()
    glRotatef(75, 0, .8, .2)
    glBegin(GL_LINES)
    for i in range(detail):
        glVertex3f(cos(2*pi*i/detail)*(-15)+sin(2*pi*i/detail),
                   cos(2*pi*i/detail)/2,
                   sin(2*pi*i/detail)*(-15)+cos(2*pi*i/detail))
    glEnd()
    glPopMatrix()
    glEnable(GL_LIGHTING)
    glEndList()

    orbitList.append(glGenLists(1))
    glNewList(orbitList[1], GL_COMPILE)
    glDisable(GL_LIGHTING)
    glPushMatrix()
    glBegin(GL_LINES)
    glColor4f(.9, .9, .9, .3)
    for i in range(detail/3):
        glVertex3f(1*cos(2*pi*i/detail*3), 0, 1*sin(2*pi*i/detail*3))
    glEnd()
    glPopMatrix()
    glEnable(GL_LIGHTING)
    glEndList()

    orbitList.append(glGenLists(1))
    glNewList(orbitList[2], GL_COMPILE)
    glDisable(GL_LIGHTING)
    glPushMatrix()
    glBegin(GL_LINES)
    glColor4f(.1, .5, 1, .3)
    for i in range(detail/3):
        glVertex3f(1.2*cos(2*pi*i/detail*3), 0, 1.2*sin(2*pi*i/detail*3))
    glEnd()
    glPopMatrix()
    glEnable(GL_LIGHTING)
    glEndList()


frameCnt = 0
startTime = -1
lastFrameTime = 0
angle = 0


def display():
    """
    GL Display function that draws the solar system. Planets/moons aren't in
    seperate classes because I used slightly different math for each one,
    but satellites are. The planets have fake eliptical oribits,
    and different materials. The lighting is moved for each
    planet to fake illumination from the sun.
    """
    global frameCnt
    global startTime
    global lastFrameTime
    global angle

    curTime = time.time()
    if startTime < 0:
        startTime = curTime
        lastFrameTime = startTime

    frameCnt += 1
    # if(frameCnt % 1000 == 0):
    #     elapsedSecsSinceStart = time.time() - startTime
    #     fps = frameCnt / elapsedSecsSinceStart
    #     print "FPS:", fps
    elapsedTime = curTime - lastFrameTime

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, 16 / float(9), 0.01, 1000)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(10*cos(angle), 3*cos(angle)+3, 10*sin(angle), 0, 0, 0, 0, 1, 0)

    glLightfv(GL_LIGHT0, GL_POSITION, (0, 0, 0, 1))
    glMaterialfv(GL_FRONT, GL_EMISSION, [0, 0, 0, 1])

    # Planet 1
    glLightfv(GL_LIGHT0, GL_SPOT_DIRECTION, (cos(angle), 0, sin(angle)))
    glPushMatrix()
    glTranslatef(cos(angle)*3.5+cos(angle)/2,
                 cos(angle)*2,
                 sin(angle)*(-3.5)+cos(angle)/2)
    glPushMatrix()
    glRotatef(angle*300, 0, 1, 0)
    glColor3f(0, .2, .2)
    glutSolidSphere(.4, 25, 25)
    glPopMatrix()
    # Moon (Same side will always face planet, just like real moon)
    glPushMatrix()
    glRotatef(-angle*360, 0, 1, 0)
    if(orbitBool):
        glCallList(orbitList[1])
    glTranslatef(.7, 0, .7)
    glColor3f(.2, .2, .2)
    glutSolidSphere(.15, 10, 10)
    glPopMatrix()
    # Low Oribit Satellite
    glPushMatrix()
    glRotatef(30, 0, .5, .5)
    glRotatef(-angle*1000, 0, 1, 0)
    if(orbitBool):
        glPushMatrix()
        glScale(.5, .5, .5)
        glCallList(orbitList[1])
        glPopMatrix()
    glTranslatef(.35, 0, .35)
    glColor3f(.3, .3, .3)
    satellite(.04)
    glPopMatrix()
    glPushMatrix()
    glRotatef(-angle*1100-100, 0, 1, 0)
    glTranslatef(.35, 0, .35)
    glColor3f(.01, .01, .01)
    satellite(.03)
    glPopMatrix()
    # End Planet 1
    glPopMatrix()

    glMaterial(GL_FRONT, GL_SPECULAR, [0, 0, 0, 1])

    # Planet 2
    glLightfv(GL_LIGHT0, GL_SPOT_DIRECTION, (sin(angle), 0, cos(angle)))
    glPushMatrix()
    glTranslatef(sin(angle*1.5)*7+cos(angle*1.5)/4,
                 sin(angle*1.5)/2,
                 cos(angle*1.5)*(-7)+cos(angle*1.5)/4)
    glPushMatrix()
    glRotatef(angle*180, 0, 1, 0)
    glColor3f(.3, 0, 0)
    glutSolidSphere(.65, 25, 25)
    glPopMatrix()
    # Moon (Same side will always face planet, just like real moon)
    glPushMatrix()
    glMaterial(GL_FRONT, GL_SPECULAR, [.3, .1, .3, 1])
    glRotatef(40, 1, 0, 1)
    glRotatef(angle*360, 0, 1, 0)
    if(orbitBool):
        glCallList(orbitList[2])
    glTranslatef(.8, 0, .8)
    glColor3f(.25, .35, .6)
    glutSolidSphere(.3, 15, 15)
    # Low Oribit Satellite
    glPushMatrix()
    glMaterial(GL_FRONT, GL_SPECULAR, [.7, .7, .7, 1])
    glRotatef(50, 0, .5, .5)
    glRotatef(-angle*1000, 0, 1, 0)
    if(orbitBool):
        glPushMatrix()
        glScale(.5, .5, .5)
        glCallList(orbitList[1])
        glPopMatrix()
    glTranslatef(.35, 0, .35)
    glColor3f(.3, .3, .3)
    satellite(.04)
    glPopMatrix()
    glPopMatrix()
    # End Planet 2
    glPopMatrix()

    # Extra Planets
    glPushMatrix()
    glLightfv(GL_LIGHT0, GL_SPOT_DIRECTION,
              (cos(2*angle+15), 0, sin(2*angle+15)))
    glTranslatef(cos(2*angle)*(-12)+sin(2*angle),
                 cos(2*angle)/2,
                 sin(2*angle)*(-12)+cos(2*angle))
    glRotatef(angle*300, 0, 1, 0)
    glColor3f(.2, .2, .2)
    glutSolidSphere(.2, 8, 8)
    glPopMatrix()
    glPushMatrix()
    glLightfv(GL_LIGHT0, GL_SPOT_DIRECTION,
              (cos(2*angle+45), 0, sin(2*angle+45)))
    glRotatef(75, 0, .8, .2)
    glTranslatef(cos(2.5*angle)*(-15)+sin(2.5*angle),
                 cos(2.5*angle)/2,
                 sin(2.5*angle)*(-15)+cos(2.5*angle))
    glRotatef(angle * 300, 0, 1, 0)
    glColor3f(.01, .01, .01)
    glutSolidSphere(.25, 8, 8)
    glPopMatrix()
    # End Extra Planets

    if(orbitBool):
        glCallList(orbitList[0])
    if(starBool):
        glCallList(starList)

    glutSwapBuffers()
    lastFrameTime = curTime
    angle += elapsedTime / 3


def drawSolarSystem():
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGBA | GLUT_DEPTH)
    glutInitWindowSize(1280, 720)
    glutCreateWindow("PlanetPy")
    glClearColor(0, 0, 0, 1)

    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    glEnable(GL_CULL_FACE)

    glEnable(GL_POLYGON_SMOOTH)
    glEnable(GL_LINE_SMOOTH)
    glHint(GL_POLYGON_SMOOTH_HINT, GL_NICEST)
    glHint(GL_POINT_SMOOTH_HINT, GL_FASTEST)

    glEnable(GL_DEPTH_TEST)
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_COLOR_MATERIAL)

    stars()
    orbits()
    glutDisplayFunc(display)
    glutIdleFunc(display)
    glutMainLoop()


if __name__ == "__main__":
    drawSolarSystem()
