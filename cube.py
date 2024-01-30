import math
import pygame
import random
from OpenGL.GL import *
from OpenGL.GLU import *
from pygame.locals import *

class Cube3 :
    """
        Based on the axis-aligned positions of the cubelets, each Group has a multiplicity of 24;
        - 8 corner pieces
        - 12 edge pieces
        - 6 center pieces
        - 1 core piece
        
        Moves act upon a face or slice of the cube, always acting upon 9 cubelets. All Moves that apply to neighbouring axes collide, and since a Cube3 has only three axes, this is always the case; so only Moves that share the same axis can occur at the same time.
    """
    def __init__ ( self ) :
        self.groups = {
            "core" : [
                Cubelet( 0, 0, 0)
            ],
            "centers" : [
                Cubelet( 0, 0,-1),
                Cubelet( 0, 0, 1),
                Cubelet( 0,-1, 0),
                Cubelet( 0, 1, 0),
                Cubelet(-1, 0, 0),
                Cubelet( 1, 0, 0),
            ],
            "edges" : [
                Cubelet( 0,-1,-1),
                Cubelet( 0,-1, 1),
                Cubelet( 0, 1,-1),
                Cubelet( 0, 1, 1),
                Cubelet(-1, 0,-1),
                Cubelet(-1, 0, 1),
                Cubelet( 1, 0,-1),
                Cubelet( 1, 0, 1),
                Cubelet(-1,-1, 0),
                Cubelet(-1, 1, 0),
                Cubelet( 1,-1, 0),
                Cubelet( 1, 1, 0),
            ],
            "corners" : [
                Cubelet(-1,-1,-1),
                Cubelet(-1,-1, 1),
                Cubelet(-1, 1,-1),
                Cubelet(-1, 1, 1),
                Cubelet( 1,-1,-1),
                Cubelet( 1,-1, 1),
                Cubelet( 1, 1,-1),
                Cubelet( 1, 1, 1),
            ]
        }
    
    def draw ( self ) :
        for group in self.groups :
            for cubelet in self.groups[group] :
                cubelet.draw()

class Cube4 :
    """
        A Cube4 is a 4x4x4 cube, consisting of 64 cubelets, in 4 groups.
        - 8 corner pieces
        - 24 edge pieces
        - 24 center pieces
        - 8 core pieces
    """

    def __init__ ( self ) :
        self.groups = {
            "core" : [
                Cubelet(-0.5,-0.5,-0.5),
                Cubelet(-0.5,-0.5, 0.5),
                Cubelet(-0.5, 0.5,-0.5),
                Cubelet(-0.5, 0.5, 0.5),
                Cubelet( 0.5,-0.5,-0.5),
                Cubelet( 0.5,-0.5, 0.5),
                Cubelet( 0.5, 0.5,-0.5),
                Cubelet( 0.5, 0.5, 0.5)
            ],
            "centers" : [
                Cubelet(-0.5,-0.5,-1.5),
                Cubelet(-0.5,-0.5, 1.5),
                Cubelet(-0.5, 0.5,-1.5),
                Cubelet(-0.5, 0.5, 1.5),
                Cubelet( 0.5,-0.5,-1.5),
                Cubelet( 0.5,-0.5, 1.5),
                Cubelet( 0.5, 0.5,-1.5),
                Cubelet( 0.5, 0.5, 1.5),

                Cubelet(-0.5,-1.5,-0.5),
                Cubelet(-0.5, 1.5,-0.5),
                Cubelet(-0.5,-1.5, 0.5),
                Cubelet(-0.5, 1.5, 0.5),
                Cubelet( 0.5,-1.5,-0.5),
                Cubelet( 0.5, 1.5,-0.5),
                Cubelet( 0.5,-1.5, 0.5),
                Cubelet( 0.5, 1.5, 0.5),

                Cubelet(-1.5,-0.5,-0.5),
                Cubelet( 1.5,-0.5,-0.5),
                Cubelet(-1.5,-0.5, 0.5),
                Cubelet( 1.5,-0.5, 0.5),
                Cubelet(-1.5, 0.5,-0.5),
                Cubelet( 1.5, 0.5,-0.5),
                Cubelet(-1.5, 0.5, 0.5),
                Cubelet( 1.5, 0.5, 0.5),
            ],
            "edges" : [
                Cubelet(-0.5,-1.5,-1.5),
                Cubelet(-0.5,-1.5, 1.5),
                Cubelet(-0.5, 1.5,-1.5),
                Cubelet(-0.5, 1.5, 1.5),
                Cubelet( 0.5,-1.5,-1.5),
                Cubelet( 0.5,-1.5, 1.5),
                Cubelet( 0.5, 1.5,-1.5),
                Cubelet( 0.5, 1.5, 1.5),
                
                Cubelet(-1.5,-0.5,-1.5),
                Cubelet(-1.5,-0.5, 1.5),
                Cubelet( 1.5,-0.5,-1.5),
                Cubelet( 1.5,-0.5, 1.5),
                Cubelet(-1.5, 0.5,-1.5),
                Cubelet(-1.5, 0.5, 1.5),
                Cubelet( 1.5, 0.5,-1.5),
                Cubelet( 1.5, 0.5, 1.5),
                
                Cubelet(-1.5,-1.5,-0.5),
                Cubelet(-1.5, 1.5,-0.5),
                Cubelet( 1.5,-1.5,-0.5),
                Cubelet( 1.5, 1.5,-0.5),
                Cubelet(-1.5,-1.5, 0.5),
                Cubelet(-1.5, 1.5, 0.5),
                Cubelet( 1.5,-1.5, 0.5),
                Cubelet( 1.5, 1.5, 0.5),
            ],
            "corners" : [
                Cubelet(-1.5,-1.5,-1.5),
                Cubelet(-1.5,-1.5, 1.5),
                Cubelet(-1.5, 1.5,-1.5),
                Cubelet(-1.5, 1.5, 1.5),
                Cubelet( 1.5,-1.5,-1.5),
                Cubelet( 1.5,-1.5, 1.5),
                Cubelet( 1.5, 1.5,-1.5),
                Cubelet( 1.5, 1.5, 1.5),
            ]
        }
    
    def draw ( self ) :
        for group in self.groups :
            for cubelet in self.groups[group] :
                cubelet.draw()


class Cubelet :
    """
        A Cubelet is a 3 axis Element.
    """

    def __init__ ( self, x, y, z ) :
        self.pos = (x, y, z)

    def draw ( self ) :
        glPushMatrix()
        glTranslatef(*self.pos)
        glScalef(0.3, 0.3, 0.3)
        self.draw_unit()
        glPopMatrix()

    def draw_unit ( self ) :
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

    """
        A Path P is a series of discrete time Moves an Entity A makes in a directed, labeled graph G = (V, E), where V is the node set, and E is the edge set representing the connections between these positions. Given a Path P_i, P_i[t] denotes the position of entity A at time t.

        A Move is formalized as a function a : V -> V, such that a(v) = v' represents the action of moving from v to v'. Moves apply to a set of Entities, and always permute their physical position, even if the logical positions might differ.

        Given two Paths P_i and P_j are valid with respect to each other if there are no collisions. A collision occurs if at the same time t, two Moves occur that apply to the same Entity. The Identity Move trivially collides with all other Moves.
    """
    """
        A Group is a collection of Entities A with their Paths.
        Entities form a Group if they share the same subgraph of V.
        Because every group is axis-aligned in 3d physical space, all logical positions have 6 outgoing and 6 incoming edges, for both rotational directions of the three axes directly neighbouring  
    """
    """
        A ... is a set of Groups with intersecting Moves.
    """

    """
        A Megaminx is a one layer dodecahedron, consisting of 
        Based on the axis-aligned positions of the cubelets, each Group has a multiplicity of 60;
        - 20 corner pieces
        - 30 edge pieces
        - 12 center pieces
        63
    """


