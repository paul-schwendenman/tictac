# * * * * * * * * * * * *
# * Paul Schwendenman   *
# * 09/20/11            *
# * If you have to ask: *
# * You aren't allowed  *
# * * * * * * * * * * * *

# * * * * * * *
# * Imported  *
# * * * * * * *
import pickle
from UserList import UserList

# * * * * * * * * * * *
# * Global Variables  *
# * * * * * * * * * * *
aidata = {}
  # this is a dictionary of numbers that point to a dictionary with choices and
  # 	success rates
  # ex. aidata = {121000000 : [2,3,2, 3,4,4, 1,-3,4]} where [2]=3
statdata = [0, 0, 0, []]


DEBUG = 0               # Choose: 0 or 1
DISPLAYSTATS = 0
STARTINGPLAYER = 1      # Choose: 1 or 2
NUMBERLASTGAMES = 15    # Choose: 1, 2, 3...
FILENAME = "data"       # Save file
AIADJUST = {'win': 1, 'lose': -1, 'draw': 0, 'last': 2}
USEDSPACEBUMP = -40      # This is used to adjust intial values for grids
                         # until smart "invalid move"


# * * * * * * * *
# * Grid Class  *
# * * * * * * * *
class Grid(UserList):
    def __init__(self, initlist=None):
        # From the userlist
        self.data = []
        if initlist is not None:
            if type(initlist) == type(self.data):
                self.data[:] = initlist
            elif isinstance(initlist, UserList):
                self.data[:] = initlist.data[:]
            else:
                self.data = list(initlist)
        else:
            self.data = [0] * 9
        if ':' in self:
            raise TypeError

    def __str__(self):
        a = ''.join([str(a) for a in self.data])
        return a

    def toString(self):
        return ':'.join([str(a) for a in self.data])

    def fromString(self, a):
        self.data = [int(b) for b in a.split(':')]

    def returnXO(self):
        b = {0: " ", 1: "X", 2: "O"}
        return [b[a] for a in self.data]

    def getEmptySpaces(self):
        return [a for a, b in enumerate(self.data) if b == 0]

    def getUsedSpaces(self):
        return [a for a, b in enumerate(self.data) if b != 0]

    def __hash__(self):
        # Okay to hash despite being mutable, hash reveals state not variable
        #return int(self.__str__())
        return translateHash(self)


# * * * * * * * * * * * * * *
# * Grid Display Functions  *
# * * * * * * * * * * * * * *
def printXO(b):
    printGrid(b.returnXO())


def printGrid(a):
    print
    print " %i | %i | %i " % (a[0], a[1], a[2])
    print "---+---+---"
    print " %i | %i | %i " % (a[3], a[4], a[5])
    print "---+---+---"
    print " %i | %i | %i " % (a[6], a[7], a[8])


def printHelp():
    print
    print " 1 | 2 | 3 "
    print "---+---+---"
    print " 4 | 5 | 6 "
    print "---+---+---"
    print " 7 | 8 | 9 "


# * * * * * * * * * * * * * * * *
# * Mostly Depricated Functions * <-- Remove?
# * * * * * * * * * * * * * * * *
def convertGridToNumber(a):
    c = 0
    for b in a:
        c = c * 10
        c = c + b
    return c


def convertNumberToGrid(a):
    b = []
    for c in str(a):
        b.append(int(c))
    return b


def convertGridToXO(a):
    b = []
    c = {0: " ", 1: "X", 2: "O"}
    for e in a:
        b.append(c[e])
    return b


def getEmptySpaces(a):
    b = []
    for c, d in enumerate(a):
        if d == 0:
            b.append(c)
    return b


def getUsedSpaces(a):
    b = []
    for c, d in enumerate(a):
        if d != 0:
            b.append(c)
    return b


def getInitialValues(a):
    b = {0: 0, 1: USEDSPACEBUMP, 2: USEDSPACEBUMP}
    return [b[c] for c in a]


# * * * * * * * * * * * *
# * Game Over Function  * <-- Add to Grid?
# * * * * * * * * * * * *
def gameOver(a):
    if a[0] == a[1] == a[2] and a[0] != 0:
        return (a[0], 1)
    elif a[3] == a[4] == a[5] and a[3] != 0:
        return (a[3], 2)
    elif a[6] == a[7] == a[8] and a[6] != 0:
        return (a[6], 3)

    elif a[0] == a[3] == a[6] and a[0] != 0:
        return (a[0], 4)
    elif a[1] == a[4] == a[7] and a[1] != 0:
        return (a[1], 5)
    elif a[2] == a[5] == a[8] and a[2] != 0:
        return (a[2], 6)

    elif a[0] == a[4] == a[8] and a[0] != 0:
        return (a[0], 7)
    elif a[6] == a[4] == a[2] and a[2] != 0:
        return (a[6], 8)
    elif sum(a) >= 13:
        return (-1, 0)
    else:
        return (0, 0)


# * * * * * * * * * * * *
# * Translation Helpers *
# * * * * * * * * * * * *
def join(a):
    return ":".join(a)


def split(a):
    DEBUGFUNC = 0
    if type(a) == type(""):
        return [int(b) for b in a.split(":")]
    elif type(a) == Grid:
        if DEBUG or DEBUGFUNC:
            raise TypeError("Passed Spilt type Grid")
        return a
    elif type(a) == type([]):
        if DEBUG or DEBUGFUNC:
            raise TypeError("Passed Spilt type []")
        return a
    else:
        raise TypeError("Passed type %s" % type(a))


# * * * * * * * * * * * * *
# * Translation Functions *
# * * * * * * * * * * * * *
def translateGetMove(a, b):
    # Given a (current grid) and b (aidata)
    # Requires c in b to get move
    c, d = translateGridMax(a)
    if c in b:
        f = translateGridReverse(b[c], d)
        g = f.index(max(f))
    else:
        g = None
    return g


def translateGrid(a, e):
    # Returns only the selected transition, designated by e.
    return translateArray(a)[e]


def translateGridReverse(a, e):
    b = {0: 0, 1: 1, 2: 2, 3: 3, 4: 4, 5: 7, 6: 6, 7: 5}
    return translateGrid(a, b[e])

def translateArray(a):
    # Finds all of the possible transitions.
    DEBUGFUNC = 0
    if a == type(""):
        a = split(a)
        if DEBUG or DEBUGFUNC:
            raise TypeError("A is a string")
    b = translateData()
    return [Grid([a[f] for f in e]) for e in b]


def translateHash(a):
    b = translateFindMax(a)
    return int(str(translateGrid(a, b)))


def translateFindMax(a):
    # Returns the highest valued transition.
    DEBUGFUNC = 0
    if a == type(""):
        a = split(a)
        if DEBUG or DEBUGFUNC:
            raise TypeError("A is a string")
    b = translateData()
    c = [(Grid([int(a[f]) for f in e]), d) for d, e in enumerate(b)]
    #Remove the above int()
    if DEBUG or DEBUGFUNC:
        print "find max\n\t c (translation grids): ", c,
        print "\n\t max: ", max(c), "\n\t a (grid): ", a
    return max(c)[1]


def translateFindIndex(a, b):
    c = translateArray(a)
    if isinstance(b, Grid):
        pass
    else:
        e = [f for f in c if hash(f) == b][0]
    d = c.index(b)
    return d

def translateGridMax(a):
    # Returns the maximum valued grid
    e = translateFindMax(a)
    return (translateGrid(a, e), e)


def translateData():
    # Returns the transitions used for all 
    return [[0, 1, 2, 3, 4, 5, 6, 7, 8], [2, 1, 0, 5, 4, 3, 8, 7, 6],
            [6, 7, 8, 3, 4, 5, 0, 1, 2], [8, 5, 2, 7, 4, 1, 6, 3, 0],
            [0, 3, 6, 1, 4, 7, 2, 5, 8], [6, 3, 0, 7, 4, 1, 8, 5, 2],
            [8, 7, 6, 5, 4, 3, 2, 1, 0], [2, 5, 8, 1, 4, 7, 0, 3, 6]]


# * * * * * * * * * * * * * * *
# * Player Movement Functions *
# * * * * * * * * * * * * * * *
def swapPlayer(n):
    if n == 1:
        return 2
    else:  # n == 2:
        return 1


def getMove(n, a, c=None):
    b = 1000
    if n == 1:

        b = getMoveComputer(a, c)

        if b not in a.getEmptySpaces():

            print "\n\t b: ", b, " is not in ", a.getEmptySpaces()
            #raise ValueError
    else:  # n == 2:

        if DEBUG:
            b = getMovePlayer(a, c)
    if b not in a.getEmptySpaces():
        b = getMove(n, a, b)
        if b not in a.getEmptySpaces():
            raise ValueError
                
    return b


def getMovePlayer(a, c):
    printXO(a)
    if c != None:
        print "Invaild Move: ", c + 1
    b = raw_input("Move? ")[0]
    if b == "h" or b == "H":
        printHelp()
    b = int(b) - 1
    return b


def getMoveComputer(a, c):
    # Make getMove handle errors
    DEBUGFUNC = 0
    global aidata

    b = translateGridMax(a)

    if c != None:

        if DEBUG or 1:
            print "\nInvalid Computer Move:",
            print "\n\t c: ", c,
            print "\n\t aidata[b[0]]: ", aidata[b[0]],
        aidata[b[0]][c] -= 1
        if DEBUG or 1:
            print "\n\t c: ", c,
            print "\n\t aidata[b[0]]: ", aidata[b[0]],
    d = translateGetMove(a, aidata)

    if c == d:

        raise ValueError("c = d")    

    if d == None:
        # Should be Intializing 'new' states 
        aidata[b[0]] = Grid()
        if DEBUG or DEBUGFUNC:
            print "AI\n\t empty: ", aidata[b[0]]
        d = pickOne(Grid())

    

    return d
    #return getEmptySpaces(a)[0]


def pickOne(a):
    # Picks one from list.
    return a[0]


# * * * * * * * * * * * * * * * * *
# * Player Finalization Handlers  *
# * * * * * * * * * * * * * * * * *
def handleGameOver(a, b, c, d):
    if d == 2:
        handleGameOverPlayer(a, d)
    elif d == 1:
        handleGameOverComputer(a, b, c, d)
    else:
        a = "Player not 1 or 2" + str(d)
        raise ValueError(a)


def handleGameOverPlayer(a, b):
    if a == b:
        print "You won! computer lost"
    elif a == -1:
        print "You tied!"
    elif a == [2, 1][b - 1]:
        print "You lost, computer won"
    else:
        print "Winner not -1, 1, or 2\n\tWinner: ", winner
        raise IndexError


def handleGameOverComputer(a, b, c, d):
    adjustAI(a, b, c, d)


def adjustAI(a, b, c, j):
    DEBUGFUNC = 1
    global aidata
    self = j
    if a == -1:  # draw
        k = AIADJUST['draw']
        print "a: ", a, " draw"
    elif a == self:  # win
        k = AIADJUST['win']
        print "a: ", a, " win"
    else:  # loss
        k = AIADJUST['lose']
        print "a: ", a, " lose"
    if b != j:
        if DEBUG or DEBUGFUNC:
            print "encountered b = ", b, " should be ", j
        c.pop()
    while len(c) >= 2:
        d, e, g = c.pop()  # AI move
        print "d, e, g", d, e, g
        if g != j:
            d, e, g = c.pop()
            print "again d, e, j, g", d, e, j ,g
        h = translateFindMax(d)
        i = translateGrid(d, h)
        print "h , i", h, i
        if i in aidata:
            print "in"
            f = aidata[i]
        else:
            print "not in"
            # Fix this:
            #	Add initial values to Grid?
            f = getInitialValues(d)

        if DEBUG or DEBUGFUNC:
            print "f: ", f

        if len(c) > 2:
            l = AIADJUST['last']
            if DEBUG or 1:
                print "Last Move?"
        else:
            l = 1
        f[e] += k * l
        aidata[d] = f
        if DEBUG or DEBUGFUNC:
            print "AI win\n\t A (winner): ", a,
            print "\n\t B (starting player): ", b,
            print "\n\t C (gamegrids): ", c, "\n\t D (grid): ", d,
            print "\n\t E (move): ", e, "\n\t F (scores): ", f,
            print "\n\t j (index): ", j, "\n\t f[e] (score): ", f[e],
            print "\n\t l*k (change): ", l * k, "\n\t aidata[d]: ", aidata[d]


# * * * * * * * * * * * * *
# * Statistical Functions *
# * * * * * * * * * * * * *
def pushStats(b, a):
    b.reverse()
    b.append(a)
    b.reverse()
    if len(b) > NUMBERLASTGAMES:
        b.pop()
    return b


def printStats(a):
    b = a[0]
    c = a[1]
    d = a[2]
    e = a[3]
    f = b + c + d
    if f > 0:
        print "Success for O",
        print "\n\twins: ", c, (c * 100.) / f,
        print "%\n\tloses: ", b, (b * 100.) / f,
        print "%\n\tties: ", d, (d * 100.) / f, "%"
        b = e.count(1)
        c = e.count(2)
        d = e.count(-1)
        f = b + c + d
        print "Last %i games:" % (NUMBERLASTGAMES),
        print "\n\twins: ", c, (c * 100.) / f,
        print "%\n\tloses: ", b, (b * 100.) / f,
        print "%\n\tties: ", d, (d * 100.) / f, "%"


def analyzeStats(a, b):
    if a == 1:
        b[0] += 1
    elif a == 2:
        b[1] += 1
    elif a == -1:
        b[2] += 1
    else:
        "Winner not -1, 1, or 2\n\tWinner: ", winner
        raise IndexError
    b[3] = pushStats(b[3], a)


# * * * * * * * * * * * * * *
# * File Control Functions  *
# * * * * * * * * * * * * * *
def load():
    DEBUGFUNC = 0
    try:
        a = open(FILENAME)
        c = pickle.load(a)
        a.close()
    except IOError:
        if DEBUG or DEBUGFUNC:
            print "File doesn't exist? IO Error, line 287"
        c = {}
    if DEBUG or DEBUGFUNC:
        print "aidata has %i items" % (len(c))
    return c


def dump(a):
    DEBUGFUNC = 0
    b = open(FILENAME, "w")
    pickle.dump(a, b)
    if DEBUG or DEBUGFUNC:
        print "aidata has %i items" % (len(a))
    b.close()


# * * * * * * * * * *
# * Error Catching  *
# * * * * * * * * * *
def handleError():
    import sys
    stop = 1
    line = []
    line.append(sys.exc_info()[2].tb_lineno)
    tb = sys.exc_info()[2].tb_next
    while stop:
        if tb == None:
            stop = 0
        else:
            line.append(tb.tb_lineno)
            tb = tb.tb_next
    print "\t", sys.exc_info()[0], sys.exc_info()[1],
    print "\n\t line no: ", line[-1], "\n\t traceback: ", line


# * * * * *
# * Main  *
# * * * * *
def play():
    DEBUGFUNC = 0

    grid = Grid()
    startingplayer = STARTINGPLAYER

    winner = 0
    gamegrids = []

    global statdata

    player = startingplayer
    while winner == 0:

        move = getMove(player, grid)

        if DEBUG or DEBUGFUNC:

            print "move (190): ", move
        gamegrids.append((grid, move, player))
        grid[move] = player

        player = swapPlayer(player)
        winner, row = gameOver(grid)


    analyzeStats(winner, statdata)
    printXO(grid)
    if DEBUG or DEBUGFUNC:
        print "Game grids (525): ", len(gamegrids), gamegrids
    for index in range(1, 3):
        handleGameOver(winner, startingplayer, gamegrids[:], index)
        if DEBUG or DEBUGFUNC:
            print "\n\tLength after: ", len(gamegrids)


def main():
    # na = 'y'
    DEBUGFUNC = 0

    global aidata
    global statdata

    # b = raw_input("Enter name to load previous \
    #                memory or \"new\" to start a new account: ")
    try:
        while 1:  # a == 'y' or a == 'Y':

            aidata = load()
            if DEBUG or DEBUGFUNC:
                try:
                    print "AI data: ", aidata
                except:
                    print "locals: ", locals()
            play()
            dump(aidata)
            # a = raw_input("Play again? ")[0]
    except (ValueError, IndexError, EOFError, KeyboardInterrupt):
        if DEBUG or DEBUGFUNC:
            print "Caught Error: User quit?"
        handleError()
    if DISPLAYSTATS:
        printStats(statdata)
    dump(aidata)
if __name__ == "__main__":
    main()

