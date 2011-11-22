times = 1000

# * * * * * *
# * Imports *
# * * * * * *

from tictac import *
from ProgressBar import ProgressBar

# * * * * * *
# * Globals *
# * * * * * *

RECORD = 1
PROGRESSBAR = 1

# * * * * * * * * *
# * New Functions *
# * * * * * * * * *

# * * * * * * * * * * * *
# * Modified Functions  *
# * * * * * * * * * * * *
count = 0

def getMove(n, a, aidata, c=None):
    b = getMoveComputer(a, c, aidata)

    if b not in a.getEmptySpaces():
        global count
        count += 1
        #print "\n\t b: ", b, " is not in ", a.getEmptySpaces()
    if b not in a.getEmptySpaces():
        b = getMove(n, a, aidata, b)
        if b not in a.getEmptySpaces():
            raise ValueError
    return b



def handleGameOver(a, b, c, d, e):
    handleGameOverComputer(a, b, c, d, e)

# * * * * * 
# * Main  * 
# * * * * * 
def play(aidata, statdata):
    grid = Grid()
    startingplayer = 1
    winner = 0
    gamegrids = []

    player = startingplayer
    while winner == 0:
        move = getMove(player, grid, aidata)
        gamegrids.append((grid[:], move, player))
        grid[move] = player
        player = swapPlayer(player)        
        winner, row = gameOver(grid)
    
    gamegrids.append((grid[:], move, player))
    analyzeStats(winner, statdata)
    #printXO(grid)
    #printGameGrids(gamegrids)
    #printGameGridsValues(gamegrids, aidata)
    #copy = dict([(key, aidata[key]) for key in aidata.keys()])
    for index in [1, 2]:
        handleGameOver(winner, startingplayer, gamegrids[:], index, aidata)
    #printGameGridsValues(gamegrids, copy)
    #printGameGridsValues(gamegrids, aidata)
    return aidata

DEBUG = 0

if __name__ == '__main__':
    #printAIData(aidata)
    statdata = [0, 0, 0, []]
    aidata = {}
    if RECORD:
        aidata = load()
    print "\t\t\t\tRunning %i games" % (times)
    if PROGRESSBAR:
        bar = ProgressBar(times, 50)
        #bar.setNewline()
    try:
        for a in range(0, times):
                play(aidata, statdata)
                if PROGRESSBAR:
                    bar.update(a)            
        if PROGRESSBAR:
            bar.success()
            del bar
    except KeyboardInterrupt:
        if PROGRESSBAR:
            del bar
    except:
        if PROGRESSBAR:
            del bar
        handleError()
    printStats(statdata)
    #printAIData(aidata)
    if RECORD:
        dump(aidata)

