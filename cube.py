import math
import random

class Cube :
    """
        A Cube is an arbitrarily sized cube of pieces.
        The state of the cube can be expressed as a full nested matrix of positions, holding the piece and orientation. Because the position of a piece can be determined by its orientation, it is possible to express the entire state of the cube as a single string of rotation letters. All 24 axis aligned rotations can be represented by a single letter, or using the two letter notation of the top and front face colors relative to the root white-green color. This is internally kept as a dictionary of piece names to rotation operations, as to not be tied to a specific order of pieces.

        The configuration of the Cube can be seen as a point within a group. Moves acting as transformations on the Cube give us other points within this group. Transformations are closed under composition, not cummutative, and every state is itself a transformation. Transformations move the state within a cyclic statespace, meaning that all states are trivially invertible and some root of the identity state, which we can arbitrarily assign to the "solved" state for convenience.

        Given the set of basic quarter turns as the generators of the group, we can define the "distance" between two cubes as the minimum amount of moves to go between them, or the distance between the cubes in a full state graph. Because the graph contains 43 quintillion states, it is obviously not possible to search the graph for the shortest path. Even with something like meet in the middle, this is too slow. The best possible solution would be to either figure out a proper expression of distance, or to find any solution and then figure out how to iteratively reduce it.

        Every basic move influences nine pieces, but since the center pieces have only one visible side, their orientation is ambiguous, so while you can speak of "even" and "odd" distanced cubes, this is practically irrelevant.

        Technically, because of parity, the six centers could be combined into a single piece and one edge and corner could be omitted.
    """

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
        "OLL-L=Shape"  : "a: f R U R' U' f'",
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
    """
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
    """

    
    scrambler = Scrambler()
    for i in range(1) :
        cube = scrambler.new()
        cube.dump()
        solver = Solver(cube)
        solver.solve_cross()
    for cube in scrambler.scrambles :
        print(cube)
    

    """
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
    """

    cube = Cube("base", "---- ---- ---- ---- ---- ------")
    for i in range(1) :
        scramble = scrambler.new()
        print(f"Distance check: {cube.distance(scramble)}")

    """
    for i in range(57) :
        alg = Cube.algorithms[f"OLL-{i+1}"]
        cube = Cube("init") * alg
        cube.name = f"OLL-{i+1}"
        print(cube)
    """

    # (Cube("init", "s-ij---- -jmj-------- ------") * "a: OLL-L y2 PLL-UbM y2").dump()
    (Cube("init", "tbry---- ------------ ------") * "a: U2 R' F2 R U2 R U2 R' F2 U' R U' R' U PLL-UbM U").dump()
    # U2 OLL-Pi U' PLL-Aa x' U PLL-UaM
    # U2 (R U2 R2 U' R2 U' R2 U2 R) U' (x L2 D2 L' U' L D2 L' U L') x' U (M2 U M U2 M' U M2)
    # U2 R' F2 R U2 R U2 R' F2 U' R U' R' U M2 U M U2 M' U M2 U

    """
         . v   . .   v .   y .  |   .     .     .     .
        .g ms .m jb .- g. kj -. |   .     -     .     j
                                | .. .. .j .. .- m. .. -. 
        .- j. .g -s .j mr .m gb |   -     .     .     .
         t .   c .   i .   w i  |   .     .     .     .
    """

# A3a1) The competitor is allotted a maximum of 15 seconds to inspect the puzzle and start the solve.
