
class Cube :
    """
        A Cube is an arbitrarily sized cube of pieces.
        The internal state of the cube is expressed as a full nested matrix of positions, holding the piece and orientation.

        Because the orientation of a piece has to be axis aligned, it can only be one of 24 orientations. This allows for the orientation to be expressed as a letter.

        Because the position of a piece can be determined by the orientation of all the pieces, it is possible to express the entire state of the cube as a single string of rotation letters.
    """

    """
        Orientation letters:
        i follows white to green
        j follows green to red
        k follows red to white

          o ijk lmn fgh pqrstuvw abcxyz
        o o ijk lmn fgh pqrstuvw abcxyz  1   identity

        i i okj fcy lxz tuvwpqrs bamgnh  ii ll
        j j koi bgz amy utsrqpwv flxchn  jj mm  half turns
        k k jio axh bcn qpwvutsr lfgmzy  kk nn
        
        l l fab ipr oqs cxyzmgnh kjtuvw  i+ l
        m m xgc sjp vot zhlbynaf wrikqu  j+ m positive roots
        n n zyh pvk uro alcmfbxg qtwsij  k+ n

        f f lba otv iuw mgnhcxyz jkpqrs  i- lll
        g g cmx rou wjq nyblhzfa vskitp  j- mmm negative roots
        h h yzn qso twk lagxbfmc purvji  k- nnn

        p p uqt zac nlm wsijvrko hyfbxg  ij lm
        q q tpu ylg hax rvjiswok nzbfmc  ij- lmmm two quarter turns
        r r wvs cnb gyl kitpojuq xmhzfa  ik ln
        s s vwr xzl mhb ikqujopt cgynaf  ik- lnnn
        t t qup hbm yfc swokrvji znlagx  i-j lllm
        u u ptq nfx zbg vrkowsij yhalcm  i-j- lllmmm
        v v srw mya xnf joptikqu gczhlb  i-k llln
        w w rsv ghf cza ojuqkitp mxnybl  i-k- lllnnn

        a a blf jqw kpv gmzyxchn oiutsr  ijj lmm
        b b afl kus jtr xchngmzy ioqpwv  i-jj lllmm  three quarter turns
        c c gxm wkt rip hzfanybl svojuq  iij llm
        x x mcg viq sku ynafzhlb rwjopt  iij- llmmm
        y y hnz trj qvi bfmclagx upswok  iik lln
        z z nhy uwi psj fbxgalcm tqvrko  iik- llnnn
    """

    """
        Position order:

        G -- R -- H
        |    |    |
        S -- V -- T  White
        |    |    |
        E -- Q -- F

        O -- X -- P
        |         |
        Y         Z  Mid
        |         |
        M -- W -- N

        C -- J -- D
        |    |    |
        K -- U -- L  Yellow
        |    |    |
        A -- I -- B

        A YGO
        B YGR
        C YBO
        D YBR
        E WGO
        F WGR
        G WBO
        H WBR

        I YG
        J YB
        K YO
        L YR
        M GO
        N GR
        O BO
        P BR
        Q WG
        R WB
        S WO
        T WR

        U Y
        V W
        W G
        X B
        Y O
        Z R
    """
    piece_letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    operation_decomposition = {
        "o": "",
        "i": "ll",
        "j": "mm",
        "k": "nn",
        "l": "l",
        "m": "m",
        "n": "n",
        "f": "lll",
        "g": "mmm",
        "h": "nnn",
        "p": "lm",
        "q": "lmmm",
        "r": "ln",
        "s": "lnnn",
        "t": "lllm",
        "u": "lllmmm",
        "v": "llln",
        "w": "lllnnn",
        "a": "lmm",
        "b": "lllmm",
        "c": "llm",
        "x": "llmmm",
        "y": "lln",
        "z": "llnnn",
    }
    operation_table = {
        "A": { "l": "C", "m": "B", "n": "B" },
        "B": { "l": "D", "m": "D", "n": "F" },
        "C": { "l": "G", "m": "A", "n": "D" },
        "D": { "l": "H", "m": "C", "n": "H" },
        "E": { "l": "A", "m": "F", "n": "A" },
        "F": { "l": "B", "m": "H", "n": "E" },
        "G": { "l": "E", "m": "E", "n": "C" },
        "H": { "l": "F", "m": "G", "n": "G" },
        "I": { "l": "J", "m": "L", "n": "N" },
        "J": { "l": "R", "m": "K", "n": "P" },
        "K": { "l": "O", "m": "I", "n": "L" },
        "L": { "l": "P", "m": "J", "n": "T" },
        "M": { "l": "K", "m": "N", "n": "I" },
        "N": { "l": "L", "m": "P", "n": "Q" },
        "O": { "l": "S", "m": "M", "n": "J" },
        "P": { "l": "T", "m": "O", "n": "R" },
        "Q": { "l": "I", "m": "T", "n": "M" },
        "R": { "l": "Q", "m": "S", "n": "O" },
        "S": { "l": "M", "m": "Q", "n": "K" },
        "T": { "l": "N", "m": "R", "n": "S" },
        "U": { "l": "X", "m": "U", "n": "Z" },
        "V": { "l": "W", "m": "V", "n": "Y" },
        "W": { "l": "U", "m": "Z", "n": "W" },
        "X": { "l": "V", "m": "Y", "n": "X" },
        "Y": { "l": "Y", "m": "W", "n": "U" },
        "Z": { "l": "Z", "m": "X", "n": "V" },

        "o": { "l": "l", "m": "m", "n": "n" },
        "i": { "l": "f", "m": "c", "n": "y" },
        "j": { "l": "b", "m": "g", "n": "z" },
        "k": { "l": "a", "m": "x", "n": "h" },
        "l": { "l": "i", "m": "p", "n": "r" },
        "m": { "l": "s", "m": "j", "n": "p" },
        "n": { "l": "p", "m": "v", "n": "k" },
        "f": { "l": "o", "m": "t", "n": "v" },
        "g": { "l": "r", "m": "o", "n": "u" },
        "h": { "l": "q", "m": "s", "n": "o" },
        "p": { "l": "z", "m": "a", "n": "c" },
        "q": { "l": "y", "m": "l", "n": "g" },
        "r": { "l": "c", "m": "n", "n": "b" },
        "s": { "l": "x", "m": "z", "n": "l" },
        "t": { "l": "h", "m": "b", "n": "m" },
        "u": { "l": "n", "m": "f", "n": "x" },
        "v": { "l": "m", "m": "y", "n": "a" },
        "w": { "l": "g", "m": "h", "n": "f" },
        "a": { "l": "j", "m": "q", "n": "w" },
        "b": { "l": "k", "m": "u", "n": "s" },
        "c": { "l": "w", "m": "k", "n": "t" },
        "x": { "l": "v", "m": "i", "n": "q" },
        "y": { "l": "t", "m": "r", "n": "j" },
        "z": { "l": "u", "m": "w", "n": "i" },
    }

    def __init__ ( self, state ) :
        self.state = state.replace(" ", "").replace("-", "o")
        if not self.valid() :
            raise ValueError("Invalid cube state: " + self.state)
    
    def valid ( self ) :
        return all(c in self.repr_pos_str() for c in Cube.piece_letters)

    def repr_orient_str ( self ) :
        return self.state[0:8] + " " + self.state[8:20] + " " + self.state[20:26]

    def repr_pos_str ( self ) :
        pos = []
        for i, c in enumerate(self.state) :
            letter = Cube.piece_letters[i]
            dec = Cube.operation_decomposition[c]
            for d in dec :
                letter = Cube.operation_table[letter][d]
            pos.append(letter)
        return "".join(pos)

    def repr_matrix ( self ) :
        for i, c in enumerate(self.state) :
            letter = Cube.piece_letters[i]
            dec = Cube.operation_decomposition[c]
            for d in dec :
                letter = Cube.operation_table[letter][d]
            pos = Cube.piece_letters.index(letter)

            if pos < 8 :
                print(f"{'-'*pos}{c}{'-'*(7-pos)}{' '*18} {letter}")
            elif pos < 20 :
                print(f"{' '*8}{'-'*(pos-8)}{c}{'-'*(19-pos)}{' '*6} {letter}")
            else :
                print(f"{' '*20}{'-'*(pos-20)}{c}{'-'*(25-pos)} {letter}")
        return self.state

    def true_equal ( self, other ) :
        return self.state == other.state
    
    def __eq__ ( self, other ) :
        return self.repr_pos_str() == other.repr_pos_str()

    def __mul__ ( self, other ) :
        state = [None]*26
        for i, orientation in enumerate(self.state) :
            letter = Cube.piece_letters[i]
            for d in Cube.operation_decomposition[orientation] :
                letter = Cube.operation_table[letter][d]
            other_orientation = other.state[Cube.piece_letters.index(letter)]
            for d in Cube.operation_decomposition[other_orientation] :
                letter = Cube.operation_table[letter][d]
                orientation = Cube.operation_table[orientation][d]

            state[Cube.piece_letters.index(letter)] = orientation

        return Cube("".join(state))

    def __str__ ( self ) :
        return self.repr_matrix()

if __name__ == "__main__" :
    I  = Cube("oooooooo oooooooooooo oooooo")

    Ym = Cube("mmmm---- mmmm-------- m-----")
    Yg = Cube("gggg---- gggg-------- g-----")
    Wm = Cube("----mmmm --------mmmm -m----")
    Wg = Cube("----gggg --------gggg -g----")
    Gn = Cube("nn--nn-- n---nn--n--- --n---")
    Gh = Cube("hh--hh-- h---hh--h--- --h---")
    Bn = Cube("--nn--nn -n----nn-n-- ---n--")
    Bh = Cube("--hh--hh -h----hh-h-- ---h--")
    Ol = Cube("l-l-l-l- --l-l-l---l- ----l-")
    Of = Cube("f-f-f-f- --f-f-f---f- ----f-")
    Rf = Cube("-f-f-f-f ---f-f-f---f -----f")
    Rl = Cube("-l-l-l-l ---l-l-l---l -----l")

    print(Ym * Yg == I)
    print(Wm * Wg == I)
    print(Gn * Gh == I)
    print(Bn * Bh == I)
    print(Ol * Of == I)
    print(Rf * Rl == I)
