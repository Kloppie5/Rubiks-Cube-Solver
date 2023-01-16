
def orientation_multiply ( lhs, rhs ) :
    return [ lhs[i] for i in rhs ]


class Cube :
    """
      A Cube is a 3x3x3 Rubik's Cube.
      The internal state is expressed as a sparse 20 by 20 matrix of quaternions.
      This representation is simplified into an array of 20 tuples, each of which is
      the index of the piece and a permutation of the original orientation.
      This means that the index in the array is the original position of the piece.

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

    face_colors = "YOBRGW"
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

    def matrix_representation ( self ) :
        r = ""
        for i in range(20) :
            piece, orientation = self.cube[i]
            r += f"{'.'*piece}X{'.'*(19-piece)} | {Cube.pieces[piece]['colors']} | {orientation}\n"
        return r

    def net_representation ( self ) :
        r = ""
        net = [['.' for _ in range(12)] for _ in range(9)]
        net[1][4] = 'W'
        net[4][1] = 'O'
        net[4][4] = 'G'
        net[4][7] = 'R'
        net[4][10] = 'B'
        net[7][4] = 'Y'
        for y, x, piece, dir in [
          # White
          (0, 3, 14, 5),
          (0, 4, 19, 5),
          (0, 5, 15, 5),
          (1, 3, 17, 5),
          (1, 5, 18, 5),
          (2, 3, 12, 5),
          (2, 4, 16, 5),
          (2, 5, 13, 5),

          # Orange
          (3, 0, 14, 1),
          (3, 1, 17, 1),
          (3, 2, 12, 1),
          (4, 0, 10, 1),
          (4, 2,  8, 1),
          (5, 0,  2, 1),
          (5, 1,  5, 1),
          (5, 2,  0, 1),

          # Green
          (3, 3, 12, 4),
          (3, 4, 16, 4),
          (3, 5, 13, 4),
          (4, 3,  8, 4),
          (4, 5,  9, 4),
          (5, 3,  0, 4),
          (5, 4,  4, 4),
          (5, 5,  1, 4),

          # Red
          (3, 6, 13, 3),
          (3, 7, 18, 3),
          (3, 8, 15, 3),
          (4, 6,  9, 3),
          (4, 8, 11, 3),
          (5, 6,  1, 3),
          (5, 7,  6, 3),
          (5, 8,  3, 3),

          # Blue
          (3, 9, 15, 2),
          (3, 10, 19, 2),
          (3, 11, 14, 2),
          (4, 9, 11, 2),
          (4, 11, 10, 2),
          (5, 9,  3, 2),
          (5, 10, 7, 2),
          (5, 11, 2, 2),

          # Yellow
          (6, 3,  0, 0),
          (6, 4,  4, 0),
          (6, 5,  1, 0),
          (7, 3,  5, 0),
          (7, 5,  6, 0),
          (8, 3,  2, 0),
          (8, 4,  7, 0),
          (8, 5,  3, 0)
        ]:
            net[y][x] = Cube.face_colors[self.cube[piece][1][dir]]

        # add command colors
        command_colors = {
            'W' : '7',
            'O' : '5',
            'G' : '2',
            'R' : '1',
            'B' : '4',
            'Y' : '3'
        }
        for line in net :
            for i in range(len(line)) :
                if line[i] in command_colors :
                    line[i] = f"\033[1;3{command_colors[line[i]][0]}m{line[i]}\033[0m"

        for line in net :
            r += "".join(line) + "\n"
        
        return r
    
    def isometric_representation ( self ) :
        screen = ""

        replacements = [
            ("A", 14, 5),
            ("M", 19, 5),
            ("a", 15, 5),
            ("B", 17, 5),
            ("b", 18, 5),
            ("C", 12, 5),
            ("O", 16, 5),
            ("c", 13, 5),

            ("D", 12, 4),
            ("d", 13, 4),
            ("E", 8, 4),
            ("e", 9, 4),
            ("F", 0, 4),
            ("f", 1, 4),
            ("P", 16, 4),
            ("R", 4, 4),
            
            ("m", 13, 3),
            ("n", 18, 3),
            ("o", 15, 3),
            ("p", 9, 3),
            ("r", 11, 3),
            ("s", 1, 3),
            ("t", 6, 3),
            ("u", 3, 3),
        ]
        template = """
                            ...........                                   
                         ....AAAAAAAA.........                            
                      ........AAAAAAA.....MM........                      
                   ....BBBBB...........MMMMMMMMMMM.........               
                ....BBBBBBBBBBB.............MMM....aaaaaaa......          
             ....CC........B.....NNNNNNNNN.........aaaaaaaa.....          
          ....CCCCCCCCCCC.........NNNNNN.....bbbb...........ooo.          
          ........CCCC....OOOOOOO.........bbbbbbbbbbb....oooooo.          
          .DDDDD.........OOOOOOOOO..............bb....nn.oooooo.          
          .DDDDDDDDD..P.............cccccccccc.....nnnnn.oooooo.          
          .DDDDDDDDD..PPPPPPPP.........ccccc....m.nnnnnn.oooo...          
          .DDDDDDDDD..PPPPPPPPP.ddddd........mmmm.nnnnnn.o......          
          ...DDDDDDD..PPPPPPPPP.dddddddddd.mmmmmm.nnnnn.....rrr.          
          ............PPPPPPPPP.dddddddddd.mmmmmm.nn.....rrrrrr.          
          .EEEEEE..........PPPP.dddddddddd.mmmmmm.....qq.rrrrrr.          
          .EEEEEEEEE..QQ..........dddddddd.mmm.....qqqqq.rrrrrr.          
          .EEEEEEEEE..QQQQQQQQQ..........d.....pp.qqqqqq.rrrr...          
          .EEEEEEEEE..QQQQQQQQQ.eeeeee......ppppp.qqqqqq.r....u.          
          ....EEEEEE..QQQQQQQQQ.eeeeeeeeee.pppppp.qqqqq....uuuu.          
          .F..........QQQQQQQQQ.eeeeeeeeee.pppppp.q......uuuuuu.          
          .FFFFFFFF.........QQQ.eeeeeeeeee.ppppp.....ttt.uuuuuu.          
          .FFFFFFFFF..RRRR.........eeeeeee.pp.....tttttt.uuuuuu.          
          .FFFFFFFFF..RRRRRRRRR.f..............ss.tttttt.uuu....          
          .FFFFFFFFF..RRRRRRRRR.ffffffff....sssss.tttttt.....             
          ......FFFF..RRRRRRRRR.ffffffffff.ssssss.tttt....                
              .........RRRRRRRR.ffffffffff.ssssss.t....                   
                     .........R.ffffffffff.sssss....                      
                            .........fffff.ss....                         
                                   ...........
        """
        for line in template.splitlines() :
            for i in range(len(line)) :  
                if line[i] == "N" :
                    screen += "W"
                elif line[i] == "Q" :
                    screen += "G"
                elif line[i] == "q" :
                    screen += "R"
                else :
                  for char, piece, dir in replacements :
                      if line[i] == char :
                          screen += Cube.face_colors[self.cube[piece][1][dir]]
                          break
                  else :
                      screen += line[i]
            screen += "\n"
        command_colors = {
            'W' : '7',
            'O' : '5',
            'G' : '2',
            'R' : '1',
            'B' : '4',
            'Y' : '3'
        }
        r = ""
        for i in range(len(screen)) :
            if screen[i] in command_colors :
                r += f"\033[1;3{command_colors[screen[i]][0]}m░\033[0m"
            elif screen[i] == "." :
                r += f"\033[30m█\033[0m"
            else :
                r += screen[i]

        return r

    def __str__ ( self ) :
        r = self.matrix_representation()
        r += "\n"
        r += self.net_representation()
        r += "\n"
        r += self.isometric_representation()
        return r
    
    def __getitem__ ( self, loc ) :
        return self.cube[loc]

    def __mul__ ( self, rhs ) :
        new_cube = [None] * 20
        for loc in range(20) :
            prev_loc, applied_orientation = rhs[loc]
            piece, prev_orientation = self.cube[prev_loc]
            new_orientation = orientation_multiply(prev_orientation, applied_orientation)
            new_cube[loc] = (piece, new_orientation)
        return Cube(new_cube)
    
    def __eq__ ( self, rhs ) :
        for loc in range(20) :
            if self.cube[loc] != rhs[loc] :
                return False
        return True

def permutation ( cyclic_permutations = [], rotation = [0, 1, 2, 3, 4, 5] ) :
    cube = [None] * 20
    for i in range(20) :
        cube[i] = (i, [0, 1, 2, 3, 4, 5])
    
    for cyclic_permutation in cyclic_permutations :
        for i in range(len(cyclic_permutation)) :
            j = cyclic_permutation[i]
            k = cyclic_permutation[(i+1) % len(cyclic_permutation)]
            cube[j] = (k, rotation)

    return Cube(cube)

I  = permutation() # Identity
Rc = permutation([[ 1, 13, 15,  3], [ 6,  9, 18, 11]], [4, 1, 0, 3, 5, 2]) # Red counterclockwise
O  = permutation([[ 0, 12, 14,  2], [ 5,  8, 17, 10]], [4, 1, 0, 3, 5, 2]) # Orange clockwise
R  = permutation([[ 1,  3, 15, 13], [ 6, 11, 18,  9]], [2, 1, 5, 3, 0, 4]) # Red clockwise
Oc = permutation([[ 0,  2, 14, 12], [ 5, 10, 17,  8]], [2, 1, 5, 3, 0, 4]) # Orange counterclockwise
W  = permutation([[12, 13, 15, 14], [16, 18, 19, 17]], [0, 4, 1, 2, 3, 5]) # White clockwise
Yc = permutation([[ 0,  1,  3,  2], [ 4,  6,  7,  5]], [0, 4, 1, 2, 3, 5]) # Yellow counterclockwise
Wc = permutation([[12, 14, 15, 13], [16, 17, 19, 18]], [0, 2, 3, 4, 1, 5]) # White counterclockwise
Y  = permutation([[ 0,  2,  3,  1], [ 4,  5,  7,  6]], [0, 2, 3, 4, 1, 5]) # Yellow clockwise
Bc = permutation([[ 2,  3, 15, 14], [ 7, 11, 19, 10]], [3, 0, 2, 5, 4, 1]) # Blue counterclockwise
G  = permutation([[ 0,  1, 13, 12], [ 4,  9, 16,  8]], [3, 0, 2, 5, 4, 1]) # Green clockwise
B  = permutation([[ 2, 14, 15,  3], [ 7, 10, 19, 11]], [1, 5, 2, 0, 4, 3]) # Blue clockwise
Gc = permutation([[ 0, 12, 13,  1], [ 4,  8, 16,  9]], [1, 5, 2, 0, 4, 3]) # Green counterclockwise

class Interface :

    def __init__ ( self ) :
        self.commands = {
            "q" : ("Quit", exit),
            "r" : ("Red clockwise", lambda cube : cube * R),
            "r2" : ("Red twice", lambda cube : cube * R * R),
            "rc" : ("Red counterclockwise", lambda cube : cube * Rc),
            "o" : ("Orange clockwise", lambda cube : cube * O),
            "o2" : ("Orange twice", lambda cube : cube * O * O),
            "oc" : ("Orange counterclockwise", lambda cube : cube * Oc),
            "w" : ("White clockwise", lambda cube : cube * W),
            "w2" : ("White twice", lambda cube : cube * W * W),
            "wc" : ("White counterclockwise", lambda cube : cube * Wc),
            "y" : ("Yellow clockwise", lambda cube : cube * Y),
            "y2" : ("Yellow twice", lambda cube : cube * Y * Y),
            "yc" : ("Yellow counterclockwise", lambda cube : cube * Yc),
            "b" : ("Blue clockwise", lambda cube : cube * B),
            "b2" : ("Blue twice", lambda cube : cube * B * B),
            "bc" : ("Blue counterclockwise", lambda cube : cube * Bc),
            "g" : ("Green clockwise", lambda cube : cube * G),
            "g2" : ("Green twice", lambda cube : cube * G * G),
            "gc" : ("Green counterclockwise", lambda cube : cube * Gc),
            "i" : ("Identity", lambda cube : I),
        }
        self.aliases = {
            "U" : "w",
            "U2" : "w2",
            "U'" : "wc",
            "D" : "y",
            "D2" : "y2",
            "D'" : "yc",
            "L" : "o",
            "L2" : "o2",
            "L'" : "oc",
            "R" : "r",
            "R2" : "r2",
            "R'" : "rc",
            "F" : "g",
            "F2" : "g2",
            "F'" : "gc",
            "B" : "b",
            "B2" : "b2",
            "B'" : "bc",
            "Sune" : "R U R' U R U2 R' U2",
            "Sexy" : "R U R' U'"
            
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
            elif command in self.aliases :
                command_queue = self.aliases[command].split(" ") + command_queue
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
