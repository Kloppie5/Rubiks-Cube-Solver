
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
        o o ijk lmn fgh pqrstuvw abcxyz  identity

        i i okj fcy lxz tuvwpqrs bamgnh
        j j koi bgz amy utsrqpwv flxchn  half turns
        k k jio axh bcn qpwvutsr lfgmzy
        
        l l fab ipr oqs cxyzmgnh kjtuvw
        m m xgc sjp vot zhlbynaf wrikqu  positive roots
        n n zyh pvk uro alcmfbxg qtwsij

        f f lba otv iuw mgnhcxyz jkpqrs
        g g cmx rou wjq nyblhzfa vskitp  negative roots
        h h znq sot wkl agxbfmcp urvji

        p p uqt zac nlm wsijvrko hyfbxg
        q q tpu ylg hax rvjiswok nzbfmc  two quarter turns
        r r wvs cnb gyl kitpojuq xmhzfa
        s s vwr xzl mhb ikqujopt cgynaf
        t t qup hbm yfc swokrvji znlagx
        u u ptq nfx zbg vrkowsij yhalcm
        v v srw mya xnf joptikqu gczhlb
        w w rsv ghf cza ojuqkitp mxnybl

        a a blf jqw kpv gmzyxchn oiutsr
        b b afl kus jtr xchngmzy ioqpwv  three quarter turns
        c c gxm wkt rip hzfanybl svojuq
        x x mcg viq sku ynafzhlb rwjopt
        y y hnz trj qvi bfmclagx upswok
        z z nhy uwi psj fbxgalcm tqvrko
    """

    """
        Position order:

        YGO YGR YBO YBR
        WGO WGR WBO WBR

        YG YB YO YR
        GO GR BO BR
        WG WB WO WR

        Y W G B O R
    """

    def __init__ ( self, state ) :
        self.state = state.replace(" ", "")
    
    def __str__ ( self ) :
        return self.state[0:8] + " " + self.state[8:20] + " " + self.state[20:26]

if __name__ == "__main__" :
    cube = Cube("oooooooo oooooooooooo oooooo")

    Y    = Cube("ggggoooo ggggoooooooo gooooo")
    Yc   = Cube("mmmmoooo mmmmoooooooo gooooo")
    W    = Cube("oooommmm oooooooommmm omoooo")
    Wc   = Cube("oooogggg oooooooogggg ogoooo")
    G    = Cube("hhoooooo hooohhoohooo oohooo")
    Gc   = Cube("nnoooooo nooonnoonooo oonooo")
    B    = Cube("oonnoooo onoooonnonoo ooonoo")
    Bc   = Cube("oohhoooo ohoooohhohoo ooohoo")
    O    = Cube("lolololo oolololooolo oooolo")
    Oc   = Cube("fofofofo oofofofooofo oooofo")
    R    = Cube("ofofofof ooofofofooof ooooof")
    Rc   = Cube("olololol ooolololoool oooool")

    print(cube)
    print(W)
    print(Wc)
    print(G)
    print(Gc)
    print(B)
    print(Bc)
    print(O)
    print(Oc)
    print(R)
    print(Rc)
    
