times = 4000

# * * * * * *
# * Imports *
# * * * * * *

from tictac import *
from ProgressBar import ProgressLock
from Timer import Timer
from multiprocessing import Process, Lock

# * * * * * *
# * Globals *
# * * * * * *

RECORD = 1
PROGRESSBAR = 1
SMARTAI = 0
PRINTGAMEGRIDS = 0
PRINTLASTFIFTEEN = 1
DISPLAYSTATS = 1
CHECKAIDATA = 0
SHOWGAME = 0

# * * * * * * * * *
# * New Functions *
# * * * * * * * * *

# * * * * * * * * * * * *
# * Modified Functions  *
# * * * * * * * * * * * *
count = 0

def getMove(n, a, aidata, c=None):
    if n == 1:
        b = getMoveComputer(a, c, aidata)
    else:
        assert n == 2
        if SMARTAI:
            b = getMoveSmarter(n, a, c, aidata)
        else:
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
def play(aidata, statdata, games):
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
        winner = gameOver(grid)
    
    gamegrids.append((grid[:], move, player))
    analyzeStats(winner, statdata)
    pushGame(games, gamegrids)
    if SHOWGAME:
        printXO(grid)
    if PRINTGAMEGRIDS:
        printGameGrids(gamegrids)
    if CHECKAIDATA:
        copy = dict([(key, aidata[key]) for key in aidata.keys()])
    for index in [1, 2]:
        handleGameOver(winner, startingplayer, gamegrids[:], index, aidata)
    if CHECKAIDATA:
        printGameGridsValues(gamegrids, copy)
        printGameGridsValues(gamegrids, aidata)
    return gamegrids

DEBUG = 0

if __name__ == '__main__':
    timer2 = Timer()
    #printAIData(aidata)
    statdata = [0, 0, 0, []]
    aidata = {}
    games = []
    lock = Lock()
    if RECORD:
        aidata = load()
    print "\t\t\t\tRunning %i games" % (times)
    if PROGRESSBAR:
        bar = ProgressLock(times, 50)
        #bar.setNewline()
    timer = Timer(times)
    
    try:
        for a in range(0, times):
                game = play(aidata, statdata, games)
                if PROGRESSBAR:
                    p = Process(target=bar.update, args=[a, lock])
                    p.start()
                    #p.join()
                    #bar.update(a)            
        if PROGRESSBAR:
            bar.success()
    except KeyboardInterrupt:
        timer.setItter(a)
    except:
        timer.setItter(a)
        handleError()
    finally:
        if PROGRESSBAR:
            del bar
        lock.acquire()
        print "Ran", a, " times."
        lock.release()
        
    del timer
    if PRINTLASTFIFTEEN:
        printGames(games)
    if DISPLAYSTATS:
        printStats(statdata)
    #printAIData(aidata)
    if RECORD:
        dump(aidata)

