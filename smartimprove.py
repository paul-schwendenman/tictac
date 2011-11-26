
# * * * * * *
# * Imports *
# * * * * * *

from improveAIData import *
from multiprocessing import Pool, Manager, Process, Lock
from ProgressBar import ProgressTimer

# * * * * * *
# * Globals *
# * * * * * *

times = 1
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

def worker(l, aidata, statdata, games):
    l.acquire()
    data = play(aidata, statdata, games)
    l.release()

# * * * * * * * * * * * *
# * Modified Functions  *
# * * * * * * * * * * * *

def playqq(aidata, statdata):
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
    return aidata, statdata


# * * * * * 
# * Main  * 
# * * * * * 
DEBUG = 0

if __name__ == '__main__':
    #printAIData(aidata)
    timer2 = Timer()
    manager = Manager()
    statdata = manager.list([0, 0, 0, []])
    aidata = manager.dict()
    games = manager.list()
    lock = Lock()
    pool = Pool(5)
    if RECORD:
        aidata = manager.dict(load())
    print "\t\t\t\tRunning %i games" % (times)
    if PROGRESSBAR:
        bar = ProgressTimer(times)
    timer = Timer(times)
    try:
        for a in range(0, times):
                #pool.apply_async(worker, [queue, aidata, statdata])
                #p = Process(target=play, args=[aidata, statdata, games])
                p = Process(target=worker, args=[lock, aidata, statdata, games])
                p.start()
                p.join()
                #pool.apply_async(play, [aidata, statdata])
                #play(aidata, statdata)
                if PROGRESSBAR:
                    bar.update(a)            
        if PROGRESSBAR:
            bar.success()
            del bar
    except KeyboardInterrupt:
        if PROGRESSBAR:
            del bar
        print "Ran", a, "times"
    except:
        if PROGRESSBAR:
            del bar
        print "Ran", a, "times"
        handleError()
    del timer

    #import time
    #time.sleep(.1)
    pool.close()
    pool.terminate()    
    pool.join()

    if PRINTLASTFIFTEEN:
        printGames(games)
    if DISPLAYSTATS:
        printStats(statdata)
    if RECORD:
        dump(aidata)
