# * * * * * *
# * Globals *
# * * * * * *

console = 0

# * * * * * *
# * Imports *
# * * * * * *

from tictac import Grid, pickPlay, printXO, handleError

# * * * * * *
# * Code    *
# * * * * * *

a = Grid([1, 1, 0, 2, 0, 2, 0, 1, 1])
printXO(a)

b = [(0, 1, 2), (3, 4, 5), (6, 7, 8), \
     (0, 3, 6), (1, 4, 7), (2, 5, 8), \
     (0, 4, 8), (2, 4, 6)]

def mapGrid(f, grid):
    lines = [(0, 1, 2), (3, 4, 5), (6, 7, 8), \
         (0, 3, 6), (1, 4, 7), (2, 5, 8), \
         (0, 4, 8), (2, 4, 6)]
    return [f(line, grid) for line in lines]    

for qq in zip(b, mapGrid(pickPlay, a)):
    print qq

def filterLinesNone(a):
    return a[0] != None

def filterLinesOne(a):
    return a[0] == 1

def filterLinesTwo(a):
    return a[0] == 2

nn = filter(filterLinesNone, mapGrid(pickPlay, a))
print 
mm = [item[1] for item in filter(filterLinesOne, mapGrid(pickPlay, a))]
print mm



# * * * * * *
# * Console *
# * * * * * *

while console:
    try:
        input = raw_input(">> ")
        exec(input)
    except EOFError, KeyboardInterrupt:
        break
    except:
        handleError()