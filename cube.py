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

class Cube3 ( Cube ) :

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
        Because proper matrix multiplication with a large matrix is slow, this is internally done by tracking index permutation cycles.
    """

    def __init__ ( self, size ) :
        self.size = size
        self.state = [i for i in range(size)]

    def dump ( self ) :
        for i in range(self.size) :
            print(f"{i:3} | {self.state[i]*'-'}1{(self.size-self.state[i]-1)*'-'} | {self.state[i]:3}")

class PermutationCube :
    """
        A Permutation Cube is a cube represented by a Permutation Matrix.
        Each set of four rows represents a cubicle, and each set of four columns represents a cubie.
        The four parts are the four center crossing diagonals, such that the 4x4 submatrix represents the orientation of the cubie.
    """

    def __init__ ( self, size ) :
        self.size = size
        self.state = PermutationMatrix(4 * size ** 3)

class MOCube :

    def __init__ ( self, size ) :
        self.size = size ** 3
        self.state = [[1 if i == j else 0 for j in range(4 * self.size)] for i in range(4 * self.size)]

    def dump ( self ) :
        print("\n".join(["".join([str(x) for x in row]) for row in self.state]))

if __name__ == "__main__" :
    cube = PermutationMatrix(4*3**3)
    cube.dump()
    # cube = Cube3()
    # cube = Cube3()
    # cube.apply_operations("R' U' F R' F' R F' R2 U R F' D2 F' U2 F2 R2 B U2 D2 R2 D2 B L D2 R' U' F")
    # cube.set_state("hbacykkhriwzx-r---gwbu-nb-g", [[19, 11, 3, 21, 7, 23, 9, 1], [18, 26, 8, 24, 20, 6]])
    # cube.apply_operations("F2 D' F2") # Green Cross
    
    # cube.apply_operations("U B R B R' B | D F2 R' F' R D' | F' U' F' U R F' R' | U' F' U F L' F L | F U' F' U F2 U' F' U | U F L F' L' U' | R F R' F R F2 R' | L F L' F' L' U L2 F' L' F' L F L' U' | F2 M2 F' M F2 M' F' M2")
    # cube.apply_operations("z2 | R2 B2 L D' B L D | y L' U2 L R' U R | U' R U R' U R U R' | y' U L' U' L | R U R' U2 R U R' U' R U R' | F R U R' U' F' | U2 R' F R B' R' F' R B | R U' R' U' R U R D R' U' R D' R' U2 R' | U' z2")
    # cube.apply_operations("y' | L2 B L R' F R | y' L U2 L' U' L U L' | U R' U2 R U' R' U' R | y' R U R' U' R U R' U2 f R f' | y' U' R' U2 R U' R' U R | U' F R U R' U' F' | R U R' U R U2 R' | R' U' F' R U R' U' R' F | R2 U' R' U' R U R' U R")
    # cube.dump()

    # cube.split_view()
    """
    graph = {}

    for i in range(1000) :
        random_move = random.choice(["R", "R2", "R'", "L", "L2", "L'", "U", "U2", "U'", "D", "D2", "D'", "F", "F2", "F'", "B", "B2", "B'"])
        prev = "".join(cube.pieces)
        cube.apply_operation(random_move)
        if prev not in graph :
            graph[prev] = {}
        graph[prev][random_move] = "".join(cube.pieces)
    
    for state in graph :
        print(f"{state} -> {graph[state]}")
    """
    """
    U R' U' D' (Green Cross)
    B' R B R'
    B L B' L' L' B' L
    B L B L'
    B2 R' B2 R B2 R' B R (F2L)
    """


"""

        A Cube is an arbitrarily sized cube of pieces.
        The state of the cube can be expressed as a full nested matrix of positions, holding the piece and orientation. Because the position of a piece can be determined by its orientation, it is possible to express the entire state of the cube as a single string of rotation letters. All 24 axis aligned rotations can be represented by a single letter, or using the two letter notation of the top and front face colors relative to the root white-green color. This is internally kept as a dictionary of piece names to rotation operations, as to not be tied to a specific order of pieces.

        The configuration of the Cube can be seen as a point within a group. Moves acting as transformations on the Cube give us other points within this group. Transformations are closed under composition, not cummutative, and every state is itself a transformation. Transformations move the state within a cyclic statespace, meaning that all states are trivially invertible and some root of the identity state, which we can arbitrarily assign to the "solved" state for convenience.

        Given the set of basic quarter turns as the generators of the group, we can define the "distance" between two cubes as the minimum amount of moves to go between them, or the distance between the cubes in a full state graph. Because the graph contains 43 quintillion states, it is obviously not possible to search the graph for the shortest path. Even with something like meet in the middle, this is too slow. The best possible solution would be to either figure out a proper expression of distance, or to find any solution and then figure out how to iteratively reduce it.

        Every basic move influences nine pieces, but since the center pieces have only one visible side, their orientation is ambiguous, so while you can speak of "even" and "odd" distanced cubes, this is practically irrelevant.

        Technically, because of parity, the six centers could be combined into a single piece and one edge and corner could be omitted.
    

    standard_order = ["WGO", "WGR", "WBO", "WBR", "YGO", "YGR", "YBO", "YBR", "WG", "WB", "WO", "WR", "YG", "YB", "YO", "YR", "GO", "GR", "BO", "BR", "W", "Y", "G", "B", "O", "R"]

    position_table = {
        #WG        i      j      k
        "WGO" : ["YGO", "WGR", "YGO"],
        "WGR" : ["YGR", "WBR", "WGO"],
        "WBO" : ["WGO", "WGO", "YBO"],
        "WBR" : ["WGR", "WBO", "WBO"],
        "YGO" : ["YBO", "YGR", "YGR"],
        "YGR" : ["YBR", "YBR", "WGR"],
        "YBO" : ["WBO", "YGO", "YBR"],
        "YBR" : ["WBR", "YBO", "WBR"],
        "WG"  : [ "YG",  "WR",  "GO"],
        "WB"  : [ "WG",  "WO",  "BO"],
        "WO"  : [ "GO",  "WG",  "YO"],
        "WR"  : [ "GR",  "WB",  "WO"],
        "YG"  : [ "YB",  "YR",  "GR"],
        "YB"  : [ "WB",  "YO",  "BR"],
        "YO"  : [ "BO",  "YG",  "YR"],
        "YR"  : [ "BR",  "YB",  "WR"],
        "GO"  : [ "YO",  "GR",  "YG"],
        "GR"  : [ "YR",  "BR",  "WG"],
        "BO"  : [ "WO",  "GO",  "YB"],
        "BR"  : [ "WR",  "BO",  "WB"],
        "W"   : [  "G",   "W",   "O"],
        "Y"   : [  "B",   "Y",   "R"],
        "G"   : [  "Y",   "R",   "G"],
        "B"   : [  "W",   "O",   "B"],
        "O"   : [  "O",   "G",   "Y"],
        "R"   : [  "R",   "B",   "W"],
    }
    rotation_table = {
        "i"  : ["i", "k", "jjj"],
        "j"  : ["kkk", "j", "i"],
        "k"  : ["j", "iii", "k"],
        #         i     j     k
        "WG" : ["BW", "WO", "RG"],
        "WB" : ["GW", "WR", "OB"],
        "WO" : ["RW", "WB", "GO"],
        "WR" : ["OW", "WG", "BR"],

        "YG" : ["BY", "YR", "OG"],
        "YB" : ["GY", "YO", "RB"],
        "YO" : ["RY", "YG", "BO"],
        "YR" : ["OY", "YB", "GR"],

        "GW" : ["YG", "GR", "OW"],
        "GY" : ["WG", "GO", "RY"],
        "GO" : ["RG", "GW", "YO"],
        "GR" : ["OG", "GY", "WR"],

        "BW" : ["YB", "BO", "RW"],
        "BY" : ["WB", "BR", "OY"],
        "BO" : ["RB", "BY", "WO"],
        "BR" : ["OB", "BW", "YR"],

        "OW" : ["YO", "OG", "BW"],
        "OY" : ["WO", "OB", "GY"],
        "OG" : ["BO", "OY", "WG"],
        "OB" : ["GO", "OW", "YB"],

        "RW" : ["YR", "RB", "GW"],
        "RY" : ["WR", "RG", "BY"],
        "RG" : ["BR", "RW", "YG"],
        "RB" : ["GR", "RY", "WB"],
    }
    rotation_shorthand = {
        "WG" : "o",
        "BW" : "i",
        "GY" : "f",
        "WO" : "j",
        "WR" : "g",
        "RG" : "k",
        "OG" : "h",
        "YB" : "l",
        "WB" : "m",
        "YG" : "n",
        "GO" : "p",
        "BR" : "q",
        "BO" : "r",
        "GR" : "s",
        "OW" : "t",
        "RY" : "u",
        "OY" : "v",
        "RW" : "w",
        "YO" : "a",
        "RB" : "b",
        "GW" : "c",
        "OB" : "x",
        "BY" : "y",
        "YR" : "z",
    }
    operation_table = {
        "WG": {"sym": "-", "dec": ""},       # identity
        "BW": {"sym": "i", "dec": "i"},      # i
        "GY": {"sym": "f", "dec": "iii"},    # (iii)
        "WO": {"sym": "j", "dec": "j"},      # j
        "WR": {"sym": "g", "dec": "jjj"},    # (jjj)
        "RG": {"sym": "k", "dec": "k"},      # k
        "OG": {"sym": "h", "dec": "kkk"},    # (kkk)
        "YB": {"sym": "l", "dec": "ii"},     # ii
        "WB": {"sym": "m", "dec": "jj"},     # jj
        "YG": {"sym": "n", "dec": "kk"},     # kk
        "GO": {"sym": "p", "dec": "jk"},     # (iii)-j-k
        "BR": {"sym": "q", "dec": "ki"},     # i-(jjj)-k
        "BO": {"sym": "r", "dec": "ij"},     # i-j-(kkk)
        "GR": {"sym": "s", "dec": "iiijjj"}, # (iii)-(jjj)-(kkk)
        "OW": {"sym": "t", "dec": "ikkk"},   # i-(kkk)-(jjj)
        "RY": {"sym": "u", "dec": "kjjj"},   # (iii)-k-(jjj)
        "OY": {"sym": "v", "dec": "jiii"},   # (iii)-(kkk)-j
        "RW": {"sym": "w", "dec": "ik"},     # i-k-j
        "YO": {"sym": "a", "dec": "iij"},    # iij
        "RB": {"sym": "b", "dec": "iik"},    # iik
        "GW": {"sym": "c", "dec": "jji"},    # jji
        "OB": {"sym": "x", "dec": "jjk"},    # jjk
        "BY": {"sym": "y", "dec": "kki"},    # kki
        "YR": {"sym": "z", "dec": "kkj"},    # kkj
    }
    orientation_distance_table = {
        "-" : {"-": 0, "i": 1, "f": 1, "j": 1, "g": 1, "k": 1, "h": 1, "l": 2, "m": 2, "n": 2, "p": 2, "q": 2, "r": 2, "s": 2, "t": 2, "u": 2, "v": 2, "w": 2, "a": 3, "b": 3, "c": 3, "x": 3, "y": 3, "z": 3},
    }

    algorithms = {
        "U" : "c: gggg ---- gggg ---- ---- g-----", # Wg
        "U'": "c: jjjj ---- jjjj ---- ---- j-----", # Wj
        "U2": "c: mmmm ---- mmmm ---- ---- m-----", # Wm
        "D" : "c: ---- jjjj ---- jjjj ---- -j----", # Yj
        "D'": "c: ---- gggg ---- gggg ---- -g----", # Yg
        "D2": "c: ---- mmmm ---- mmmm ---- -m----", # Ym
        "R" : "c: -f-f -f-f ---f ---f -f-f -----f", # Rf
        "R'": "c: -i-i -i-i ---i ---i -i-i -----i", # Ri
        "R2": "c: -l-l -l-l ---l ---l -l-l -----l", # Rl
        "L" : "c: i-i- i-i- --i- --i- i-i- ----i-", # Oi
        "L'": "c: f-f- f-f- --f- --f- f-f- ----f-", # Of
        "L2": "c: l-l- l-l- --l- --l- l-l- ----l-", # Ol
        "F" : "c: hh-- hh-- h--- h--- hh-- --h---", # Gh
        "F'": "c: kk-- kk-- k--- k--- kk-- --k---", # Gk
        "F2": "c: nn-- nn-- n--- n--- nn-- --n---", # Gn
        "B" : "c: --kk --kk -k-- -k-- --kk ---k--", # Bk
        "B'": "c: --hh --hh -h-- -h-- --hh ---h--", # Bh
        "B2": "c: --nn --nn -n-- -n-- --nn ---n--", # Bn

        "r" : "c: -f-f -f-f ff-f ff-f -f-f ffff-f", # R M'
        "r'": "c: -i-i -i-i ii-i ii-i -i-i iiiii-", # R' M
        "r2": "c: -l-l -l-l ll-l ll-l -l-l lllll-", # R2 M2
        "l" : "c: i-i- i-i- iii- iii- i-i- iiiii-", # L M
        "l'": "c: f-f- f-f- fff- fff- f-f- fffff-", # L' M'
        "l2": "c: l-l- l-l- lll- lll- l-l- lllll-", # L2 M2

        "x" : "c: ffff ffff ffff ffff ffff ffffff", # Ff
        "x'": "c: iiii iiii iiii iiii iiii iiiiii", # Fi
        "y" : "c: gggg gggg gggg gggg gggg gggggg", # Fg
        "y2": "c: mmmm mmmm mmmm mmmm mmmm mmmmmm", # Fm
        "y'": "c: jjjj jjjj jjjj jjjj jjjj jjjjjj", # Fj
        "z" : "c: hhhh hhhh hhhh hhhh hhhh hhhhhh", # Fh
        "z'": "c: kkkk kkkk kkkk kkkk kkkk kkkkkk", # Fk

        "M" : "c: ---- ---- ii-- ii-- ---- iiii--", # Ci
        "M'": "c: ---- ---- ff-- ff-- ---- ffff--", # Cf
        "M2": "c: ---- ---- ll-- ll-- ---- llll--", # Cl
        "E" : "c: ---- ---- ---- ---- jjjj --jjjj", # Cj
        "E'": "c: ---- ---- ---- ---- gggg --gggg", # Cg
        "S" : "c: ---- ---- --hh --hh ---- hh--hh", # Ch
        "S'": "c: ---- ---- --kk --kk ---- kk--kk", # Ck

        # 2-Look OLL
        "OLL-Dot"      : "a: F R U R' U' F' f R U R' U' f'",
        "OLL-I-Shape"  : "a: F R U R' U' F'",
        "OLL-L-Shape"  : "a: f R U R' U' f'",
        "OLL-Antisune" : "a: R U2 R' U' R U' R'",
        "OLL-H"        : "a: R U R' U R U' R' U R U2 R'",
        "OLL-L"        : "a: F R' F' r U R U' r'",
        "OLL-Pi"       : "a: R U2 R2 U' R2 U' R2 U2 R",
        "OLL-Sune"     : "a: R U R' U R U2 R'",
        "OLL-T"        : "a: r U R' U' r' F R F'",
        "OLL-U"        : "a: R2 D R' U2 R D' R' U2 R'",

        "OLL-1"  : "a: R U2 R2 F R F' U2 R' F R F'",
        "OLL-2"  : "a: r U r' U2 r U2 R' U2 R U' r'",
        "OLL-3"  : "a: r' R2 U R' U r U2 r' U M'",
        "OLL-4"  : "a: M U' r U2 r' U' R U' R' M'",
        "OLL-5"  : "a: l' U2 L U L' U l",
        "OLL-6"  : "a: r U2 R' U' R U' r'",
        "OLL-7"  : "a: r U R' U R U2 r'",
        "OLL-8"  : "a: l' U' L U' L' U2 l",
        "OLL-9"  : "a: R U R' U' R' F R2 U R' U' F'",
        "OLL-10" : "a: R U R' U R' F R F' R U2 R'",
        "OLL-11" : "a: r U R' U R' F R F' R U2 r'",
        "OLL-12" : "a: M' R' U' R U' R' U2 R U' R r'",
        "OLL-13" : "a: F U R U' R2 F' R U R U' R'",
        "OLL-14" : "a: R' F R U R' F' R F U' F'",
        "OLL-15" : "a: l' U' l L' U' L U l' U l",
        "OLL-16" : "a: r U r' R U R' U' r U' r'",
        "OLL-17" : "a: F R' F' R2 r' U R U' R' U' M'",
        "OLL-18" : "a: r U R' U R U2 r2 U' R U' R' U2 r",
        "OLL-19" : "a: r' R U R U R' U' M' R' F R F'",
        "OLL-20" : "a: r U R' U' M2 U R U' R' U' M'",
        "OLL-21" : "a: R U2 R' U' R U R' U' R U' R'",
        "OLL-22" : "a: R U2 R2 U' R2 U' R2 U2 R",
        "OLL-23" : "a: R2 D' R U2 R' D R U2 R",
        "OLL-24" : "a: r U R' U' r' F R F'",
        "OLL-25" : "a: F' r U R' U' r' F R",
        "OLL-26" : "a: R U2 R' U' R U' R'",
        "OLL-27" : "a: R U R' U R U2 R'",
        "OLL-28" : "a: r U R' U' r' R U R U' R'",
        "OLL-29" : "a: R U R' U' R U' R' F' U' F R U R'",
        "OLL-30" : "a: F R' F R2 U' R' U' R U R' F2",
        "OLL-31" : "a: R' U' F U R U' R' F' R",
        "OLL-32" : "a: L U F' U' L' U L F L'",
        "OLL-33" : "a: R U R' U' R' F R F'",
        "OLL-34" : "a: R U R2 U' R' F R U R U' F'",
        "OLL-35" : "a: R U2 R2 F R F' R U2 R'",
        "OLL-36" : "a: L' U' L U' L' U L U L F' L' F",
        "OLL-37" : "a: F R' F' R U R U' R'",
        "OLL-38" : "a: R U R' U R U' R' U' R' F R F'",
        "OLL-39" : "a: L F' L' U' L U F U' L'",
        "OLL-40" : "a: R' F R U R' U' F' U R",
        "OLL-41" : "a: R U R' U R U2 R' F R U R' U' F'",
        "OLL-42" : "a: R' U' R U' R' U2 R F R U R' U' F'",
        "OLL-43" : "a: F' U' L' U L F",
        "OLL-44" : "a: F U R U' R' F'",
        "OLL-45" : "a: F R U R' U' F'",
        "OLL-46" : "a: R' U' R' F R F' U R",
        "OLL-47" : "a: R' U' R' F R F' R' F R F' U R",
        "OLL-48" : "a: F R U R' U' R U R' U' F'",
        "OLL-49" : "a: r U' r2 U r2 U r2 U' r",
        "OLL-50" : "a: r' U r2 U' r2 U' r2 U r'",
        "OLL-51" : "a: F U R U' R' U R U' R' F'",
        "OLL-52" : "a: R U R' U R U' B U' B' R'",
        "OLL-53" : "a: l' U2 L U L' U' L U L' U l",
        "OLL-54" : "a: r U2 R' U' R U R' U' R U' r'",
        "OLL-55" : "a: R' F R U R U' R2 F' R2 U' R' U R U R'",
        "OLL-56" : "a: r' U' r U' R' U R U' R' U R r' U r",
        "OLL-57" : "a: R U R' U' M' U R U' r'",

        "PLL-Aa" : "a: x L2 D2 L' U' L D2 L' U L'",
        "PLL-F"  : "a: R' U' F' R U R' U' R' F R2 U' R' U' R U R' U R",
        "PLL-Ga" : "a: R2 U R' U R' U' R U' R2 U' D R' U R D'",
        "PLL-Gb" : "a: R' U' R U D' R2 U R' U R U' R U' R2 D",
        "PLL-Jb" : "a: R U R' F' R U R' U' R' F R2 U' R'",
        "PLL-T"  : "a: R U R' U' R' F R2 U' R' U' R U R' F'",
        "PLL-UaM": "a: M2 U M U2 M' U M2",
        "PLL-UaR": "a: R U' R U R U R U' R' U' R2",
        "PLL-UbM": "a: M2 U' M U2 M' U' M2",
        "PLL-UbR": "a: R2 U R U R' U' R' U' R' U R'",
        "PLL-V"  : "a: R' U R' U' y R' F' R2 U' R' U R' F R F",
        "PLL-Y"  : "a: F R U' R' U' R U R' F' R U R' U' R' F R F'",
        "PLL-Z"  : "a: M' U M2 U M2 U M' U2 M2",

        "quick---------jmj--------": "a: U2 PLL-UbM U2"
    }
    static_cache = {}

    def __init__ ( self, name = "", state = "-------- ------------ ------" ) :
        self.name = name
        self.state = {}
        self.hist = []
        if isinstance(state, str) :
            state = state.replace(" ", "")
            for i in range(len(state)) :
                for k, v in Cube.operation_table.items() :
                    if v["sym"] == state[i] :
                        self.state[Cube.standard_order[i]] = k
                        break
                else :
                    raise Exception(f"Invalid state: {state}")
        elif isinstance(state, dict) :
            self.state = state
        else :
            raise Exception(f"Invalid state: {state}")

    def dump ( self ) :
        print(f"{self.name} | {self.hist}")
        for state in [self.repr_orient_str(), self.repr_distance()] :
            print(f"  {state[:4]} {state[4:8]} {state[8:12]} {state[12:16]} {state[16:20]} {state[20:]}")

    def distance ( self, other_cube ) :
        print(f"Distance from {self.name} to {other_cube.name}")
        self.dump()
        other_cube.dump()
        print(f"  {self.repr_distance()} -> {other_cube.repr_distance()}")
        print(f"  {self.repr_orient_str()} -> {other_cube.repr_orient_str()}")
        print(f"  {self.repr_inv_orient_str()} -> {other_cube.repr_inv_orient_str()}")
        # Admissible heuristics are lower bounds on the distance to the goal

        heuristics = []
        # 9 piece heuristics; caps at 26*3/9 = 8.67
        heuristics.append((["WGO", "WGR", "WBO", "WBR", "YGO", "YGR", "YBO", "YBR", "WG", "WB", "WO", "WR", "YG", "YB", "YO", "YR", "GO", "GR", "BO", "BR", "W", "Y", "G", "B", "O", "R"], 9))
        # 8 piece heuristics;
        #  Non-centers; caps at 20*3/8 = 7.5
        heuristics.append((["WGO", "WGR", "WBO", "WBR", "YGO", "YGR", "YBO", "YBR", "WG", "WB", "WO", "WR", "YG", "YB", "YO", "YR", "GO", "GR", "BO", "BR"], 8))
        # 4 piece heuristics
        #  Corners; caps at 8*3/4 = 6
        heuristics.append((["WGO", "WGR", "WBO", "WBR", "YGO", "YGR", "YBO", "YBR"], 4))
        #  Edges heuristic; caps at 12*3/4 = 9
        heuristics.append((["WG", "WB", "WO", "WR", "YG", "YB", "YO", "YR", "GO", "GR", "BO", "BR"], 4))
        # 3 piece heuristics
        # 2 piece heuristics
        #  Split edges; caps at 4*3/2 = 6
        heuristics.append((["WGO", "WBR", "YGR", "YBO"], 2))
        heuristics.append((["WGR", "WBO", "YGO", "YBR"], 2))
        #  Corner-grouped edges; caps at 6*3/2 = 9
        heuristics.append((["WG", "WO", "YB", "YR", "GO", "BR"], 4))
        heuristics.append((["WG", "WR", "YB", "YO", "GR", "BO"], 4))
        heuristics.append((["WB", "WO", "YG", "YR", "BO", "GR"], 4))
        heuristics.append((["WB", "WR", "YG", "YO", "BR", "GO"], 4))
        #  Slice edges; caps at 6*3/2 = 9
        heuristics.append((["WB", "WR", "YG", "YO", "GR", "BO"], 2))
        heuristics.append((["WB", "WO", "YG", "YR", "GO", "BR"], 2))
        heuristics.append((["WG", "WR", "YB", "YO", "GO", "BR"], 2))
        heuristics.append((["WG", "WO", "YB", "YR", "GR", "BO"], 2))

        # 1 piece heuristics

        # Grouped corners cap at 6, grouped edges cap at 9

        for heuristic in heuristics :
            pieces, group_size = heuristic
            result = sum([Cube.orientation_distance_table[Cube.operation_table[self.state[piece]]["sym"]][Cube.operation_table[other_cube.state[piece]]["sym"]] for piece in pieces]) / group_size
            print(f"  {math.ceil(result)}/{math.ceil(len(pieces)*3/group_size)} | {pieces}")
        
        # Independent edge distance heuristics
        # ["WGO", "WGR", "WBO", "WBR", "YGO", "YGR", "YBO", "YBR", "WG", "WB", "WO", "WR", "YG", "YB", "YO", "YR", "GO", "GR", "BO", "BR", "W", "Y", "G", "B", "O", "R"]

        return -1

    def find_pos ( self, piece, orientation ) :
        for step in Cube.operation_table[orientation]["dec"] :
            piece = Cube.position_table[piece]["ijk".index(step)]
        return piece

    def rotate ( self, orientation, rotation ) :
        for step in Cube.operation_table[rotation]["dec"] :
            orientation = Cube.rotation_table[orientation]["ijk".index(step)]
        return orientation

    def repr_distance ( self ) :
        return "".join([str(Cube.orientation_distance_table["-"][Cube.operation_table[orientation]["sym"]]) for orientation in self.state.values()])

    def repr_orient_str ( self ) :
        return "".join([Cube.operation_table[self.state[piece]]["sym"] for piece in Cube.standard_order])
    
    def repr_inv_orient_str ( self ) :
        state = [None]*len(self.state)
        for piece, orientation in self.state.items() :
            pos = self.find_pos(piece, orientation)
            if state[Cube.standard_order.index(pos)] is not None :
                raise Exception(f"Invalid state: {self.state}; {pos} is already occupied by {state[Cube.standard_order.index(pos)]}")
            state[Cube.standard_order.index(pos)] = Cube.operation_table[orientation]["sym"]
        state = "".join(state)
        
        return state

    def __mul__ ( self, other ) :
        if isinstance(other, Cube) :
            new_state = {}
            for piece, orientation in self.state.items() :
                pos = self.find_pos(piece, orientation)
                rotation = other.state[pos]
                new_state[piece] = self.rotate(orientation, rotation)
                
            solution = Cube(self.name, new_state)
            solution.hist = self.hist + other.hist
            return solution
        elif isinstance(other, str) :
            if other.startswith("a: ") :
                if other in Cube.static_cache :
                    return self * Cube.static_cache[other]
                other_list = other[3:].split(' ')
                other_cube = Cube()
                for step in other_list :
                    if step == "" : continue
                    if step in Cube.algorithms :
                        other_cube *= Cube.algorithms[step]
                    else :
                        raise Exception(f"Invalid step: {step}")
                other_cube.hist = other_list
                Cube.static_cache[other] = other_cube
                return self * other_cube

            elif other.startswith("c: ") :
                other = other[3:]
                return self * Cube("", other)
            else :
                raise Exception(f"Invalid algorithm: {other}")
        else :
            raise Exception(f"Invalid operation: {self} * {other}")

    def __str__ ( self ) :
        return f"{self.repr_orient_str()} | {self.repr_distance()} | {self.repr_inv_orient_str()}"

class Scrambler :
    
    def __init__ ( self, options = [["U", "U'", "U2", "D", "D'", "D2"], ["R", "R'", "R2", "L", "L'", "L2"], ["F", "F'", "F2", "B", "B'", "B2"]] ) :
        self.options = options
        self.scrambles = []

    def new ( self ) :
        cube = Cube()
        scramble = []
        prev = -1
        for i in range(20) :
            step = random.randint(0, len(self.options)-1)
            step = (step + 1) % len(self.options) if step == prev else step
            choice = random.choice(self.options[step])
            scramble.append(choice)
            cube *= Cube.algorithms[choice]
            prev = step
        cube.name = "a: " + " ".join(scramble)
        self.scrambles.append(cube)
        return cube

class Solver :
    def __init__ ( self, cube ) :
        self.cube = cube
        self.solution = []

    def recenter ( self, debug = True ) :
        print(f"Scrambler generated cubes dont need recentering; todo later")

    def solve_cross ( self, debug = True ) :
        statestr = self.cube.repr_orient_str()
        print(f"Solving cross for {self.cube.name}")
        print(f"???? ???? ???? {statestr[12:16]} ???? ??????")
        moves = ["R", "R'", "L", "L'", "F", "F'", "B", "B'", "U", "U'", "D", "D'"]
        
    def solve_2_look_oll ( self, debug = True ) :
        print(f"Solving 2 look OLL for {self.cube.name}")
        print(f"  Current state: {self.cube}")

if __name__ == "__main__" :
    ""
    (Cube("init", "-myi---- crgm-------- ------") * "a: OLL-32 PLL-T").dump()
    (Cube("init", "tjmy---- c-x--------- ------") * "a: OLL-31 PLL-Y").dump()
    (Cube("init", "v-ik---- sjgw-------- ------") * "a: OLL-9 U PLL-T U PLL-UaR U").dump()
    (Cube("init", "pbtj---- cgvm-------- ------") * "a: OLL-15 U PLL-T U2").dump()
    (Cube("init", "twvu---- cggk-------- ------") * "a: OLL-53 U PLL-Z U2").dump()
    (Cube("init", "sgrj---- g-tb-------- ------") * "a: OLL-44 U2 PLL-T U PLL-Z").dump()
    (Cube("init", "vpig---- cqg--------- ------") * "a: OLL-8 U PLL-T U' PLL-UbR").dump()
    (Cube("init", "hpgw---- fjmw-------- ------") * "a: OLL-16 U2 PLL-Jb U").dump()
    (Cube("init", "sgvi---- cyxb-------- ------") * "a: OLL-3 U2 PLL-Aa x' U").dump()
    (Cube("init", "s-ij---- crvk-------- ------") * "a: OLL-17 PLL-UbR U").dump()
    (Cube("init", "vcmk---- fixb-------- ------") * "a: OLL-4 U PLL-F").dump()
    (Cube("init", "smjb---- mi-b-------- ------") * "a: OLL-44 U PLL-Ga U").dump()
    (Cube("init", "vs-w---- c-mk-------- ------") * "a: OLL-12 PLL-V y' U'").dump()
    # print(Cube("????---- ????-------- ------") * "a: ")
    ""

    ""
    scrambler = Scrambler()
    for i in range(1) :
        cube = scrambler.new()
        cube.dump()
        solver = Solver(cube)
        solver.solve_cross()
    for cube in scrambler.scrambles :
        print(cube)
    ""

    ""
    (Cube("scramble", "lvhi hvis mipk bxkv uxt- -jk---") * "a: ").dump()
    (Cube("scramble", "iztq cc-- avcm mav- aqq- ggnnl-") * "a: ").dump()
    (Cube("scramble", "bszk uung lmyt bjfk jiqy mmk--f") * "a: ").dump()
    (Cube("scramble", "nbfg mbrm w-uy rlky tqni jg-hii") * "a: ").dump()
    (Cube("scramble", "fyxg jhci hhxg l-mr cypm --nh-l") * "a: ").dump()
    (Cube("scramble", "aygf jaxb wasv sftc aytb -jk-l-") * "a: ").dump()
    (Cube("scramble", "vhlb aa-t llju pxri uivn mmkklf") * "a: ").dump()
    (Cube("scramble", "ussj hvtv qxvp qrpj zhru ---h--") * "a: ").dump()
    (Cube("scramble", "i-c- qrvw lxml awqm rkqg m-hhf-") * "a: ").dump()
    (Cube("scramble", "qwvr yhky bkau fcfl u-cy --nkff") * "a: ").dump()
    ""

    cube = Cube("base", "---- ---- ---- ---- ---- ------")
    cube *= "a: OLL-Pi OLL-Pi"
    cube.dump()

    # PLL-T:  -j-g ---- --mm ---- ---- j-----
    # OLL-T:  s-ij ---- ---- ---- ---- ----if
    #         f-gw ---- ---- ---- ---- ----ll
    # OLL-Pi: vptq ---- mjj- ---- ---- m-----
    #         ---- ---- gmg- ---- ---- ------


    # (Cube("init", "s-ij---- -jmj-------- ------") * "a: OLL-L y2 PLL-UbM y2").dump()
    # (Cube("init", "tbry---- ------------ ------") * "a: U2 R' F2 R U2 R U2 R' F2 U' R U' R' U PLL-UbM U").dump()
    # U2 OLL-Pi U' PLL-Aa x' U PLL-UaM
    # U2 (R U2 R2 U' R2 U' R2 U2 R) U' (x L2 D2 L' U' L D2 L' U L') x' U (M2 U M U2 M' U M2)
    # U2 R' F2 R U2 R U2 R' F2 U' R U' R' U M2 U M U2 M' U M2 U

    ""
         . v   . .   v .   y .  |   .     .     .     .
        .g ms .m jb .- g. kj -. |   .     -     .     j
                                | .. .. .j .. .- m. .. -. 
        .- j. .g -s .j mr .m gb |   -     .     .     .
         t .   c .   i .   w i  |   .     .     .     .
    ""

# A3a1) The competitor is allotted a maximum of 15 seconds to inspect the puzzle and start the solve.

"""
