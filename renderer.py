import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

def Cube():
    glBegin(GL_LINES)
    glVertex3fv((1,1,1))
    glVertex3fv((1,1,-1))
    glVertex3fv((1,-1,-1))
    glEnd()

def main():
    pygame.init()
    display = (800,600)
    pygame.display.set_mode(display, DOUBLEBUF|OPENGL)

    glEnable(GL_DEPTH_TEST)
    glDepthFunc(GL_LESS)

    glMatrixMode(GL_PROJECTION)
    gluPerspective(45, (display[0]/display[1]), 0.1, 50.0)

    
    glMatrixMode(GL_MODELVIEW)
    glTranslatef(0.0,0.0,-5)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        glRotatef(1,3,1,1)
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        
        c = Cublet()
        c.draw()
        pygame.display.flip()
        pygame.time.wait(10)


class Cublet :

    """
    
          +y
           0 +x
        +z

    """

    """
                     | cos  -sin       |
        R_z(theta) = | sin   cos       |
                     |              1  |
        
                     |  cos        sin |
        R_y(theta) = |        1        |
                     | -sin        cos |
        
                     |   1             |
        R_x(theta) = |       cos  -sin |
                     |       sin   cos |
    """

    def __init__ ( self ) :
        self.pos = [0, 0, 0]

    def draw ( self ) :
        glPushMatrix()
        glTranslatef(*self.pos)
        glBegin(GL_QUADS)

        # Top green
        glColor3f(0.0, 1.0, 0.0)
        glVertex3f(1.0, 1.0, -1.0)
        glVertex3f(-1.0, 1.0, -1.0)
        glVertex3f(-1.0, 1.0, 1.0)
        glVertex3f(1.0, 1.0, 1.0)
    
        # Bottom blue
        glColor3f(0.0, 0.0, 1.0)
        glVertex3f(1.0, -1.0, 1.0)
        glVertex3f(-1.0, -1.0, 1.0)
        glVertex3f(-1.0, -1.0, -1.0)
        glVertex3f(1.0, -1.0, -1.0)

        # Front
        glColor3f(1.0, 1.0, 1.0) # white
        glVertex3f(1.0, 1.0, 1.0)
        glVertex3f(-1.0, 1.0, 1.0)
        glVertex3f(-1.0, -1.0, 1.0)
        glVertex3f(1.0, -1.0, 1.0)
    
        # Back
        glColor3f(1.0, 1.0, 0.0) # yellow
        glVertex3f(1.0, -1.0, -1.0)
        glVertex3f(-1.0, -1.0, -1.0)
        glVertex3f(-1.0, 1.0, -1.0)
        glVertex3f(1.0, 1.0, -1.0)

        # Left
        glColor3f(1.0, 0.0, 0.0) # red
        glVertex3f(-1.0, 1.0, 1.0)
        glVertex3f(-1.0, 1.0, -1.0)
        glVertex3f(-1.0, -1.0, -1.0)
        glVertex3f(-1.0, -1.0, 1.0)

        # Right
        glColor3f(1.0, 0.5, 0.0) # orange
        glVertex3f(1.0, 1.0, -1.0)
        glVertex3f(1.0, 1.0, 1.0)
        glVertex3f(1.0, -1.0, 1.0)
        glVertex3f(1.0, -1.0, -1.0)
        
        glEnd()
        glPopMatrix()

class Renderer :
    def draw_cublet ( self ) :
        glLineWidth(GLfloat(5.0))
        glBegin(GL_LINES)
        glColor3fv((0.0,0.0,0.0))



main()