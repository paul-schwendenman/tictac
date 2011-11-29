# * * * * * *
# * Globals *
# * * * * * *

console = 1

# * * * * * *
# * Imports *
# * * * * * *

import tictac
from tictac import Grid, printXO, handleError
from ProgressBar import ProgressTimer
from Timer import units

# * * * * * *
# * Code    *
# * * * * * *

a = Grid([1, 1, 0, 2, 0, 2, 0, 1, 1])
printXO(a)

a = ProgressTimer(234, 60)


def func(**args):
    print args
    if 'a' in args and args['a'] == 1:
        print "works"

# * * * * * *
# * Console *
# * * * * * *

while console:
    try:
        print
        input = raw_input(">> ")
        exec(input)
    except EOFError, KeyboardInterrupt:
        break
    except:
        handleError()
