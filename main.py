import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

from cube import Cube3, Cube4

def main ( ) :
    pygame.init()
    display = (800,600)
    pygame.display.set_mode(display, DOUBLEBUF|OPENGL)

    glEnable(GL_DEPTH_TEST)
    glDepthFunc(GL_LESS)

    glMatrixMode(GL_PROJECTION)
    gluPerspective(45, (display[0]/display[1]), 0.1, 50.0)


    glMatrixMode(GL_MODELVIEW)
    glTranslatef(0.0,0.0,-20)

    cube = Cube4()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        glRotatef(1,3,1,1)
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        
        cube.draw()

        pygame.display.flip()
        pygame.time.wait(10)

if __name__ == "__main__" :
    main()