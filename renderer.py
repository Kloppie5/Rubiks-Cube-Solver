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
    
class Renderer :

    def __init__ ( self ) :
        self.rotationsteps = 8
        self.rotationangle = pi / 2 / rotationsteps

    def draw_cublet ( self ) :
        glLineWidth(GLfloat(5.0))
        glBegin(GL_LINES)
        glColor3fv((0.0,0.0,0.0))



main()