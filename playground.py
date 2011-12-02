# * * * * * *
# * Globals *
# * * * * * *

console = 0

# * * * * * *
# * Imports *
# * * * * * *
import tictac
from tictac import Grid, printXO, handleError
from tictac import pickOne, gameOver, translateGridMax
from ProgressBar import ProgressProcess
from Timer import Timer, units


# * * * * * *
# * Code    *
# * * * * * *
'''
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
grids = list(set([translateGridMax(grid)[0] for grid in grids]))
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
from tictac import translateArray, translateGridReverse, printGrids, printNine
a = range(0, 9)
b = translateArray(a)
for d in range(0, 8):
    print "-" * 13, d, '-' * 13
    c = translateArray(b[d])
    printGrids([a, translateGridReverse(b[d], d), Grid(), b[d], c[d]])
    printGrids(b)
    printGrids(c)


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
