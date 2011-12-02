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
from UserList import UserList
from handleError import handleError
from ProgressBar import ProgressProcess
from Timer import Timer

# * * * * * * * * * * *
# * Global Variables  *
# * * * * * * * * * * *
DEBUG = 0               # Choose: 0 or 1
NUMBERLASTGAMES = 15    # Choose: 1, 2, 3...
AIADJUST = [{'win': 1, 'lose': -1, 'draw': 0, 'last': 2},
            {'win': 1, 'lose': -1, 'draw': 0, 'last': 2}]
USEDSPACE = -5      # This is used to adjust values for used spaces in grids
RECURSIONCOUNT = 50        # Number of times to try and not pick a used move


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
        return ':'.join([("      " + str(a))[pick(-4, -len(str(a))):] \
               for a in self.data])

    def __sub__(self, other):
        assert len(self.data) == len(self.data)
        return Grid([self.data[index] - other[index] for index in range(0, len(self.data))])

    def fromString(self, a):
        self.data = [int(b) for b in a.split(':')]

    def returnXO(self):
        b = {0: " ", 1: "X", 2: "O"}
        return [b[a] for a in self.data]

    def getEmptySpaces(self):
        return [a for a, b in enumerate(self.data) if b == 0]

    def getUsedSpaces(self):
        '''
        Returns a list of (spaces) list indices that are not valued empty.
        '''
        return [a for a, b in enumerate(self.data) if b != 0]

    def __hash__(self):
        # Okay to hash despite being mutable, hash reveals state not variable
        #return int(self.__str__())
        return translateHash(self)


# * * * * * * * * *
# * Player Class  *
# * * * * * * * * *
class Player():
    '''
    The base player class for a game.
    '''
    def __init__(self, index):
        self.index = index

    def getMove(self, *args):
        '''
        This function should take a variable number
        of inputs and return a single number.

        Typically takes two inputs:
        - the current grid
        - an error raised flag

        Output:
        - should be in [0...8] (3x3 grid)
        '''
        pass

    def handleGameOver(self, *args):
        '''
        The method should handle all end game
        activities for the player.

        Typical Input:
        - winner
        - startingplayer
        - gamegrids
        - index, aidata <-- local
        '''
        pass


class Human(Player):
    '''
    Player designed for human input.
    '''
    def getMove(self, grid, error):
        try:
            printXO(grid)
            if error != None:
                print "Invalid Move: ", error + 1
            input = raw_input("Move? ")[0]
            if input == "h" or input == "H":
                printHelp()
                input = raw_input("Move? ")[0]
            else:
                return int(input) - 1
        except (ValueError, IndexError, KeyError, EOFError, KeyboardInterrupt):
            raise UserError("User Quit")

    def handleGameOver(self, winner, gamegrids):
        printXO(gamegrids[-1][0])
        assert winner in [-1, 1, 2]
        if winner == -1:
            print "You tied!"
        elif (winner == self.index):
            print "You won! computer lost"
        else:
            print "You lost, computer won"


class HumanNumber(Human):
    '''
    Use the numberpad.
    '''
    def getMove(self, *args):
        a = {7: 0, 8: 1, 9: 2, 4: 3, 5: 4, 6: 5, 1: 6, 2: 7, 3: \
            8}[Human.getMove(self, *args) + 1] - 1
        print "Move:", a
        return a


class Comp(Player):
    '''
    Base that all computer players have.
    '''
    def __init__(self, index, **settings):
        self.index = index
        if 'filename' in settings:
            self.filename = settings['filename']
        else:
            self.filename = 'data'
        if 'record' in settings and settings['record'] == 1:
            self.record = 1
            self.load()
        else:
            self.record = 0
            self.aidata = {}

    def setAIdata(self, aidata):
        self.aidata = aidata

    def getMove(self, *args):
        pass

    def handleGameOver(self, *args):
        pass

    def loadPickle(self, filename=None):
        from cPickle import load
        try:
            a = open(filename)
            self.aidata = load(a)
            a.close()
        except IOError:
            print "File doesn't exist?"
            self.aidata = {}
        else:
            print "aidata has %i items" % (len(self.aidata))

    def load(self):
        self.loadPickle(self.filename)

    def dumpPickle(self):
        from cPickle import dump
        b = open(self.filename, "w")
        dump(self.aidata, b)
        print "aidata has %i items" % (len(self.aidata))
        b.close()

    def dump(self):
        self.record = 0
        self.dumpPickle()

    def __del__(self):
        if self.record:
            self.dump()


class CompPick(Comp):
    '''
    Pick one... no thought.
    '''
    def getMove(self, grid, c):
        return pickOne(grid.getEmptySpaces())


class CompTwo(Comp):
    '''
    Plays 'perfect' should finish wins and
    should block moves.
    '''
    def getMove(self, grid, c):
        one = ([item[1] for item in filter(filterLinesOne, \
                mapGrid(pickPlay, grid))])
        two = ([item[1] for item in filter(filterLinesTwo, \
                mapGrid(pickPlay, grid))])
        grid = grid.getEmptySpaces()
        if self.index == 2:
            if  two:
                grid = two
            elif one:
                grid = one
        elif self.index == 1:
            if two:
                grid = two
            elif one:
                grid = one
        return pickOne(grid)

    def handleGameOver(self, *args):
        '''
        Doesn't Need to learn anything
        '''
        pass


class CompLearning(Comp):
    def getMove(self, grid, error):
        # Make getMove handle errors
        DEBUGFUNC = 0
        if grid.count(0) == len(grid):
            return pickOne([pickOne([0, 2, 6, 8]), pickOne([1, 3, 5, 7]), 4])
        b = translateGridMax(grid)
        if DEBUG or DEBUGFUNC:
            printXO(grid)
            printXO(b[0])
        if error != None:
            f = [0, 1, 2, 3, 4, 5, 6, 7, 8, ]
            e = translateGridReverse(f, b[1])[error]
            if DEBUG or DEBUGFUNC:
                print "Invalid Computer Move:"
                print "\t error:", error, "\t e:", e, "\t b[1]:", b[1]
                print "\t self.aidata[b[0]]:", self.aidata[b[0]].toString(),
            self.aidata[b[0]][e] += USEDSPACE
            if DEBUG or DEBUGFUNC:
                print "\nAfter:"
                print "\t self.aidata[b[0]]:", self.aidata[b[0]].toString()
        d = translateGetMove(grid, self.aidata)

        if error == d and d != None and error != None:
            raise ValueError("error = d")

        if d == None:
            # Should be Intializing 'new' states
            #if DEBUG or DEBUGFUNC:
            #    print "AI\n\t self.aidata:", self.aidata,
            self.aidata[b[0]] = Grid()
            if DEBUG or DEBUGFUNC:
                print "\n\t empty: ", self.aidata[b[0]]
            d = Grid()
            #d = pickOne(grid.getEmptySpaces())
        return pickOne(d)
        #return getEmptySpaces(a)[0]

    def handleGameOver(self, a, b):
        adjustAI(a, b[: -1][2 - self.index:: 2], self.index, self.aidata)

    def load(self):
        self.aidata = {}
        try:
            file = open(self.filename)
            lines = file.readlines()
            for line in lines:
                line = line[:-1].split("\t")
                grid = Grid()
                value = Grid()
                grid.fromString(line[0])
                value.fromString(line[1])
                self.aidata[grid] = value
            file.close()
        except IOError:
            print "File doesn't exist?"
            self.aidata = {}
        except:
            handleError
            try:
                file.close()
                self.loadPickle()
            except:
                pass
        print "aidata has %i items" % (len(self.aidata))

    def dump(self):
        self.record = 0
        file = open(self.filename, "w")
        grids = sorted(self.aidata.keys())
        for grid in grids:
            file.write(grid.toString() + "\t" + \
                       self.aidata[grid].toString() + "\n")
        print "aidata has %i items" % (len(self.aidata))
        file.close()


class CompTree(Comp):
    def getMove(self, grid, error):
        printXO(grid)
        print "Error:", error, grid
        assert error == None
        gridmax, trans = translateGridMax(grid)
        if grid in self.aidata:
            print "Tree"
            move = followTree(gridmax)
        else:
            print "Pick from"
            move = gridmax.getEmptySpaces()[0]
            #move = pickOne(gridmax.getEmptySpaces())
        #if move not in grid.getEmptySpaces():
        move2 = translateGridReverse(range(0, 9), trans)[move]
        print trans
        print gridmax, Grid(range(0, 9)), gridmax.getEmptySpaces(), move
        print grid, translateGridReverse(range(0, 9), trans), grid.getEmptySpaces(), move2
        return move2

    def followTree(self, grid):
        if grid in self.aidata and type(self.aidata[grid]) == type(1):
            return (None, self.aidata[grid]) 
        elif len(self.aidata[grid]) > 1:
            results = []
            for each in self.aidata[grid]:
                results.append(((each - grid).index(self.index), \
                                 followTree(each),))
            moves = [s for s in filter(lambda a: a[1] == self.index, results)]
            if not moves:
                moves = [s for s in filter(lambda a: a[1] == -1, results)]
                if not moves:
                    moves = [s for s in filter(lambda a: a[1] == 0, results)]
                    if not moves:
                        moves = [s for s in filter(lambda a: a[1] not in \
                                 [-1, 0, self.index], results)]
            return pickOne(moves)
        else:
            return ((self.aidata[grid][0] - grid).index(self.index), \
                     followTree(self.aidata[0][grid]),)
            pass
    def handleGameOver(self, winner, grids):
        grids = grids[2 - self.index:: 2]
        grids.reverse()
        while len(grids) > 1:
            grid = translateGridMax(grids.pop()[0])[0]
            if grid in self.aidata:
                self.aidata[grid].append(translateGridMax(grids[-1][0])[0])
            else:
                self.aidata[grid] = [translateGridMax(grids[-1][0])[0]]
        assert len(grids) == 1
        grid = translateGridMax(grids.pop()[0])[0]
        if grid not in self.aidata:
            self.aidata[grid] = winner
        else:
            assert self.aidata[grid] == winner


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


def printNine(a):
    print "%2i %2i %2i\n%2i %2i %2i\n%2i %2i %2i\n" % (a[0], a[1], a[2], \
          a[3], a[4], a[5], a[6], a[7], a[8])


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


# * * * * * * * * * * * * * * * * *
# * Sorting and Filter Functions  *
# * * * * * * * * * * * * * * * * *
def mapGrid(f, grid):
    lines = [(0, 1, 2), (3, 4, 5), (6, 7, 8), \
             (0, 3, 6), (1, 4, 7), (2, 5, 8), \
             (0, 4, 8), (2, 4, 6)]
    return [f(line, grid) for line in lines]


def filterLinesNone(a):
    '''
    Returns false if None
    '''
    return a != None


def filterLinesOne(a):
    '''
    Returns true if one.
    '''
    return a[0] == 1


def filterLinesTwo(a):
    '''
    Returns true if two.
    '''
    return a[0] == 2


def pickGameOver(sample, grid):
    '''
    Picks the in a given sample. Ex: row.
    '''
    values = [grid[sample[0]], grid[sample[1]], grid[sample[2]]]
    if values[0] == values[1] == values[2] and values[0] != 0:
        return (values[0])
    return (None)


def pickPlay(sample, grid):
    '''
    Picks the open space in a given sample. Ex: row.
    '''
    values = [grid[sample[0]], grid[sample[1]], grid[sample[2]]]
    if values.count(0) == 1:
        index = values.index(0)
        del values[index]
        if values[0] == values[1]:
            return (values[0], sample[index])
    return (None, None)


def gameOver(grid):
    values = filter(filterLinesNone, mapGrid(pickGameOver, grid))
    if len(values) == 0:
        values = [0]
        if  sum(grid) >= 13:  # Get empty spaces
            values = [-1]
    assert values.count(values[0]) == len(values)
    return values[0]


# * * * * * * * * * * * * * * *
# * Player Movement Functions *
# * * * * * * * * * * * * * * *
def swapPlayer(n):
    if n == 1:
        return 2
    else:  # n == 2:
        return 1


def getMove(n, grid, players, error=None):
    '''
    Get a move from the specified player,
    check and make sure it is a valid move.
    '''
    assert (n == 1) or (n == 2)
    move = players[n].getMove(grid, error)
    count = 0
    if move not in grid.getEmptySpaces():
        move = getMove(n, grid, players, move)
    return move


def pickOne(list):
    '''
    Picks one.
    First: a[0], last: a[-1], random: r(0, len(a) - 1)
    '''
    from random import randint as r
    return list[r(0, len(list) - 1)]


# * * * * * * * * * * * * * * * * *
# * Player Finalization Handlers  *
# * * * * * * * * * * * * * * * * *
def handleGameOver(a, b, index, players):
    assert (index == 1) or (index == 2)
    players[index].handleGameOver(a, b)


def quantifyResult(winner, index):
    if winner == -1:  # draw
        return AIADJUST[index - 1]['draw']
    elif (winner == index):  # win
        return AIADJUST[index - 1]['win']
    else:  # loss
        return AIADJUST[index - 1]['lose']


def adjustAI(winner, gamegrids, index, aidata):
    DEBUGFUNC = 0
    #assert gameOver(gamegrids.pop()[0])[0] != 0
    k = quantifyResult(winner, index)
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
            translatedscores = scores = aidata[maxgrid] = \
                Grid([0, 0, 0, 0, 0, 0, 0, 0, 0])
            #raise Exception("newgrid not in data")
        if len(gamegrids) > 2:
            l = AIADJUST[index - 1]['last']
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
            print "\n\t gamegrids: ", gamegrids, "\n\t grid: ", grid,
            print "\n\t move: ", move, "\n\t scores: ", scores,
            print "\n\t adjustedscores: ", adjustedscores,
            print "\n\t index: ", index, "\n\t scores[move]: ", scores[move],
            print "\n\t l*k (change): ", l * k,
            print "\n\t aidata[grid]: ", aidata[maxgrid]


# * * * * * * * * * * * * *
# * Print Game Functions  *
# * * * * * * * * * * * * *
def pushGame(b, a):
    b.reverse()
    b.append(a)
    b.reverse()
    if len(b) > NUMBERLASTGAMES:
        b.pop()
    return b


def printGames(games):
    for game in games:
        printGameGrids(game)


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

# * * * * *
# * Main  *
# * * * * *
def play(players, statdata, games, On, **settings):
    grid = Grid()
    winner = 0
    gamegrids = []
    player = 1
    while winner == 0:
        move = getMove(player, grid, players)
        gamegrids.append((grid[:], move, player))
        grid[move] = player
        player = swapPlayer(player)
        winner = gameOver(grid)
    gamegrids.append((grid[:], move, player))
    analyzeStats(winner, statdata)
    pushGame(games, gamegrids)
    if On('gamegrids'):
        printGameGrids(gamegrids)
    if On('checkdata'):
        # Doesn't work
        copy = dict([(key, aidata[key]) for key in aidata.keys()])
    for index in [1, 2]:
        handleGameOver(winner, gamegrids[:], index, players)
    if On('checkdata'):
        printGameGridsValues(gamegrids, copy)
        printGameGridsValues(gamegrids, aidata)


def main(players, **settings):
    def On(key):
        return key in settings and settings[key] != 0
    if On('timers'):
        timer2 = Timer()
    #printAIData(aidata)
    statdata = [0, 0, 0, []]
    games = []
    if On('times'):
        print "Running", (settings['times']), "games"
    if On('progressbar'):
        bar = ProgressProcess(settings['times'], settings['progressbar'])
        #bar.setNewline()
    if On('timers'):
        timer = Timer(times)
    try:
        if On('times'):
            for a in range(0, settings['times']):
                play(players, statdata, games, On)
                if On('progressbar'):
                    bar.update(a)
            if On('progressbar'):
                bar.success()
                #del bar
        else:
            while (1):
                play(players, statdata, games, On, **settings)
    except UserError:
        print "\nUser quit."
    except KeyboardInterrupt:
        print
        if On('timers'):
            timer.setItter(a)
    except:
        if On('timers'):
            timer.setItter(a)
        handleError()
    finally:
        if On('times'):
            print "Ran", a + 1, " times."
    if On('timers'):
        del timer
    if On('lastfifteen'):
        printGames(games)
    if On('stats'):
        printStats(statdata)
    #printAIData(aidata)


if __name__ == "__main__":
    #players = [None, CompLearning(1, filename='data', record=1), CompTwo(2)]
    players = [None, CompTree(1, filename='datatree', record=0), CompTwo(2)]
    #players = [None, CompTwo(1), Human(2)]
    #players = [None, CompLearning(1, filename='data', record=1), Human(2)]
    # {'record': 1, 'stats': 1, 'lastfifteen': 1, 'timers': 1, \
    # 'times': 100, 'progressbar': 50, 'gamegrids': 1, 'checkdata': 1}
    #main(players, stats=1, lastfifteen=1)
    #main(players, times=4, progressbar=60, lastfifteen=1)
    main(players, times=15, lastfifteen=1, stats=1, gamegrids=1)
    #main([None, CompTwo(1), HumanNumber(2)])
