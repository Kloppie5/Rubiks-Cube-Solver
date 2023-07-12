import math
import random

class Cube :
    """
        A Cube is an abstract object with disjoint groups of rotation-cyclic states of size 24.

        Since pieces are always axis-aligned, an orientation can be expressed as a permutation of the diagonals, giving us 24 axis-aligned states.

        We arbitrarily assign the diagonals as 1, 2, 3, 4 being the diagonals starting from the topleft, topright, bottomleft, and bottomright pieces of the top face.
        We name the horizontal axis as x, the vertical axis as y, and the depth axis as z, and use clockwise rotations as positive and counterclockwise as negative, indicated by the prime symbol.

        This gives us a way to both represent the current rotation of a piece, as well as a rotation operation by means of a cyclic permutation.

        x  = (1324)
        x' = (1423)
        y  = (1342)
        y' = (1243)
        z  = (1432)
        z' = (1234)

        This means we can list all 24 rotations as follows:

        # Rot   Perm     Col Ops
        o 1234           WG  e
        
        x 3421  (1324)   BW  x
        r 4312  (1423)   GY  x'
        y 3142  (1342)   WO  y
        s 2413  (1243)   WR  y'
        z 4123  (1432)   RG  z
        t 2341  (1234)   OG  z'
        
        u 2143  (12)(34) YB  xx
        v 4321  (14)(23) WB  yy
        w 3412  (13)(24) YG  zz
        
        a 4213  (143)    BO  xy   = yz'  = z'x
        b 1342  (234)    BR  xy'  = y'z  = zx
        c 2314  (123)    RW  xz   = yx   = zy
        d 4132  (142)    OW  xz'  = y'x  = z'y' 
        e 2431  (124)    GO  x'y  = yz   = zx'
        f 3124  (132)    GR  x'y' = y'z' = z'x'
        g 3241  (134)    RY  x'z  = y'x' = zy'
        h 1423  (243)    OY  x'z' = yx'  = z'y
        
        i 1243  (34)     GW  xzz  = x'yy = yxz   = yyx    = yzy    = y'xz' = y'z'y' = zx'y' = zyz    = zzx'   = z'x'y' = z'y'z'
        j 1324  (23)     YO  xxy  = xyz' = xz'x  = x'yz   = x'zx'  = yzz   = y'xx   = zx'z  = zy'x'  = zzy'   = z'xz'  = z'y'x
        k 1432  (24)     RB  xxz  = xyx  = xzy   = x'y'x' = x'zy'  = yxy   = yyz'   = yz'x  = y'x'y' = y'z'x' = zyy    = z'xx
        l 2134  (12)     BY  xyy  = x'zz = yx'z' = yyx'   = yz'y   = y'x'z = y'zy'  = zxy'  = zy'z   = zzx    = z'xy   = z'yz'
        m 3214  (13)     OB  xxz' = xy'x = xz'y' = x'yx'  = x'z'y  = yx'y  = yyz    = yzx'  = y'xy'  = y'zx   = zxx    = z'yy
        n 4231  (14)     YR  xxy' = xy'z = xzx   = x'y'z' = x'z'x' = yxx   = y'zz   = zxz   = zyx    = zzy    = z'x'z' = z'yx'
        
        Using the original position of a piece, its current position and its rotation carry the same information. This means we can express an operation on a group of pieces a permutation too. For this reason, we assign a single letter name to each rotation.
    """

    rotations = {
        "-" : (1, 2, 3, 4),
        "x" : (3, 4, 2, 1),
        "r" : (4, 3, 1, 2),
        "y" : (3, 1, 4, 2),
        "s" : (2, 4, 1, 3),
        "z" : (4, 1, 2, 3),
        "t" : (2, 3, 4, 1),
        "u" : (2, 1, 4, 3),
        "v" : (4, 3, 2, 1),
        "w" : (3, 4, 1, 2),
        "a" : (4, 2, 1, 3),
        "b" : (1, 3, 4, 2),
        "c" : (2, 3, 1, 4),
        "d" : (4, 1, 3, 2),
        "e" : (2, 4, 3, 1),
        "f" : (3, 1, 2, 4),
        "g" : (3, 2, 4, 1),
        "h" : (1, 4, 2, 3),
        "i" : (1, 2, 4, 3),
        "j" : (1, 3, 2, 4),
        "k" : (1, 4, 3, 2),
        "l" : (2, 1, 3, 4),
        "m" : (3, 2, 1, 4),
        "n" : (4, 2, 3, 1)
    }

    def __init__ ( self, size ) :
        self.size = size
        self.pieces = ["-" for x in range(size * size * size)]
        self.piece_order = [x for x in range(size * size * size)]
        self.piece_moves = [[] for _ in range(len(self.pieces))]
        self.loc_moves = [[] for _ in range(len(self.pieces))]
        self.root_operation = {}
        self.operations = {}

    def add_root_operation ( self, name, rotations, permutations ) :
        self.root_operation[name] = (rotations, permutations)
    def add_operation ( self, name, operations ) :
        pieces = ["-" for x in range(self.size * self.size * self.size)]
        piece_order = [x for x in range(self.size * self.size * self.size)]
        for operation in operations.split(" ") :
            subrotations, subpermutations = self.root_operation[operation]
            pieces = [
                [k for k, v in Cube.rotations.items() if v == tuple(
                    [Cube.rotations[subrotations[i]][Cube.rotations[pieces[i]][x] - 1]
                    for x in range(4)]
                )][0]
            for i in range(self.size * self.size * self.size)]
            # Permutation
            for perm in subpermutations :
                for (old, new) in list(zip(perm[:-1], perm[1:]))[::-1] :
                    pieces[old], pieces[new] = pieces[new], pieces[old]
                    piece_order[old], piece_order[new] = piece_order[new], piece_order[old]
        permutations = []
        for i in range(len(piece_order)) :
            if piece_order[i] == i or piece_order[i] == -1 :
                continue
            permutation = []
            while piece_order[i] != -1 :
                permutation.append(i)
                piece_order[i], i = -1, piece_order[i]
            permutations.append(permutation[::-1])
        self.operations[name] = ("".join(pieces), permutations)
    def apply_operations ( self, operations ) :
        for operation in operations.split(" ") :
            if operation == "|" :
                self.dump()
            else :
                self.apply(operation)
    def apply ( self, name ) :
        rotations, permutations = self.operations[name]
        prev = "".join(self.pieces)
        # Rotation
        self.pieces = [
            [k for k, v in Cube.rotations.items() if v == tuple(
                [Cube.rotations[rotations[i]][Cube.rotations[self.pieces[i]][x] - 1]
                for x in range(4)]
            )][0]
        for i in range(self.size * self.size * self.size)]
        # Permutation
        mov_len = len(self.piece_moves[0]) + 1
        for perm in permutations :
            for (old, new) in list(zip(perm[:-1], perm[1:]))[::-1] :
                self.pieces[old], self.pieces[new] = self.pieces[new], self.pieces[old]
                self.piece_order[old], self.piece_order[new] = self.piece_order[new], self.piece_order[old]
                self.piece_moves[old], self.piece_moves[new] = self.piece_moves[new], self.piece_moves[old]
                if len(self.piece_moves[old]) < mov_len :
                    self.piece_moves[old].append(f"{name:2}")
                if len(self.piece_moves[new]) < mov_len :
                    self.piece_moves[new].append(f"{name:2}")
        for i in range(len(self.pieces)) :
            if self.pieces[i] != prev[i] :
                self.loc_moves[i].append(f"{name:2}")
            else :
                self.loc_moves[i].append("  ")
            if len(self.piece_moves[i]) < mov_len :
                self.piece_moves[i].append("  ")
    def set_state ( self, pieces, permutations ) :
        self.pieces = list(pieces)
        self.piece_order = [x for x in range(self.size * self.size * self.size)]
        self.piece_moves = [[] for _ in range(len(self.pieces))]
        self.loc_moves = [[] for _ in range(len(self.pieces))]
        for perm in permutations :
            for (old, new) in list(zip(perm[:-1], perm[1:]))[::-1] :
                self.piece_order[old], self.piece_order[new] = self.piece_order[new], self.piece_order[old]

    def calc_permutations ( self ) :
        permutations = []
        piece_order = [self.piece_order[i] for i in range(len(self.piece_order))]
        for i in range(len(piece_order)) :
            if piece_order[i] == i or piece_order[i] == -1 :
                continue
            permutation = []
            while piece_order[i] != -1 :
                permutation.append(i)
                piece_order[i], i = -1, piece_order[i]
            permutations.append(permutation[::-1])
        return permutations

class Cube3Old ( Cube ) :

    """
        i=00 i=01 i=02 
        i=03 i=04 i=05 
        i=06 i=07 i=08 

        i=09 i=10 i=11 
        i=12 i=13 i=14 
        i=15 i=16 i=17 

        i=18 i=19 i=20 
        i=21 i=22 i=23 
        i=24 i=25 i=26 
    """

    def __init__ ( self, pieces = "---------------------------" ) :
        super().__init__(3)
        self.pieces = list(pieces)

        self.add_root_operation("x1", "x--x--x--x--x--x--x--x--x--", [[ 0,  6, 24, 18], [ 3, 15, 21,  9]])
        self.add_root_operation("x2", "-x--x--x--x--x--x--x--x--x-", [[ 1,  7, 25, 19], [ 4, 16, 22, 10]])
        self.add_root_operation("x3", "--x--x--x--x--x--x--x--x--x", [[ 2,  8, 26, 20], [ 5, 17, 23, 11]])
        self.add_root_operation("y1", "------------------yyyyyyyyy", [[18, 24, 26, 20], [19, 21, 25, 23]])
        self.add_root_operation("y2", "---------yyyyyyyyy---------", [[ 9, 15, 17, 11], [10, 12, 16, 14]])
        self.add_root_operation("y3", "yyyyyyyyy------------------", [[ 0,  6,  8,  2], [ 1,  3,  7,  5]])
        self.add_root_operation("z1", "zzz------zzz------zzz------", [[ 0, 18, 20,  2], [ 1,  9, 19, 11]])
        self.add_root_operation("z2", "---zzz------zzz------zzz---", [[ 3, 21, 23,  5], [ 4, 12, 22, 14]])
        self.add_root_operation("z3", "------zzz------zzz------zzz", [[ 6, 24, 26,  8], [ 7, 15, 25, 17]])

        self.add_operation("L",  "x1")
        self.add_operation("L2", "x1 x1")
        self.add_operation("L'", "x1 x1 x1")
        self.add_operation("M",  "x2")
        self.add_operation("M2", "x2 x2")
        self.add_operation("M'", "x2 x2 x2")
        self.add_operation("R",  "x3 x3 x3")
        self.add_operation("R2", "x3 x3")
        self.add_operation("R'", "x3")
        self.add_operation("D",  "y1")
        self.add_operation("D2", "y1 y1")
        self.add_operation("D'", "y1 y1 y1")
        self.add_operation("E",  "y2")
        self.add_operation("E2", "y2 y2")
        self.add_operation("E'", "y2 y2 y2")
        self.add_operation("U",  "y3 y3 y3")
        self.add_operation("U2", "y3 y3")
        self.add_operation("U'", "y3")
        self.add_operation("B",  "z1")
        self.add_operation("B2", "z1 z1")
        self.add_operation("B'", "z1 z1 z1")
        self.add_operation("S",  "z2 z2 z2")
        self.add_operation("S2", "z2 z2")
        self.add_operation("S'", "z2")
        self.add_operation("F",  "z3 z3 z3")
        self.add_operation("F2", "z3 z3")
        self.add_operation("F'", "z3")

        self.add_operation("l",  "x1 x2")
        self.add_operation("l2", "x1 x1 x2 x2")
        self.add_operation("l'", "x1 x1 x1 x2 x2 x2")
        self.add_operation("r",  "x2 x2 x2 x3 x3 x3")
        self.add_operation("r2", "x2 x2 x3 x3")
        self.add_operation("r'", "x2 x3")
        self.add_operation("d",  "y1 y2")
        self.add_operation("d2", "y1 y1 y2 y2")
        self.add_operation("d'", "y1 y1 y1 y2 y2 y2")
        self.add_operation("u",  "y2 y2 y2 y3 y3 y3")
        self.add_operation("u2", "y2 y2 y3 y3")
        self.add_operation("u'", "y2 y3")
        self.add_operation("b",  "z1 z2")
        self.add_operation("b2", "z1 z1 z2 z2")
        self.add_operation("b'", "z1 z1 z1 z2 z2 z2")
        self.add_operation("f",  "z2 z2 z2 z3 z3 z3")
        self.add_operation("f2", "z2 z2 z3 z3")
        self.add_operation("f'", "z2 z3")

        self.add_operation("x",  "x1 x1 x1 x2 x2 x2 x3 x3 x3")
        self.add_operation("x2", "x1 x1 x2 x2 x3 x3")
        self.add_operation("x'", "x1 x2 x3")
        self.add_operation("y",  "y1 y1 y1 y2 y2 y2 y3 y3 y3")
        self.add_operation("y2", "y1 y1 y2 y2 y3 y3")
        self.add_operation("y'", "y1 y2 y3")
        self.add_operation("z",  "z1 z1 z1 z2 z2 z2 z3 z3 z3")
        self.add_operation("z2", "z1 z1 z2 z2 z3 z3")
        self.add_operation("z'", "z1 z2 z3")

    def dump ( self ) :
        print("".join(self.pieces))
    
    def split_view ( self ) :
        print(f"{''.join(self.pieces)} | {self.calc_permutations()}")
        for piece in range(len(self.pieces)) :
            print(f"{piece:2} | {''.join(self.loc_moves[piece])} | {''.join(self.piece_moves[piece])} | {self.pieces[piece]} {Cube.rotations[self.pieces[piece]]} | {self.piece_order[piece]}")

class PermutationMatrix :
    """
        A Permutation Matrix is a square matrix that is row-equivalent to the identity matrix.
        Because proper matrix multiplication with a large matrix is slow, this is internally done by tracking an index array.
    """

    def __init__ ( self ) :
        self.state = {}

    def __getitem__ ( self, key ) :
        return self.state[key] if key in self.state else key
    def __setitem__ ( self, key, value ) :
        self.state[key] = value
    def __len__ ( self ) :
        if len(self.state) == 0 :
            return 0
        return max(len(self.state), max(self.state.keys()) + 1)

    def dump ( self ) :
        for i in range(len(self)) :
            row = ["-" for _ in range(len(self))]
            row[i] = "\\"
            row[self[i]] = "1"
            print(f"{i:3} | {''.join(row)} | {self[i]:3}")

    def __str__ ( self ) :
        return ",".join([str(self[i]) for i in range(len(self))])

class PermutationCube :
    """
        A Permutation Cube is a cube represented by a Permutation Matrix.
        Each set of four rows represents a cubicle, and each set of four columns represents a cubie.
        The four parts are the four center crossing diagonals, such that the 4x4 submatrix represents the orientation of the cubie.
    """

    def __init__ ( self, moves = [] ) :
        self.state = PermutationMatrix()
        for move in moves :
            self.state[move[0]*4    ] = move[1]*4 + move[2]
            self.state[move[0]*4 + 1] = move[1]*4 + move[3]
            self.state[move[0]*4 + 2] = move[1]*4 + move[4]
            self.state[move[0]*4 + 3] = move[1]*4 + move[5]

    def __mul__ ( self, other ) :
        result = PermutationCube()
        size = max(len(self.state), len(other.state))
        for i in range(size) :
            result.state[i] = other.state[self.state[i]]
        return result
    
    def __str__ ( self ) :
        return str(self.state)

class Cube3 :

    x1 = PermutationCube([
        ( 0,  6, 2, 3, 1, 0), ( 6, 24, 2, 3, 1, 0), (24, 18, 2, 3, 1, 0), (18,  0, 2, 3, 1, 0),
        ( 3, 15, 2, 3, 1, 0), (15, 21, 2, 3, 1, 0), (21,  9, 2, 3, 1, 0), ( 9,  3, 2, 3, 1, 0),
        (12, 12, 2, 3, 1, 0)
    ])
    x2 = PermutationCube([
        ( 1,  7, 2, 3, 1, 0), ( 7, 25, 2, 3, 1, 0), (25, 19, 2, 3, 1, 0), (19,  1, 2, 3, 1, 0),
        ( 4, 16, 2, 3, 1, 0), (16, 22, 2, 3, 1, 0), (22, 10, 2, 3, 1, 0), (10,  4, 2, 3, 1, 0),
        (13, 13, 2, 3, 1, 0)
    ])
    x3 = PermutationCube([
        ( 2,  8, 2, 3, 1, 0), ( 8, 26, 2, 3, 1, 0), (26, 20, 2, 3, 1, 0), (20,  2, 2, 3, 1, 0),
        ( 5, 17, 2, 3, 1, 0), (17, 23, 2, 3, 1, 0), (23, 11, 2, 3, 1, 0), (11,  5, 2, 3, 1, 0),
        (14, 14, 2, 3, 1, 0)
    ])

    y1 = PermutationCube([
        (18, 24, 2, 0, 3, 1), (24, 26, 2, 0, 3, 1), (26, 20, 2, 0, 3, 1), (20, 18, 2, 0, 3, 1),
        (19, 21, 2, 0, 3, 1), (21, 25, 2, 0, 3, 1), (25, 23, 2, 0, 3, 1), (23, 19, 2, 0, 3, 1),
        (22, 22, 2, 0, 3, 1)
    ])
    y2 = PermutationCube([
        ( 9, 15, 2, 0, 3, 1), (15, 17, 2, 0, 3, 1), (17, 11, 2, 0, 3, 1), (11,  9, 2, 0, 3, 1),
        (10, 12, 2, 0, 3, 1), (12, 16, 2, 0, 3, 1), (16, 14, 2, 0, 3, 1), (14, 10, 2, 0, 3, 1),
        (13, 13, 2, 0, 3, 1)
    ])
    y3 = PermutationCube([
        ( 0,  6, 2, 0, 3, 1), ( 6,  8, 2, 0, 3, 1), ( 8,  2, 2, 0, 3, 1), ( 2,  0, 2, 0, 3, 1),
        ( 1,  3, 2, 0, 3, 1), ( 3,  7, 2, 0, 3, 1), ( 7,  5, 2, 0, 3, 1), ( 5,  1, 2, 0, 3, 1),
        ( 4,  4, 2, 0, 3, 1)
    ])

    z1 = PermutationCube([
        ( 0, 18, 3, 0, 1, 2), (18, 20, 3, 0, 1, 2), (20,  2, 3, 0, 1, 2), ( 2,  0, 3, 0, 1, 2),
        ( 1,  9, 3, 0, 1, 2), ( 9, 19, 3, 0, 1, 2), (19, 11, 3, 0, 1, 2), (11,  1, 3, 0, 1, 2),
        (10, 10, 3, 0, 1, 2)
    ])
    z2 = PermutationCube([
        ( 3, 21, 3, 0, 1, 2), (21, 23, 3, 0, 1, 2), (23,  5, 3, 0, 1, 2), ( 5,  3, 3, 0, 1, 2),
        ( 4, 12, 3, 0, 1, 2), (12, 22, 3, 0, 1, 2), (22, 14, 3, 0, 1, 2), (14,  4, 3, 0, 1, 2),
        (13, 13, 3, 0, 1, 2)
    ])
    z3 = PermutationCube([
        ( 6, 24, 3, 0, 1, 2), (24, 26, 3, 0, 1, 2), (26,  8, 3, 0, 1, 2), ( 8,  6, 3, 0, 1, 2),
        ( 7, 15, 3, 0, 1, 2), (15, 25, 3, 0, 1, 2), (25, 17, 3, 0, 1, 2), (17,  7, 3, 0, 1, 2),
        (16, 16, 3, 0, 1, 2)
    ])
    """
    d0              d1
      i=00 i=01 i=02
      i=03 i=04 i=05
      i=06 i=07 i=08
    d2              d3
    
      i=09 i=10 i=11
      i=12 i=13 i=14
      i=15 i=16 i=17

    d3              d2
      i=18 i=19 i=20
      i=21 i=22 i=23
      i=24 i=25 i=26
    d1              d0 
    """

    operations = {
        "L"  : x1,
        "L2" : x1 * x1,
        "L'" : x1 * x1 * x1,
        "M"  : x2,
        "M2" : x2 * x2,
        "M'" : x2 * x2 * x2,
        "R"  : x3 * x3 * x3,
        "R2" : x3 * x3,
        "R'" : x3,
        "D"  : y1,
        "D2" : y1 * y1,
        "D'" : y1 * y1 * y1,
        "E"  : y2,
        "E2" : y2 * y2,
        "E'" : y2 * y2 * y2,
        "U"  : y3 * y3 * y3,
        "U2" : y3 * y3,
        "U'" : y3,
        "B"  : z1,
        "B2" : z1 * z1,
        "B'" : z1 * z1 * z1,
        "S"  : z2 * z2 * z2,
        "S2" : z2 * z2,
        "S'" : z2,
        "F"  : z3 * z3 * z3,
        "F2" : z3 * z3,
        "F'" : z3,

        "l"  : x1 * x2,
        "l2" : x1 * x1 * x2 * x2,
        "l'" : x1 * x1 * x1 * x2 * x2 * x2,
        "r"  : x2 * x2 * x2 * x3 * x3 * x3,
        "r2" : x2 * x2 * x3 * x3,
        "r'" : x2 * x3,
        "d"  : y1 * y2,
        "d2" : y1 * y1 * y2 * y2,
        "d'" : y1 * y1 * y1 * y2 * y2 * y2,
        "u"  : y2 * y2 * y2 * y3 * y3 * y3,
        "u2" : y2 * y2 * y3 * y3,
        "u'" : y2 * y3,
        "b"  : z1 * z2,
        "b2" : z1 * z1 * z2 * z2,
        "b'" : z1 * z1 * z1 * z2 * z2 * z2,
        "f"  : z2 * z2 * z2 * z3 * z3 * z3,
        "f2" : z2 * z2 * z3 * z3,
        "f'" : z2 * z3,

        "x"  : x1 * x1 * x1 * x2 * x2 * x2 * x3 * x3 * x3,
        "x2" : x1 * x1 * x2 * x2 * x3 * x3,
        "x'" : x1 * x2 * x3,
        "y"  : y1 * y1 * y1 * y2 * y2 * y2 * y3 * y3 * y3,
        "y2" : y1 * y1 * y2 * y2 * y3 * y3,
        "y'" : y1 * y2 * y3,
        "z"  : z1 * z1 * z1 * z2 * z2 * z2 * z3 * z3 * z3,
        "z2" : z1 * z1 * z2 * z2 * z3 * z3,
        "z'" : z1 * z2 * z3
    }
    algorithms = {
        # 2-Look OLL
        "OLL-Dot"      : "F R U R' U' F' f R U R' U' f'",
        "OLL-I-Shape"  : "F R U R' U' F'",
        "OLL-L-Shape"  : "f R U R' U' f'",
        "OLL-Antisune" : "R U2 R' U' R U' R'",
        "OLL-H"        : "R U R' U R U' R' U R U2 R'",
        "OLL-L"        : "F R' F' r U R U' r'",
        "OLL-Pi"       : "R U2 R2 U' R2 U' R2 U2 R",
        "OLL-Sune"     : "R U R' U R U2 R'",
        "OLL-T"        : "r U R' U' r' F R F'",
        "OLL-U"        : "R2 D R' U2 R D' R' U2 R'",

        "OLL-1"  : "R U2 R2 F R F' U2 R' F R F'",
        "OLL-2"  : "r U r' U2 r U2 R' U2 R U' r'",
        "OLL-3"  : "r' R2 U R' U r U2 r' U M'",
        "OLL-4"  : "M U' r U2 r' U' R U' R' M'",
        "OLL-5"  : "l' U2 L U L' U l",
        "OLL-6"  : "r U2 R' U' R U' r'",
        "OLL-7"  : "r U R' U R U2 r'",
        "OLL-8"  : "l' U' L U' L' U2 l",
        "OLL-9"  : "R U R' U' R' F R2 U R' U' F'",
        "OLL-10" : "R U R' U R' F R F' R U2 R'",
        "OLL-11" : "r U R' U R' F R F' R U2 r'",
        "OLL-12" : "M' R' U' R U' R' U2 R U' R r'",
        "OLL-13" : "F U R U' R2 F' R U R U' R'",
        "OLL-14" : "R' F R U R' F' R F U' F'",
        "OLL-15" : "l' U' l L' U' L U l' U l",
        "OLL-16" : "r U r' R U R' U' r U' r'",
        "OLL-17" : "F R' F' R2 r' U R U' R' U' M'",
        "OLL-18" : "r U R' U R U2 r2 U' R U' R' U2 r",
        "OLL-19" : "r' R U R U R' U' M' R' F R F'",
        "OLL-20" : "r U R' U' M2 U R U' R' U' M'",
        "OLL-21" : "R U2 R' U' R U R' U' R U' R'",
        "OLL-22" : "R U2 R2 U' R2 U' R2 U2 R",
        "OLL-23" : "R2 D' R U2 R' D R U2 R",
        "OLL-24" : "r U R' U' r' F R F'",
        "OLL-25" : "F' r U R' U' r' F R",
        "OLL-26" : "R U2 R' U' R U' R'",
        "OLL-27" : "R U R' U R U2 R'",
        "OLL-28" : "r U R' U' r' R U R U' R'",
        "OLL-29" : "R U R' U' R U' R' F' U' F R U R'",
        "OLL-30" : "F R' F R2 U' R' U' R U R' F2",
        "OLL-31" : "R' U' F U R U' R' F' R",
        "OLL-32" : "L U F' U' L' U L F L'",
        "OLL-33" : "R U R' U' R' F R F'",
        "OLL-34" : "R U R2 U' R' F R U R U' F'",
        "OLL-35" : "R U2 R2 F R F' R U2 R'",
        "OLL-36" : "L' U' L U' L' U L U L F' L' F",
        "OLL-37" : "F R' F' R U R U' R'",
        "OLL-38" : "R U R' U R U' R' U' R' F R F'",
        "OLL-39" : "L F' L' U' L U F U' L'",
        "OLL-40" : "R' F R U R' U' F' U R",
        "OLL-41" : "R U R' U R U2 R' F R U R' U' F'",
        "OLL-42" : "R' U' R U' R' U2 R F R U R' U' F'",
        "OLL-43" : "F' U' L' U L F",
        "OLL-44" : "F U R U' R' F'",
        "OLL-45" : "F R U R' U' F'",
        "OLL-46" : "R' U' R' F R F' U R",
        "OLL-47" : "R' U' R' F R F' R' F R F' U R",
        "OLL-48" : "F R U R' U' R U R' U' F'",
        "OLL-49" : "r U' r2 U r2 U r2 U' r",
        "OLL-50" : "r' U r2 U' r2 U' r2 U r'",
        "OLL-51" : "F U R U' R' U R U' R' F'",
        "OLL-52" : "R U R' U R U' B U' B' R'",
        "OLL-53" : "l' U2 L U L' U' L U L' U l",
        "OLL-54" : "r U2 R' U' R U R' U' R U' r'",
        "OLL-55" : "R' F R U R U' R2 F' R2 U' R' U R U R'",
        "OLL-56" : "r' U' r U' R' U R U' R' U R r' U r",
        "OLL-57" : "R U R' U' M' U R U' r'",

        "PLL-Aa" : "x L2 D2 L' U' L D2 L' U L'",
        "PLL-F"  : "R' U' F' R U R' U' R' F R2 U' R' U' R U R' U R",
        "PLL-Ga" : "R2 U R' U R' U' R U' R2 U' D R' U R D'",
        "PLL-Gb" : "R' U' R U D' R2 U R' U R U' R U' R2 D",
        "PLL-Jb" : "R U R' F' R U R' U' R' F R2 U' R'",
        "PLL-T"  : "R U R' U' R' F R2 U' R' U' R U R' F'",
        "PLL-UaM": "M2 U M U2 M' U M2",
        "PLL-UaR": "R U' R U R U R U' R' U' R2",
        "PLL-UbM": "M2 U' M U2 M' U' M2",
        "PLL-UbR": "R2 U R U R' U' R' U' R' U R'",
        "PLL-V"  : "R' U R' U' y R' F' R2 U' R' U R' F R F",
        "PLL-Y"  : "F R U' R' U' R U R' F' R U R' U' R' F R F'",
        "PLL-Z"  : "M' U M2 U M2 U M' U2 M2",
    }

    def __init__ ( self ) :
        self.state = PermutationCube()

    def apply_operations ( self, operations ) :
        for operation in operations.split(" ") :
            if operation == "|" :
                self.state.state.dump()
            elif operation in Cube3.algorithms :
                self.apply_operations(Cube3.algorithms[operation])
            elif operation in Cube3.operations :
                self.state *= Cube3.operations[operation]
            else :
                print(f"Unknown operation: {operation}")

if __name__ == "__main__" :
    cube = Cube3()
    cube.apply_operations("R' U' F R' F' R F' R2 U R F' D2 F' U2 F2 R2 B U2 D2 R2 D2 B L D2 R' U' F")

    # cube.apply_operations("U B R B R' B | D F2 R' F' R D' | F' U' F' U R F' R' | U' F' U F L' F L | F U' F' U F2 U' F' U | U F L F' L' U' | R F R' F R F2 R' | L F L' F' L' U L2 F' L' F' L F L' U' | F2 M2 F' M F2 M' F' M2")
    # cube.apply_operations("z2 | R2 B2 L D' B L D | y L' U2 L R' U R | U' R U R' U R U R' | y' U L' U' L | R U R' U2 R U R' U' R U R' | F R U R' U' F' | U2 R' F R B' R' F' R B | R U' R' U' R U R D R' U' R D' R' U2 R' | U' z2")
    # cube.apply_operations("y' | L2 B L R' F R | y' L U2 L' U' L U L' | U R' U2 R U' R' U' R | y' R U R' U' R U R' U2 f R f' | y' U' R' U2 R U' R' U R | U' F R U R' U' F' | R U R' U R U2 R' | R' U' F' R U R' U' R' F | R2 U' R' U' R U R' U R")

    cube.state.state.dump()

    # cube.split_view()
