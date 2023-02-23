
class Cube :
    """
        A Cube is an arbitrarily sized cube of pieces.
        The state of the cube can be expressed as a full nested matrix of positions, holding the piece and orientation.

        Because the position of a piece can be determined by its orientation, it is possible to express the entire state of the cube as a single string of rotation letters. All 24 axis aligned rotations can be represented by a single letter, or using the two letter notation of the top and front face colors relative to the root white-green color.

        This is internally kept as a dictionary of piece names to rotation operations, as to not be tied to a specific order of pieces.
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
        "WG": {"sym": "-", "dist": 0, "dec": ""},       # identity
        "BW": {"sym": "i", "dist": 1, "dec": "i"},      # i
        "GY": {"sym": "f", "dist": 1, "dec": "iii"},    # (iii)
        "WO": {"sym": "j", "dist": 1, "dec": "j"},      # j
        "WR": {"sym": "g", "dist": 1, "dec": "jjj"},    # (jjj)
        "RG": {"sym": "k", "dist": 1, "dec": "k"},      # k
        "OG": {"sym": "h", "dist": 1, "dec": "kkk"},    # (kkk)
        "YB": {"sym": "l", "dist": 2, "dec": "ii"},     # ii
        "WB": {"sym": "m", "dist": 2, "dec": "jj"},     # jj
        "YG": {"sym": "n", "dist": 2, "dec": "kk"},     # kk
        "GO": {"sym": "p", "dist": 2, "dec": "jk"},     # (iii)-j-k
        "BR": {"sym": "q", "dist": 2, "dec": "ki"},     # i-(jjj)-k
        "BO": {"sym": "r", "dist": 2, "dec": "ij"},     # i-j-(kkk)
        "GR": {"sym": "s", "dist": 2, "dec": "iiijjj"}, # (iii)-(jjj)-(kkk)
        "OW": {"sym": "t", "dist": 2, "dec": "ikkk"},   # i-(kkk)-(jjj)
        "RY": {"sym": "u", "dist": 2, "dec": "kjjj"},   # (iii)-k-(jjj)
        "OY": {"sym": "v", "dist": 2, "dec": "jiii"},   # (iii)-(kkk)-j
        "RW": {"sym": "w", "dist": 2, "dec": "ik"},     # i-k-j
        "YO": {"sym": "a", "dist": 3, "dec": "iij"},    # iij
        "RB": {"sym": "b", "dist": 3, "dec": "iik"},    # iik
        "GW": {"sym": "c", "dist": 3, "dec": "jji"},    # jji
        "OB": {"sym": "x", "dist": 3, "dec": "jjk"},    # jjk
        "BY": {"sym": "y", "dist": 3, "dec": "kki"},    # kki
        "YR": {"sym": "z", "dist": 3, "dec": "kkj"},    # kkj
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

        "OLL-3"  : "a: r' R2 U R' U r U2 r' U M'",
        "OLL-4"  : "a: M U' r U2 r' U' R U' R' M'",
        "OLL-8"  : "a: l' U' L U' L' U2 l",
        "OLL-9"  : "a: R U R' U' R' F R2 U R' U' F'",
        "OLL-12" : "a: M' R' U' R U' R' U2 R U' R r'",
        "OLL-15" : "a: l' U' l L' U' L U l' U l",
        "OLL-16" : "a: r U r' R U R' U' r U' r'",
        "OLL-17" : "a: F R' F' R2 r' U R U' R' U' M'",
        "OLL-31" : "a: R' U' F U R U' R' F' R",
        "OLL-32" : "a: L U F' U' L' U L F L'",
        "OLL-44" : "a: F U R U' R' F'",
        "OLL-53" : "a: l' U2 L U L' U' L U L' U l",

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
    }

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
        print(f"{self.repr_orient_str()} | {self.name} | {self.hist}")

    def find_pos ( self, piece, orientation ) :
        for step in Cube.operation_table[orientation]["dec"] :
            piece = Cube.position_table[piece]["ijk".index(step)]
        return piece

    def rotate ( self, orientation, rotation ) :
        for step in Cube.operation_table[rotation]["dec"] :
            orientation = Cube.rotation_table[orientation]["ijk".index(step)]
        return orientation

    def repr_distance ( self ) :
        return "".join([str(Cube.operation_table[orientation]["dist"]) for orientation in self.state.values()])

    def repr_orient_str ( self ) :
        state = [Cube.operation_table[self.state[piece]]["sym"] for piece in Cube.standard_order]
        try :
            state = "".join(state)
        except TypeError :
            raise Exception(f"Invalid state: {self.state}")
        return state
    
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
                other = other[3:]
                other_cube = Cube()
                for step in other.split(' ') :
                    if step in Cube.algorithms :
                        other_cube *= Cube.algorithms[step]
                    else :
                        raise Exception(f"Invalid step: {step}")
                other_cube.hist = other.split(' ')
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

if __name__ == "__main__" :
    """
         . v   . .   v .   . .  |   f     y     v     .
        .. .s .m .. .- .. kj .. |   m     -     .     .
                                | .. .. .. .r x- m. k. .b 
        .. .. .g -s .j m. .. .b |   .     .     .     .
         . .   c .   i .   w i  |   c     i     .     .
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

# A3a1) The competitor is allotted a maximum of 15 seconds to inspect the puzzle and start the solve.
