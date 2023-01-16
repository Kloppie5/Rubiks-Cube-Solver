
def quaternion_multiply ( a, b ) :
    """
      Multiplies two quaternions.
    """
    w1, x1, y1, z1 = a
    w2, x2, y2, z2 = b
    w = w1*w2 - x1*x2 - y1*y2 - z1*z2
    x = w1*x2 + x1*w2 + y1*z2 - z1*y2
    y = w1*y2 + y1*w2 + z1*x2 - x1*z2
    z = w1*z2 + z1*w2 + x1*y2 - y1*x2
    return (w, x, y, z)

class Cube :
    """
      A Cube is a 3x3x3 Rubik's Cube.
      The internal state is expressed as a sparse 20 by 20 matrix of quaternions.
      This representation is simplified into an array of 20 tuples, each of which is
      the index of the piece and the quaternion representing its orientation.
      This means that the index in the array is the original position of the piece.
      The quaternions are represented as simple tuples of 4 floats; w, x, y, z.

      The numbering of the pieces follows the reverse order in which you would
      solve the cube, with the bottom layer being white and the front layer being
      blue. The centers are excluded. This gives the following pieces, numbered in order:

      Yellow-Green-Orange, Yellow-Green-Red, Yellow-Blue-Orange, Yellow-Blue-Red,
      Yellow-Green, Yellow-Orange, Yellow-Red, Yellow-Blue,
      Green-Orange, Green-Red, Blue-Orange, Blue-Red,
      White-Green-Orange, White-Green-Red, White-Blue-Orange, White-Blue-Red,
      White-Green, White-Orange, White-Red, White-Blue.

            00 ---- 04 ---- 01
            /|      /       /|      00 04 01
           / |     /       / |      05 YY 06
         05 08   YY      06 09      02 07 03
         /   |   /       /  /|
        /    |  /       /  / |      08 GG 09      Y
      02 ----|07 ---- 03 RR  |      OO CC RR      OX UL
       |    12 |--- 16 |-/- 13      10 BB 11     Z
       |    /  |       |/   /
      10   /  BB      11   /        12 16 13
       | 17    |       | 18         17 WW 18
       | /     |       | /          14 19 15
       |/      |       |/
      14 ---- 19 ---- 15
    """

    pieces = [
        { "name" : "Yellow-Green-Orange", "colors" : "YO--G-" },
        { "name" : "Yellow-Green-Red",    "colors" : "Y--RG-" },
        { "name" : "Yellow-Blue-Orange",  "colors" : "YOB---" },
        { "name" : "Yellow-Blue-Red",     "colors" : "Y-BR--" },
        { "name" : "Yellow-Green",        "colors" : "Y-- G-" },
        { "name" : "Yellow-Orange",       "colors" : "YO----" },
        { "name" : "Yellow-Red",          "colors" : "Y--R--" },
        { "name" : "Yellow-Blue",         "colors" : "Y-B---" },
        { "name" : "Green-Orange",        "colors" : "-O--G-" },
        { "name" : "Green-Red",           "colors" : "---RG-" },
        { "name" : "Blue-Orange",         "colors" : "-OB---" },
        { "name" : "Blue-Red",            "colors" : "---R--" },
        { "name" : "White-Green-Orange",  "colors" : "-O--GW" },
        { "name" : "White-Green-Red",     "colors" : "---RGW" },
        { "name" : "White-Blue-Orange",   "colors" : "-OB--W" },
        { "name" : "White-Blue-Red",      "colors" : "--BR-W" },
        { "name" : "White-Green",         "colors" : "--- GW" },
        { "name" : "White-Orange",        "colors" : "-O---W" },
        { "name" : "White-Red",           "colors" : "---R-W" },
        { "name" : "White-Blue",          "colors" : "--B--W" }
    ]

    def __init__ ( self, cube ) :
        self.cube = cube

    def __str__ ( self ) :
        r = ""
        for i in range(20) :
            piece, quaternion = self.cube[i]
            r += f"{'.'*piece}X{'.'*(19-piece)} | {Cube.pieces[i]['colors']} | {quaternion}\n"
        return r
    
    def __getitem__ ( self, loc ) :
        return self.cube[loc]

    def __mul__ ( self, rhs ) :
        new_cube = [None] * 20
        for loc in range(20) :
            prev_loc, quaternion = rhs[loc]
            piece, prev_quaternion = self.cube[prev_loc]
            new_quaternion = quaternion_multiply(prev_quaternion, quaternion)
            new_cube[loc] = (piece, new_quaternion)
        return Cube(new_cube)
    
    def __eq__ ( self, rhs ) :
        for i in range(20) :
            ql = self.cube[i][1]
            qr = rhs[i][1]

            if abs(ql[0]) - abs(qr[0]) > 0.0001 :
                return False
            for j in range(1, 4) :
                if abs(ql[j] - qr[j]) > 0.0001 :
                    return False
        return True

def permutation ( cyclic_permutation = [], rotation = (1, 0, 0, 0) ) :
    cube = [None] * 20
    for i in range(20) :
        cube[i] = (i, (1, 0, 0, 0))
    
    for i, j in cyclic_permutation :
        cube[i] = (j, rotation)

    return Cube(cube)

a  = 0.7071067811865476 # 90/2 angle
        
I  = permutation() # Identity
Rc = permutation([( 1, 13), ( 3,  1), (13, 15), (15,  3), ( 6,  9), ( 9, 18), (11,  6), (18, 11)], (a,  a,  0,  0)) # Red counterclockwise
O  = permutation([( 0, 12), ( 2,  0), (12, 14), (14,  2), ( 5,  8), ( 8, 17), (10,  5), (17, 10)], (a,  a,  0,  0)) # Orange clockwise
R  = permutation([( 1,  3), ( 3, 15), (13,  1), (15, 13), ( 6, 11), ( 9,  6), (11, 18), (18,  9)], (a, -a,  0,  0)) # Red clockwise
Oc = permutation([( 0,  2), ( 2, 14), (12,  0), (14, 12), ( 5, 17), ( 8,  5), (10,  8), (17, 10)], (a, -a,  0,  0)) # Orange counterclockwise
W  = permutation([(12, 13), (13, 15), (14, 12), (15, 14), (16, 18), (17, 16), (18, 19), (19, 17)], (a,  0,  a,  0)) # White clockwise
Yc = permutation([( 0,  1), ( 1,  3), ( 2,  0), ( 3,  2), ( 4,  6), ( 5,  4), ( 6,  7), ( 7,  5)], (a,  0,  a,  0)) # Yellow counterclockwise
Wc = permutation([(12, 14), (13, 12), (14, 15), (15, 13), (16, 17), (17, 19), (18, 16), (19, 18)], (a,  0, -a,  0)) # White counterclockwise
Y  = permutation([( 0,  2), ( 1,  0), ( 2,  3), ( 3,  1), ( 4,  5), ( 5,  7), ( 6,  4), ( 7,  6)], (a,  0, -a,  0)) # Yellow clockwise
Bc = permutation([( 2,  3), ( 3, 15), (14,  2), (15, 14), ( 7, 11), (10,  7), (11, 19), (19, 10)], (a,  0,  0,  a)) # Blue counterclockwise
G  = permutation([( 0,  1), ( 1, 13), (12,  0), (13, 12), ( 4,  9), ( 8,  4), ( 9, 16), (16,  8)], (a,  0,  0,  a)) # Green clockwise
B  = permutation([( 2, 14), ( 3,  2), (14, 15), (15,  3), ( 7, 10), (10, 19), (11,  7), (19, 11)], (a,  0,  0, -a)) # Blue clockwise
Gc = permutation([( 0, 12), ( 1,  0), (12, 13), (13,  1), ( 4,  8), ( 8, 16), ( 9,  4), (16,  9)], (a,  0,  0, -a)) # Green counterclockwise

class Interface :

    def __init__ ( self ) :
        self.commands = {
            "q" : ("Quit", exit),
            "r" : ("Red clockwise", lambda cube : cube * R),
            "rc" : ("Red counterclockwise", lambda cube : cube * Rc),
            "o" : ("Orange clockwise", lambda cube : cube * O),
            "oc" : ("Orange counterclockwise", lambda cube : cube * Oc),
            "w" : ("White clockwise", lambda cube : cube * W),
            "wc" : ("White counterclockwise", lambda cube : cube * Wc),
            "y" : ("Yellow clockwise", lambda cube : cube * Y),
            "yc" : ("Yellow counterclockwise", lambda cube : cube * Yc),
            "b" : ("Blue clockwise", lambda cube : cube * B),
            "bc" : ("Blue counterclockwise", lambda cube : cube * Bc),
            "g" : ("Green clockwise", lambda cube : cube * G),
            "gc" : ("Green counterclockwise", lambda cube : cube * Gc),
            "i" : ("Identity", lambda cube : I),
            "s" : ("Sexy move", lambda cube : cube * R * Y * Rc * Yc),

            "U" : ("Up", lambda cube : cube * W),
            "U2" : ("Up twice", lambda cube : cube * W * W),
            "U'" : ("Up counterclockwise", lambda cube : cube * Wc),
            "D" : ("Down", lambda cube : cube * Y),
            "D2" : ("Down twice", lambda cube : cube * Y * Y),
            "D'" : ("Down counterclockwise", lambda cube : cube * Yc),
            "L" : ("Left", lambda cube : cube * O),
            "L2" : ("Left twice", lambda cube : cube * O * O),
            "L'" : ("Left counterclockwise", lambda cube : cube * Oc),
            "R" : ("Right", lambda cube : cube * R),
            "R2" : ("Right twice", lambda cube : cube * R * R),
            "R'" : ("Right counterclockwise", lambda cube : cube * Rc),
            "F" : ("Front", lambda cube : cube * G),
            "F2" : ("Front twice", lambda cube : cube * G * G),
            "F'" : ("Front counterclockwise", lambda cube : cube * Gc),
            "B" : ("Back", lambda cube : cube * B),
            "B2" : ("Back twice", lambda cube : cube * B * B),
            "B'" : ("Back counterclockwise", lambda cube : cube * Bc),
        }
    
    def run ( self, cube, command_queue, debug = False ) :
        while len(command_queue) > 0 :
            command = command_queue.pop(0)
            if command == "" :
                continue
            if command in self.commands :
                if debug :
                    print(self.commands[command][0])
                cube = self.commands[command][1](cube)
            else :
                print(f"Invalid command: {command}\n")
        return cube
    

if __name__ == "__main__" :
    cube = I
    while True :
        command_input = input("Command: ")
        command_queue = command_input.split(" ")
        cube = Interface().run(cube, command_queue)
        print(cube)
        
