
class Cube :
    """
        A Cube is an arbitrarily sized cube of pieces.
        The state of the cube can be expressed as a full nested matrix of positions, holding the piece and orientation.

        Because the position of a piece can be determined by its orientation, it is possible to express the entire state of the cube as a single string of rotation letters. All 24 axis aligned rotations can be represented by a single letter, but I chose to use the two letter notation of the top and front face colors relative to the root white-green color.

        This is internally kept as a dictionary of piece names to rotation operations, as to not be tied to a specific order of pieces.
    """
    position_table = {
        #WG       BW     WO     RG
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
        #        BW    WO    RG
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
    rotation_decomposition = {
        "WG" : [], # 0 identity

        "BW" : ["BW"],             # 1 i
        "GY" : ["BW", "BW", "BW"], # 1 (iii)
        "WO" : ["WO"],             # 1 j
        "WR" : ["WO", "WO", "WO"], # 1 (jjj)
        "RG" : ["RG"],             # 1 k
        "OG" : ["RG", "RG", "RG"], # 1 (kkk)
        
        "YB" : ["BW", "BW"], # 2 ii
        "WB" : ["WO", "WO"], # 2 jj
        "YG" : ["RG", "RG"], # 2 kk

        "OW" : ["BW", "WO", "WO", "WO"], # 2 i-(jjj)-(kkk)
        "OY" : ["BW", "BW", "BW", "WO"], # 2 (iii)-j-(kkk)
        "RY" : ["WO", "WO", "WO", "RG"], # 2 (iii)-(jjj)-k
        "RW" : ["BW", "WO"], # 2 i-j-k

        "GO" : ["RG", "WO"], # 2 (iii)-k-j
        "BO" : ["WO", "BW"], # 2 i-(kkk)-j
        "BR" : ["BW", "RG"], # 2 i-k-(jjj)
        "GR" : ["BW", "BW", "BW", "RG", "RG", "RG"], # 2 (iii)-(kkk)-(jjj)

        "YO" : ["WO", "BW", "BW"], # 3 jii
        "BY" : ["BW", "RG", "RG"], # 3 jji
        "OB" : ["BW", "BW", "RG"], # 3 iik
        "RB" : ["BW", "WO", "BW"], # 3 j(ij) (ij)i
        "GW" : ["BW", "WO", "WO"], # 3 k(ij) (ij)j
        "YR" : ["BW", "WO", "RG"], # 3 i(ij) (ij)k
    }

    def operate ( self, base, operation ) :
        result = self.operation_table[base][self.operation_letters.index(operation)]
        if result == "..." :
            if operation in Cube.operation_decomposition :
                result = self.operate(base, Cube.operation_decomposition[operation][0])
                for op in Cube.operation_decomposition[operation][1:] :
                    result2 = self.operate(result, op)
                    if result2 == "..." :
                        raise Exception(f"Unknown operation {result}/{op}")
                    result = result2
            else :
                raise Exception(f"Unknown operation {base}/{operation}")
            Cube.operation_table[base][self.operation_letters.index(operation)] = result
            print(f"Operation {base}/{operation} = {result}")
        return result


    def __init__ ( self, state = "-------- ------------ ------" ) :
        if isinstance(state, str) :
            state = state.replace(" ", "").replace("-", "o")
            self.state = {
                "YGO" : state[0],
                "YGR" : state[1],
                "YBO" : state[2],
                "YBR" : state[3],
                "WGO" : state[4],
                "WGR" : state[5],
                "WBO" : state[6],
                "WBR" : state[7],

                "YG" : state[8],
                "YB" : state[9],
                "YO" : state[10],
                "YR" : state[11],
                "WG" : state[12],
                "WB" : state[13],
                "WO" : state[14],
                "WR" : state[15],
                "GO" : state[16],
                "GR" : state[17],
                "BO" : state[18],
                "BR" : state[19],

                "Y" : state[20],
                "W" : state[21],
                "G" : state[22],
                "B" : state[23],
                "O" : state[24],
                "R" : state[25],
            }
        elif isinstance(state, dict) :
            self.state = state
        self.validate()
    
    def validate ( self ) :
        for piece in self.state :
            if self.state[piece] not in self.operation_letters :
                raise Exception("Invalid orientation letter: " + self.state[piece])
    
    def repr_orient_str ( self ) :
        return "".join([self.state[piece] for piece in ["YGO", "YGR", "YBO", "YBR", "WGO", "WGR", "WBO", "WBR", "YG", "YB", "YO", "YR", "WG", "WB", "WO", "WR", "GO", "GR", "BO", "BR", "Y", "W", "G", "B", "O", "R"]])
    
    def __mul__ ( self, other ) :
        if not isinstance(other, Cube) :
            raise Exception("Can only multiply a cube by another cube")
        new_state = {}
        for piece, orientation in self.state.items() :
            new_state[piece] = self.operate(orientation, other.state[self.operate(piece, orientation)])

        return Cube(new_state)

    def __str__ ( self ) :
        return self.repr_orient_str()

if __name__ == "__main__" :
    I  = Cube("oooooooo oooooooooooo oooooo")

    Yj = Cube("jjjj---- jjjj-------- j-----")
    Cj = Cube("-------- --------jjjj --jjjj")
    Wj = Cube("----jjjj ----jjjj---- -j----")
    Yg = Cube("gggg---- gggg-------- g-----")
    Cg = Cube("-------- --------gggg --gggg")
    Wg = Cube("----gggg ----gggg---- -g----")

    Gk = Cube("kk--kk-- k---k---kk-- --k---")
    Ck = Cube("-------- --kk--kk---- kk--kk")
    Bk = Cube("--kk--kk -k---k----kk ---k--")
    Gh = Cube("hh--hh-- h---h---hh-- --h---")
    Ch = Cube("-------- --hh--hh---- hh--hh")
    Bh = Cube("--hh--hh -h---h----hh ---h--")

    Oi = Cube("i-i-i-i- --i---i-i-i- ----i-")
    Ci = Cube("-------- ii--ii------ iiii--")
    Ri = Cube("-i-i-i-i ---i---i-i-i -----i")
    Of = Cube("f-f-f-f- --f---f-f-f- ----f-")
    Cf = Cube("-------- ff--ff------ ffff--")
    Rf = Cube("-f-f-f-f ---f---f-f-f -----f")
    
    print(Yj * Gk * Oi)
    print(Cj * Ck * Ci)
    print(Wj * Bk * Ri)
    print(Yg * Gh * Of)
    print(Cg * Ch * Cf)
    print(Wg * Bh * Rf)
