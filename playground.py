# * * * * * *
# * Globals *
# * * * * * *

console = 1

# * * * * * *
# * Imports *
# * * * * * *
import tictac
from tictac import Grid, printXO, handleError, pickOne, gameOver, translateGridMax
from ProgressBar import ProgressProcess
from Timer import Timer, units

# * * * * * *
# * Code    *
# * * * * * *

a = Grid([1, 1, 0, 2, 0, 2, 0, 1, 1])
printXO(a)

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
                                    grids.append(Grid([a, b, c, d, e, f, g, h, i]))
print "Total possible games:", len(grids), "\n\t",
del timer

def everyother(grid):
    return (abs(grid.count(1) - grid.count(2)) <= 1)

timer = Timer(19683)
timer2 = Timer(8953)
grids = filter(everyother, grids)
print "With proper alternation:", len(grids), "\n\t",
del timer
print "\t",
del timer2

def onewin(grid):
    try:
        gameOver(grid)
    except:
        return 0
    else:
        return 1
timer = Timer(8953)
timer2 = Timer(8725)
grids = filter(onewin, grids)
print "No more than one winner:", len(grids), '\n\t',
del timer
print "\t",
del timer2

timer = Timer(8725)
grids = list(set([translateGridMax(grid)[0] for grid in grids]))
print "Translations:", len(grids), '\n\t',
del timer


def po():
    printXO(pickOne(grids))
        
'''
bar = ProgressProcess(19683)
count = 0
for grid in grids2:
    count += 1
    bar.update(count)
    while grids2.count(grid) > 1:
        grids2.remove(grid)
bar.success()
print len(grids2)
'''


# * * * * * *
# * Console *
# * * * * * *

while console:
    try:
        print
        input = raw_input(">> ")
        exec(input, out)
        print out
    except EOFError, KeyboardInterrupt:
        break
    except:
        handleError()
