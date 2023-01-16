import pytest
from cube import *

all_faces = ["U", "D", "L", "R", "F", "B"]

@pytest.mark.parametrize("face", all_faces)
def test_equality_twice ( face ) :
    assert Interface().run(Cube(I), [face+"2"]) == Interface().run(Cube(I), [face, face])

@pytest.mark.parametrize("face", all_faces)
def test_counter_undo ( face ) :
    assert Interface().run(Cube(I), [face, face+"'"]) == Cube(I)

@pytest.mark.parametrize("face", all_faces)
def test_identity_quadruple ( face ) :
    assert Interface().run(Cube(I), [face, face, face, face]) == Cube(I)

def test_sexy_move ( ) :
    sexy_move = ["R U R' U'"]
    assert Interface().run(Cube(I), sexy_move * 6) == Cube(I)

def test_t_perm ( ) :
    t_perm = ["R U R' U' R' F R2 U' R' U' R U R' F'"]
    assert Interface().run(Cube(I), t_perm * 2) == Cube(I)

@pytest.mark.parametrize("scramble, solution", [
    ("F2 U' F' B D B' L B2 D' R2 U' R2 F2 B2 R2 B2 U2 R F R", "R' B2 R' F D L B' D' F U' F2 R2 L B2 L2 U2 B2 D2 F2 R2 L'"),
    ("D2 L2 D' R' B2 L F L R2 U' F2 U L2 B2 U L2 U D B2 D' R", "R' D B2 D' U' L2 U' B2 L2 U' F2 U R2 L' F' L' B2 R D L2 D2"),
    ("F2 U' B2 L2 F D R' F L2 F B2 D2 L2 B' L2 B R2 B2 L2 D' F'", "F B2 D' F2 L U2 L' U' L2 F' D2 B' U2 L2 D2 B' D2 B L2 U2 L'"),
    ("F' U F B L B L U R' F2 R D2 L' U2 D2 L2 F2 R' D2 L2 U", "U' L2 D2 R F2 L2 D2 U2 L D2 R' F2 R U' L' B' L' B' F' U' F"),
    ("D2 L F' B R2 U' L' F' R' U L2 B2 U2 R B2 R F2 R U2 L' D2", "R D B2 U' L F2 R U L2 U R2 U' D F2 L2 D' L2 D F D B'"),
    ("B R2 F R2 B R2 D2 F U2 F' R U' R2 F D' R F L U'", "U L' F' R' D F' R2 U R' F U2 F' D2 R2 B' R2 F' R2 B'"),
])
def test_scramble_solve ( scramble, solution) :
    scramble = Interface().run(Cube(I), scramble.split())
    solution = Interface().run(scramble, solution.split())
    assert solution == Cube(I)
