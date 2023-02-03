
class Cube :
    """
        A Cube is an arbitrarily sized cube of pieces.
        The state of the cube can be expressed as a full nested matrix of positions, holding the piece and orientation.

        Because the position of a piece can be determined by its orientation, it is possible to express the entire state of the cube as a single string of rotation letters. All 24 axis aligned rotations can be represented by a single letter, or using the two letter notation of the top and front face colors relative to the root white-green color.

        This is internally kept as a dictionary of piece names to rotation operations, as to not be tied to a specific order of pieces.
    """
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
        "OW" : "p",
        "OY" : "q",
        "RY" : "r",
        "RW" : "s",
        "GO" : "t",
        "BO" : "u",
        "BR" : "v",
        "GR" : "w",
        "YO" : "a",
        "BY" : "b",
        "OB" : "c",
        "RB" : "x",
        "GW" : "y",
        "YR" : "z",
    }
    rotation_decomposition = {
        "WG" : "",       # o 0 identity

        "BW" : "i",      # i 1 i
        "GY" : "iii",    # f 1 (iii)
        "WO" : "j",      # j 1 j
        
        "WR" : "jjj",    # g 1 (jjj)
        "RG" : "k",      # k 1 k
        "OG" : "kkk",    # h 1 (kkk)
        
        "YB" : "ii",     # l 2 ii
        "WB" : "jj",     # m 2 jj
        "YG" : "kk",     # n 2 kk

        "OW" : "ijjj",   # p 2 i-(jjj)-(kkk)
        "OY" : "iiij",   # q 2 (iii)-j-(kkk)
        "RY" : "jjjk",   # r 2 (iii)-(jjj)-k
        "RW" : "ij",     # s 2 i-j-k

        "GO" : "kj",     # t 2 (iii)-k-j
        "BO" : "ji",     # u 2 i-(kkk)-j
        "BR" : "ik",     # v 2 i-k-(jjj)
        "GR" : "iiikkk", # w 2 (iii)-(kkk)-(jjj)

        "YO" : "jii",    # a 3 jii
        "BY" : "jji",    # b 3 jji
        "OB" : "iik",    # c 3 iik
        "RB" : "iji",    # x 3 j(ij) (ij)i
        "GW" : "ijj",    # y 3 k(ij) (ij)j
        "YR" : "ijk",    # z 3 i(ij) (ij)k
    }

    def find_pos ( self, piece, orientation ) :
        for step in Cube.rotation_decomposition[orientation] :
            piece = Cube.position_table[piece]["ijk".index(step)]
        return piece

    def rotate ( self, orientation, rotation ) :
        for step in Cube.rotation_decomposition[orientation] :
            rotation = Cube.rotation_table[rotation]["ijk".index(step)]
        return rotation

    def __init__ ( self, state = "-------- ------------ ------" ) :
        if isinstance(state, str) :
            state = state.replace(" ", "").replace("-", "o")
            state = [list(Cube.rotation_shorthand.keys())[list(Cube.rotation_shorthand.values()).index(c)] for c in state]
            self.state = {
                "WGO" : state[0],
                "WGR" : state[1],
                "WBO" : state[2],
                "WBR" : state[3],
                "YGO" : state[4],
                "YGR" : state[5],
                "YBO" : state[6],
                "YBR" : state[7],

                "WG" : state[8],
                "WB" : state[9],
                "WO" : state[10],
                "WR" : state[11],
                "YG" : state[12],
                "YB" : state[13],
                "YO" : state[14],
                "YR" : state[15],
                "GO" : state[16],
                "GR" : state[17],
                "BO" : state[18],
                "BR" : state[19],

                "W" : state[20],
                "Y" : state[21],
                "G" : state[22],
                "B" : state[23],
                "O" : state[24],
                "R" : state[25],
            }
        elif isinstance(state, dict) :
            self.state = state

    def repr_orient_str ( self ) :
        return "".join([Cube.rotation_shorthand[self.state[piece]] for piece in ["WGO", "WGR", "WBO", "WBR", "YGO", "YGR", "YBO", "YBR", "WG", "WB", "WO", "WR", "YG", "YB", "YO", "YR", "GO", "GR", "BO", "BR", "W", "Y", "G", "B", "O", "R"]])
    
    def __mul__ ( self, other ) :
        if not isinstance(other, Cube) :
            raise Exception("Can only multiply a cube by another cube")
        new_state = {}
        for piece, orientation in self.state.items() :
            pos = self.find_pos(piece, orientation)
            rotation = other.state[pos]
            new_state[piece] = self.rotate(orientation, rotation)

        return Cube(new_state)

    def __str__ ( self ) :
        return self.repr_orient_str()

if __name__ == "__main__" :
    I  = Cube("oooo oooo oooo oooo oooo oooooo")

    Wj = Cube("jjjj ---- jjjj ---- ---- j-----")
    Cj = Cube("---- ---- ---- ---- jjjj --jjjj")
    Yj = Cube("---- jjjj ---- jjjj ---- -i----")
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

    # R U R' U' | R' F R | R U' R' U' R U R' F'
    """
        R  Rf
        R' Ri
        U  Wg
        U' Wj
        F  Gh
        F' Gk
    """

    print(Rf)
    print(Rf * Wg)
    print(Rf * Wg * Ri)
    print(Rf * Wg * Ri * Wj)
    print()
    sexy_move = Rf * Wg * Ri * Wj
    print(sexy_move * Rf)
    print(sexy_move * Rf * Wg)
    print(sexy_move * Rf * Wg * Ri)
    print(sexy_move * Rf * Wg * Ri * Wj)
    print()
    
    print(sexy_move)
    print(sexy_move * sexy_move)
    print(sexy_move * sexy_move * sexy_move)
    print(sexy_move * sexy_move * sexy_move * sexy_move)
    print(sexy_move * sexy_move * sexy_move * sexy_move * sexy_move)
    print(sexy_move * sexy_move * sexy_move * sexy_move * sexy_move * sexy_move)
