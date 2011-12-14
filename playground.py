# * * * * * *
# * Globals *
# * * * * * *

console = 0

# * * * * * *
# * Imports *
# * * * * * *
import tictac
from tictac import Grid, printXO, handleError
from tictac import pickOne, gameOver, Translate
from ProgressBar import ProgressProcess
from Timer import Timer, units


# * * * * * *
# * Code    *
# * * * * * *


'''
# * * * * * * * *
# * Every Grid  *
# * * * * * * * *
def func(**args):
    print args
    if 'a' in args and args['a'] == 1:
        print "works"

grids = []
timer = Timer(19683)
count = 0
for a in [0, 1, 2]:
    for b in [0, 1, 2]:
        for c in [0, 1, 2]:
            for d in [0, 1, 2]:
                for e in [0, 1, 2]:
                    for f in [0, 1, 2]:
                        for g in [0, 1, 2]:
                            for h in [0, 1, 2]:
                                for i in [0, 1, 2]:
                                    grids.append(Grid([a, b, c, d, \
                                                       e, f, g, h, i]))
print "Total possible games:", len(grids), "\n\t",
del timer


def everyother(grid):
    return (abs(grid.count(1) - grid.count(2)) <= 1)


def everyother_one(grid):
    return (grid.count(1) - grid.count(2) in [0, 1])


def everyother_two(grid):
    return (grid.count(1) - grid.count(2) in [0, -1])


timer = Timer(len(grids))
grids = (filter(everyother_one, grids))
print "With proper alternation:", len(grids), "\n\t",
del timer


def filterGameOver(grid, y=None):
    try:
        x = gameOver(grid)
    except:
        return 0
    else:
        if y == None:
            return 1
        elif x == y:
            return 1
        else:
            return 0
getOneType_One = lambda grid: filterGameOver(grid, 1)
getOneType_None = lambda grid: filterGameOver(grid, 0)
getOneType_Tie = lambda grid: filterGameOver(grid, -1)
getOneType_Two = lambda grid: filterGameOver(grid, 2)

timer = Timer(len(grids))
grids = (filter(filterGameOver, grids))
print "No more than one winner:", len(grids), '\n\t',
del timer

timer = Timer(len(grids))
grids = list(set([Translate.GridMax(grid)[0] for grid in grids]))
print "Translations:", len(grids), '\n\t',
del timer

#gridsset = grids1 & grids2 & grids3
print "And together now...", len(grids)


def po(aa=grids):
    printXO(pickOne(aa))

timer = Timer()
aa = filter(getOneType_One, grids)
bb = filter(getOneType_Two, grids)
cc = filter(getOneType_Tie, grids)
dd = filter(getOneType_None, grids)
print "Wins", len(aa), "Losses", len(bb), "Ties", len(cc), "Rest", len(dd)
print "\t",
del timer
'''
'''
from tictac import printGrids, printNine
a = range(0, 9)
b = Translate.Array(a)
for d in range(0, 8):
    print "-" * 13, d, '-' * 13
    c = Translate.Array(b[d])
    printGrids([a, Translate.GridReverse(b[d], d), Grid(), b[d], c[d]])
    printGrids(b)
    printGrids(c)
'''
'''
# * * * * * * * * * * * * *
# * Demo Guess Difference *
# * * * * * * * * * * * * *

from tictac import printGameGrids, printGrids

def printSequence(a, b):
    z = Grid()
    c, t = Translate.GridMax(a)
    d = Translate.GridMax(b)[0]
    v = Translate.GuessDifference(c, d)
    e = v[0][0]
    f = Translate.GridReverse(e - c, t)
    g = Translate.Grid(b, t)
    h = Translate.GridReverse(g - c, t)

    print "The actual game:"
    printGameGrids([(a,), (b,), (b,), (z - z,), (b - a,)],  \
        "Move: " + str((b - a).index(1)))
    print "The correct guess:"
    printGameGrids([(c,), (z,), (g,), (g - c,), (h,)],  \
        "Move: " + str((h).index(1)))
    print "and their solutions:"
    for w in v:
        e = w[0]
        f = Translate.GridReverse(e - c, t)
        printGameGrids([(c,), (d,), (e,), (e - c,), (f,)], \
            "Move: " + str((f).index(1)))
    print "All possible guesses"
    printGameGrids(v)

a = Grid([0, 0, 1, 0, 0, 2, 1, 0, 0])
b = Grid([1, 0, 1, 0, 0, 2, 1, 0, 2])
printSequence(a, b)
a = Grid([0, 0, 1, 2, 1, 0, 0, 0, 0])
b = Grid([1, 0, 1, 2, 1, 0, 2, 0, 0])
printSequence(a, b)
a = Grid([0, 0, 1, 0, 2, 0, 0, 0, 0])
b = Grid([1, 0, 1, 0, 2, 0, 2, 0, 0])
printSequence(a, b)

print '*' * 43
'''

from tictac import Grid, gameOver, printGameGrids, Translate

def fillTwo(grid):
    results = []
    if gameOver(grid) != 0:
        return gameOver(grid)
        #return [grid]

    if grid.count(1) > grid.count(2):
        return fillOne(grid)

    for x in grid.getEmptySpaces():
        grid1 = grid[:]
        grid1[x] = 1
        if gameOver(grid1) != 0:
            results.append(grid1)
            continue
        results += fillOne(grid1)
    return results

def fillOne(grid):
    results = []
    for o in grid.getEmptySpaces():
        grid1 = grid[:]
        grid1[o] = 2
        results.append(grid1)
    return results
    


def reduceDuplicates(initlist):
    return list(set(initlist))

def addDict(self, other):
    for key in other.keys():
        if key in self and self[key] != 'Depth':
            assert self[key] == other[key]
        else:
            self[key] = other[key]
            del other[key]


a = Grid([1, 2, 2, 2, 1, 1, 0, 0, 0])
            
def finishTree(grid, depth=0):
    tree = {}
    grid = Translate.GridMax(grid)[0]
    if depth > 5:
        return {grid: 'Depth'}
    if gameOver(grid) != 0:
        tree[grid] = gameOver(grid)
    else:
        tree[grid] = fillTwo(grid)
        for item in fillTwo(grid):
            addDict(tree, finishTree(item, depth + 1))
    return tree


timer = Timer()
#a = Grid([1, 2, 1, 2, 1, 0, 0, 0, 0])
a = Grid()
#tree = finishTree(a)
del timer

'''
# For Multiprocessing
grids = filter(lambda a: tree[a] == 'Depth', tree.keys()
for grid in grids:
    addDict(tree, finishTree(grid))
'''
def printTree(tree):
    for item in sorted(tree.keys()):
        #print item, tree[item]
        if isinstance(tree[item], list):
            printGameGrids([(item1,) for item1 in [item, Grid()] + tree[item]])
        elif isinstance(tree[item], int) or  isinstance(tree[item], str):
            printGameGrids([(item1,) for item1 in [item, Grid()]], '', tree[item])
    print "Length:", len(tree)

from cPickle import dump, load
file = open("tree", "r")
#dump(tree, file)
printTree(load(file))

file.close()

# * * * * * *
# * Console *
# * * * * * *

while console:
    try:
        input = raw_input(">> ")
    except EOFError, KeyboardInterrupt:
        break
    timer = Timer()
    try:
        exec(input)
    except:
        handleError()
    del timer
