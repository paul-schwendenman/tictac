'''
 * * * * * * * * * * * *
 * Paul Schwendenman   *
 * 09/20/11            *
 * If you have to ask: *
 * You aren't allowed  *
 * * * * * * * * * * * *
'''

# * * * * * * *
# * Imported  *
# * * * * * * *
import pickle as pack
from UserList import UserList

# * * * * * * * * * * *
# * Global Variables  *
# * * * * * * * * * * *
DEBUG = 0               # Choose: 0 or 1
DISPLAYSTATS = 1
RECORD = 1              # Toggle Saving Data
STARTINGPLAYER = 1      # Choose: 1 or 2
NUMBERLASTGAMES = 15    # Choose: 1, 2, 3...
FILENAME = "data"       # Save file
AIADJUST = [{'win': 1, 'lose': -2, 'draw': -1, 'last': 1},
            {'win': 2, 'lose': -2, 'draw': 1, 'last': 1}]
USEDSPACE = -5      # This is used to adjust values for used spaces in grids
AICOUNT = 50        # Number of times to try and not pick a used move
USENUMBERPAD = 0    # Option for tubbs


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
        def pick(a, b):
            if a > b:
                return b
            else:
                return a
        return ':'.join([("      "  + str(a))[pick(-4, -len(str(a))):] for a in self.data])

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


# * * * * * * * *
# * UserError   *
# * * * * * * * *
class UserError(Exception):
    pass


# * * * * * * * * * * * * * *
# * Grid Display Functions  *
# * * * * * * * * * * * * * *
def printXO(b):
    '''
    Prints the tictactoe grid with XOs
    '''
    printGrid(b.returnXO())


def printGrid(a):
    '''
    Basic formatting for lists
    '''
    if type(a[0]) == type(1):
        print
        print " %i | %i | %i " % (a[0], a[1], a[2])
        print "---+---+---"
        print " %i | %i | %i " % (a[3], a[4], a[5])
        print "---+---+---"
        print " %i | %i | %i " % (a[6], a[7], a[8])
    else:
        print
        print " %c | %c | %c " % (a[0], a[1], a[2])
        print "---+---+---"
        print " %c | %c | %c " % (a[3], a[4], a[5])
        print "---+---+---"
        print " %c | %c | %c " % (a[6], a[7], a[8])


def printHelp():
    '''
    Helpful grid
    '''
    print
    if USENUMBERPAD:
        print " 7 | 8 | 9 "
        print "---+---+---"
        print " 4 | 5 | 6 "
        print "---+---+---"
        print " 1 | 2 | 3 "
    else:
        print " 1 | 2 | 3 "
        print "---+---+---"
        print " 4 | 5 | 6 "
        print "---+---+---"
        print " 7 | 8 | 9 "


def printAIData(a):
    '''
    Prints a useful representation of the AIdata variable.
    '''
    print len(a)
    for b, c in a.iteritems():
        d = b.returnXO()
        printEighteen(d, c)


def printEighteen(a, b):
    '''
    Prints a pair of 3x3 grids next to each other.
    '''
    print "%c %c %c %2i %2i %2i" % (a[0], a[1], a[2], b[0], b[1], b[2])
    print "%c %c %c %2i %2i %2i" % (a[3], a[4], a[5], b[3], b[4], b[5])
    print "%c %c %c %2i %2i %2i" % (a[6], a[7], a[8], b[6], b[7], b[8])
    print


def printGameGrids(a, e=None):
    '''
    Prints a resonable representation of the value of
    GameGrids and thus the history of the game so far.
    '''
    b = [d[0].returnXO() for d in a]
    if e != None:
        b.append(e.returnXO())
    for c in b:
        print c[0], c[1], c[2], "|",
    print
    for c in b:
        print c[3], c[4], c[5], "|",
    print
    for c in b:
        print c[6], c[7], c[8], "|",
    print
    print


def printGameGridsValues(gamegrids, aidata):
    '''
    Print the value for each grid in gamegrids based on aidata.
    '''
    h = []
    for i in gamegrids:
        f = translateFindMax(i[0])
        g = translateGrid(i[0], f)
        #print i , g, f
        h.append(translateGridReverse(aidata[g], f)
                 if (g in aidata) else Grid([''] * 9))
    printGrids(h)


def printGrids(a):
    for c in a:
        print "%2s%2s%2s%c" % (c[0], c[1], c[2], "|"),
    print
    for c in a:
        print "%2s%2s%2s%c" % (c[3], c[4], c[5], "|"),
    print
    for c in a:
        print "%2s%2s%2s%c" % (c[6], c[7], c[8], "|"),
    print
    print


# * * * * * * * * * * * * * * * *
# * Mostly Depricated Functions * <-- Remove them?
# * * * * * * * * * * * * * * * *
def convertGridToNumber(a):
    '''
    Hashs a list based on its contents
    '''
    # int(str(a))  # <-- better?
    c = 0
    for b in a:
        c = c * 10
        c = c + b
    return c


def convertNumberToGrid(a):
    '''
    Turns a hash into a list.
    '''
    b = []  # Make this  use Grid()?
    for c in str(a):
        b.append(int(c))
    return b


def convertGridToXO(a):
    '''
    Returns a list based on values of the input Grid
    '''
    b = []
    c = {0: " ", 1: "X", 2: "O"}
    for e in a:
        b.append(c[e])
    return b


def getEmptySpaces(a):
    '''
    Returns a list of the spaces that are valued empty.
    '''
    empty = 0
    b = []
    for c, d in enumerate(a):
        if d == empty:
            b.append(c)
    return b


def getUsedSpaces(a):
    '''
    Returns a list of (spaces) list indices that are not valued empty.
    '''
    empty = 0
    b = []
    for c, d in enumerate(a):
        if d != empty:
            b.append(c)
    return b


def getInitialValues(a):
    '''
    Return
    '''
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
        g = [i for i, j in enumerate(f) if j == max(f)]
        #g = f.index(max(f))
    else:
        g = None
    return g


def translateGrid(a, e):
    # Returns only the selected transition, designated by e.
    return translateArray(a)[e]


def translateGridReverse(a, e):
    #Returns the Reverse Grid
    return translateGrid(a, translateReverseIndex(e))


def translateReverseIndex(a):
    # Returns the complementary translation
    b = {0: 0, 1: 1, 2: 2, 3: 3, 4: 4, 5: 7, 6: 6, 7: 5}
    return b[a]


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
    # Returns the maximum valued grid, and the transition index
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

count = 0


def getMove(n, a, aidata, c=None):
    b = 1000
    if n == 1:

        b = getMoveComputer(a, c, aidata)

        if b not in a.getEmptySpaces():
            global count
            count += 1
            if DEBUG:
                print "\n\t b: ", b, " is not in ", a.getEmptySpaces()
            if count > AICOUNT:
                raise ValueError("Count greater than %i" % AICOUNT)
    else:  # n == 1
        b = getMovePlayer(a, c)

    if b not in a.getEmptySpaces():
        b = getMove(n, a, aidata, b)
        if b not in a.getEmptySpaces():
            raise ValueError

    return b


def getMovePlayer(a, c):
    printXO(a)
    try:
        if c != None:
            print "Invalid Move: ", c + 1
        b = raw_input("Move? ")[0]
        if b == "h" or b == "H":
            printHelp()
            b = -1
        if USENUMBERPAD:
            return {-1: -1, 7: 0, 8: 1, 9: 2, 4: 3,
                     5: 4, 6: 5, 1: 6, 2: 7, 3: 8}[int(b)]
        else:
            return int(b) - 1
    except (ValueError, IndexError, KeyError, EOFError, KeyboardInterrupt):
        raise UserError("User Quit")


def getMoveComputer(a, c, aidata):
    # Make getMove handle errors
    DEBUGFUNC = 0
    b = translateGridMax(a)
    if DEBUG or DEBUGFUNC:
        printXO(a)
        printXO(b[0])
    if c != None:
        f = [0, 1, 2, 3, 4, 5, 6, 7, 8, ]
        e = translateGridReverse(f, b[1])[c]
        if DEBUG or DEBUGFUNC:
            print "Invalid Computer Move:",
            print "\n\t c:", c,
            print "\t e:", e,
            print "\t b[1]:", b[1],
            print "\n\t aidata[b[0]]:", aidata[b[0]].toString(),
        aidata[b[0]][e] += USEDSPACE
        if DEBUG or DEBUGFUNC:
            print "\nAfter:"
            print "\t aidata[b[0]]:", aidata[b[0]].toString()
    d = translateGetMove(a, aidata)

    if c == d and d != None and c != None:
        raise ValueError("c = d")

    if d == None:
        # Should be Intializing 'new' states
        if DEBUG or DEBUGFUNC:
            print "AI\n\t aidata:", aidata,
        aidata[b[0]] = Grid()
        if DEBUG or DEBUGFUNC:
            print "\n\t empty: ", aidata[b[0]]
        d = Grid()
        #d = pickOne(a.getEmptySpaces())
    return pickOne(d)
    #return getEmptySpaces(a)[0]


def pickOne(a):
    '''
    Picks one.
    First: a[0], last: a[-1], random: r(0, len(a) - 1)
    '''
    from random import randint as r
    return a[r(0, len(a) - 1)]


# * * * * * * * * * * * * * * * * *
# * Player Finalization Handlers  *
# * * * * * * * * * * * * * * * * *
def handleGameOver(a, b, c, d, e):
    if d == b:
        handleGameOverPlayer(a, b, c, d, e)
    elif d != b:
        handleGameOverComputer(a, b, c, d, e)
    else:
        a = "Player not 1 or 2" + str(d)
        raise ValueError(a)


def handleGameOverPlayer(a, b, c, d, e):
    if a == -1:
        print "You tied!"
    elif (a == d):
        print "You won! computer lost"
    elif (a != d):
        print "You lost, computer won"
    else:
        print "Winner not -1, 1, or 2"
        raise IndexError
#    printGameGrids(c)
#    printGameGridsValues(c, e)


def handleGameOverComputer(a, b, c, d, e):
    #printGameGrids(c[:-1][d-1::2])
    #printGameGrids(c[:-1][2-d::2])
    adjustAI(a, b, c[: -1][2 - d:: 2], d, e)


def quantifyResult(a, b, c):
    if a == -1:  # draw
        return AIADJUST[c - 1]['draw']
    elif (a == c):  # win
        if DEBUG:
            print "AI win! a: %i, b: %i, c: %i" % (a, b, c)
        return AIADJUST[c - 1]['win']
    else:  # loss
        if DEBUG:
            print "AI loss :( a: %i, b: %i, c: %i" % (a, b, c)
        return AIADJUST[c - 1]['lose']


def adjustAI(winner, startingplayer, gamegrids, index, aidata, ignoreai=0):
    DEBUGFUNC = 0
    #assert gameOver(gamegrids.pop()[0])[0] != 0
    k = quantifyResult(winner, startingplayer, index)
    if DEBUG or DEBUGFUNC:
        printGameGrids(gamegrids)
    while len(gamegrids) > 0:
        grid, move, g = gamegrids.pop()  # AI move
        if DEBUG or DEBUGFUNC:
                print "grid, move, g, index", grid, move, g, index
                printXO(grid)
        maxgrid, translation = translateGridMax(grid)
        if maxgrid in aidata:
            scores = aidata[maxgrid]
            translatedscores = translateGridReverse(scores, translation)
        else:
            if ignoreai:
                translatedscores = scores = aidata[maxgrid] = Grid([0, 0, 0, 0, 0, 0, 0, 0, 0])
            else:
                raise Exception("newgrid not in data")
        if len(gamegrids) > 2:
            l = AIADJUST[startingplayer - 1]['last']
        else:
            l = 1

        translatedscores[move] += k * l
        adjustedscores = translateGrid(translatedscores, translation)
        aidata[maxgrid] = adjustedscores
        if DEBUG or DEBUGFUNC:
            print "*" * 30
            printEighteen(maxgrid.returnXO(), translatedscores)
            printEighteen(grid.returnXO(), scores)
            printEighteen(grid.returnXO(), adjustedscores)
        if DEBUG or DEBUGFUNC:
            print "AI win\n\t winner: ", winner,
            print "\n\t starting player: ", startingplayer,
            print "\n\t gamegrids: ", gamegrids, "\n\t grid: ", grid,
            print "\n\t move: ", move, "\n\t scores: ", scores,
            print "\n\t adjustedscores: ", adjustedscores,
            print "\n\t index: ", index, "\n\t scores[move]: ", scores[move],
            print "\n\t l*k (change): ", l * k,
            print "\n\t aidata[grid]: ", aidata[maxgrid]


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
        print "Success for O"
        print "\twins:\t%i\t%f%%" % (c, (c * 100.) / f)
        print "\tloses:\t%i\t%f%%" % (b, (b * 100.) / f)
        print "\tties:\t%i\t%f%%" % (d, (d * 100.) / f)
        b = e.count(1)
        c = e.count(2)
        d = e.count(-1)
        f = b + c + d
        print "Last %i games:" % (NUMBERLASTGAMES)
        print "\twins:\t%i\t%f%%" % (c, (c * 100.) / f)
        print "\tloses:\t%i\t%f%%" % (b, (b * 100.) / f)
        print "\tties:\t%i\t%f%%" % (d, (d * 100.) / f)


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
def loadPickle():
    DEBUGFUNC = 1
    try:
        a = open(FILENAME)
        c = pack.load(a)
        a.close()
    except IOError:
        if DEBUG or DEBUGFUNC:
            print "File doesn't exist? IO Error, line 287"
        c = {}
    if DEBUG or DEBUGFUNC:
        print "aidata has %i items" % (len(c))
    return c


def load():
    DEBUGFUNC = 1
    aidata = {}
    try:
        file = open(FILENAME)
        lines = file.readlines()
        for line in lines:
            line = line[:-1].split("\t")
            grid = Grid()
            value = Grid()
            grid.fromString(line[0])
            value.fromString(line[1])
            aidata[grid] = value
        file.close()
    except IOError:
        if DEBUG or DEBUGFUNC:
            print "File doesn't exist? IO Error, line 287"
        aidata = {}
    except:
        handleError
        try:
            file.close()
            aidata = loadPickle()
        except:
            pass
    if DEBUG or DEBUGFUNC:
        print "aidata has %i items" % (len(aidata))
    return aidata


def dumpPickle(a):
    DEBUGFUNC = 1
    b = open(FILENAME, "w")
    pack.dump(a, b)
    if DEBUG or DEBUGFUNC:
        print "aidata has %i items" % (len(a))
    b.close()


def dump(aidata):
    DEBUGFUNC = 1
    file = open(FILENAME, "w")
    grids = sorted(aidata.keys())
    for grid in grids:
        file.write(grid.toString() + "\t" + aidata[grid].toString() + "\n")
    if DEBUG or DEBUGFUNC:
        print "aidata has %i items" % (len(aidata))
    file.close()


# * * * * * * * * * *
# * Error Catching  *
# * * * * * * * * * *
def handleError():
    '''
    An in house represention for Error Handling.
    '''
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
    print "\t", __name__, sys.exc_info()[0], sys.exc_info()[1],
    print "\n\t line no: ", line[-1], "\n\t traceback: ", line


# * * * * *
# * Main  *
# * * * * *
def play(aidata, statdata):
    DEBUGFUNC = 0
    grid = Grid()
    startingplayer = STARTINGPLAYER
    winner = 0
    gamegrids = []
    player = startingplayer
    while winner == 0:
        move = getMove(player, grid, aidata)
        gamegrids.append((grid[:], move, player))
        player = swapPlayer(player)
        if DEBUG or DEBUGFUNC:
            print "move (578): ", move
        grid[move] = player
        winner, row = gameOver(grid)
    gamegrids.append((grid[:], move, player))
    analyzeStats(winner, statdata)
    printXO(grid)
    #printGameGrids(gamegrids)
    #printGameGridsValues(gamegrids, aidata)
    for index in range(1, 3):
        handleGameOver(winner, startingplayer, gamegrids[:], index, aidata)
    #printGameGridsValues(gamegrids, aidata)


def main():
    # na = 'y'
    DEBUGFUNC = 0

    aidata = {}
    statdata = [0, 0, 0, []]

    # b = raw_input("Enter name to load previous \
    #                memory or \"new\" to start a new account: ")
    try:
        if RECORD:
            aidata = load()
        if DEBUG or DEBUGFUNC:
            try:
                print "AI data: ", aidata
            except:
                print "locals: ", locals()

        while 1:  # a == 'y' or a == 'Y':
            play(aidata, statdata)
            # a = raw_input("Play again? ")[0]
    except UserError:
        print "User quit."
        if DEBUG or DEBUGFUNC:
            handleError()
    except:
        handleError()
    if DISPLAYSTATS:
        printStats(statdata)
    if RECORD:
        dump(aidata)
if __name__ == "__main__":
    main()
