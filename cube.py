
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

    def __init__ ( self, state = "-------- ------------ ------" ) :
        if isinstance(state, str) :
            state = state.replace(" ", "")
            self.state = {}
            for i in range(len(state)) :
                for k, v in Cube.operation_table.items() :
                    if v["sym"] == state[i] :
                        self.state[Cube.standard_order[i]] = k
                        break
        elif isinstance(state, dict) :
            self.state = state

    def find_pos ( self, piece, orientation ) :
        for step in Cube.operation_table[orientation]["dec"] :
            piece = Cube.position_table[piece]["ijk".index(step)]
        return piece

    def rotate ( self, orientation, rotation ) :
        for step in Cube.operation_table[rotation]["dec"] :
            orientation = Cube.rotation_table[orientation]["ijk".index(step)]
        return orientation

    def get_position_color ( self, piece, direction ) :
        pass

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
        if not isinstance(other, Cube) :
            raise Exception("Can only multiply a cube by another cube")
        new_state = {}
        for piece, orientation in self.state.items() :
            pos = self.find_pos(piece, orientation)
            rotation = other.state[pos]
            new_state[piece] = self.rotate(orientation, rotation)
            new_pos = self.find_pos(piece, new_state[piece])
            
        return Cube(new_state)

    def __str__ ( self ) :
        return f"{self.repr_orient_str()} | {self.repr_distance()} | {self.repr_inv_orient_str()}"

class CubeBuilder :

    Wj = Cube("jjjj ---- jjjj ---- ---- j-----")
    Cj = Cube("---- ---- ---- ---- jjjj --jjjj")
    Yj = Cube("---- jjjj ---- jjjj ---- -j----")
    Wg = Cube("gggg ---- gggg ---- ---- g-----")
    Cg = Cube("---- ---- ---- ---- gggg --gggg")
    Yg = Cube("---- gggg ---- gggg ---- -g----")

    Gk = Cube("kk-- kk-- k--- k--- kk-- --k---")
    Ck = Cube("---- ---- --kk --kk ---- kk--kk")
    Bk = Cube("--kk --kk -k-- -k-- --kk ---k--")
    Gh = Cube("hh-- hh-- h--- h--- hh-- --h---")
    Ch = Cube("---- ---- --hh --hh ---- hh--hh")
    Bh = Cube("--hh --hh -h-- -h-- --hh ---h--")

    Oi = Cube("i-i- i-i- --i- --i- i-i- ----i-")
    Ci = Cube("---- ---- ii-- ii-- ---- iiii--")
    Ri = Cube("-i-i -i-i ---i ---i -i-i -----i")
    Of = Cube("f-f- f-f- --f- --f- f-f- ----f-")
    Cf = Cube("---- ---- ff-- ff-- ---- ffff--")
    Rf = Cube("-f-f -f-f ---f ---f -f-f -----f")

    algorithms = {
        "OLL-9" : "R U R' U' R' F R2 U R' U' F'",
        "OLL-15": "l' U' l L' U' L U l' U l",
        "OLL-31": "R' U' F U R U' R' F' R",
        "OLL-32": "L U F' U' L' U L F L'",

        "PLL-T": "R U R' U' R' F R2 U' R' U' R U R' F'",
        "PLL-Y": "F R U' R' U' R U R' F' R U R' U' R' F R F'",
        "PLL-UaM": "M2 U M U2 M' U M2",
        "PLL-UaR": "R U' R U R U R U' R' U' R2",
        "PLL-UbM": "M2 U' M U2 M' U' M2",
        "PLL-UbR": "R2 U R U R' U' R' U' R' U R'",
    }

    def from_alg ( self, alg ) :
        cube = Cube()
        for step in alg.split(' ') :
            if step == "" : continue
            if   step == "R"  : cube *= CubeBuilder.Rf
            elif step == "R'" : cube *= CubeBuilder.Ri
            elif step == "R2" : cube *= CubeBuilder.Rf * CubeBuilder.Rf
            elif step == "L"  : cube *= CubeBuilder.Oi
            elif step == "L'" : cube *= CubeBuilder.Of
            elif step == "l"  : cube *= CubeBuilder.Oi * CubeBuilder.Ci
            elif step == "l'" : cube *= CubeBuilder.Of * CubeBuilder.Cf
            elif step == "U"  : cube *= CubeBuilder.Wg
            elif step == "U'" : cube *= CubeBuilder.Wj
            elif step == "U2" : cube *= CubeBuilder.Wg * CubeBuilder.Wg
            elif step == "F"  : cube *= CubeBuilder.Gh
            elif step == "F'" : cube *= CubeBuilder.Gk
            elif step == "M"  : cube *= CubeBuilder.Ci
            elif step == "M'" : cube *= CubeBuilder.Cf
            elif step == "M2" : cube *= CubeBuilder.Ci * CubeBuilder.Ci
            elif step in CubeBuilder.algorithms :
                cube *= self.from_alg(CubeBuilder.algorithms[step])
            else :
                raise Exception(f"Invalid step: {step}")
        return cube

if __name__ == "__main__" :
    """
    print(f"OLL Sune: {R * U * Rp * U * R * U * U * Rp * U * U}")

    print(f"PLL-Nb: {Rp * U * R * Up * Rp * Fp * Up * F * R * U * Rp * F * Rp * Fp * R * Up * R}")
    PLLT = R * U * Rp * Up * Rp * F * R * R * Up * Rp * Up * R * U * Rp * Fp
    print(f"PLL-T : {PLLT}")
    print(f"PLL-Ua: {M * M * U * M * U * U * Mp * U * M * M}")
    print(f"PLL-Ua: {R * Up * R * U * R * U * R * Up * Rp * Up * R * R}")
    print(f"PLL-Ub: {M * M * Up * M * U * U * Mp * Up * M * M}")
    print(f"PLL-Ub: {R * R * U * R * U * Rp * Up * Rp * Up * Rp * U * Rp}")
    print(f"PLL-Z : {Mp * U * M * M * U * M * M * U * Mp * U * U * M * M * Up}")
    print(f"PLL-H : {M * M * U * M * M * U * U * M * M * U * M * M}")
    print(f"PLL-H : {M * M * Up * M * M * U * U * M * M * Up * M * M}")
    """

    print(f"{Cube('-myi---- crgm-------- ------') * CubeBuilder().from_alg('OLL-32 PLL-T')}")
    print(f"{Cube('tjmy---- c-x--------- ------') * CubeBuilder().from_alg('OLL-31 PLL-Y')}")
    print(f"{Cube('v-ik---- sjgw-------- ------') * CubeBuilder().from_alg('OLL-9 U PLL-T U PLL-UaR U')}")
    print(f"{Cube('pbtj---- cgvm-------- ------') * CubeBuilder().from_alg('OLL-15 U PLL-T U2')}")
    # print(f"{Cube('????---- ????-------- ------') * CubeBuilder().from_alg('')}")
