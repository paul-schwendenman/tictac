# * * * * * *
# * Globals *
# * * * * * *

console = 1

# * * * * * *
# * Imports *
# * * * * * *

import tictac
from tictac import Grid, printXO, handleError
from tictac import gameOver, gameOverFilter

# * * * * * *
# * Code    *
# * * * * * *

a = Grid([1, 1, 0, 2, 0, 2, 0, 1, 1])
printXO(a)

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