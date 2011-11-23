
# * * * * * *
# * Imports *
# * * * * * *

from improveAIData import *
from multiprocessing import Pool, Queue


# * * * * * *
# * Globals *
# * * * * * *

times = 50000
RECORD = 1
PROGRESSBAR = 1

# * * * * * * * * *
# * New Functions *
# * * * * * * * * *

def worker(q, aidata, statdata):
    data = play(aidata, statdata)
    q.put(data)

# * * * * * * * * * * * *
# * Modified Functions  *
# * * * * * * * * * * * *

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
    aidata = {}
    for index in [1, 2]:
        handleGameOver(winner, startingplayer, gamegrids[:], index, aidata, ignoreai=1)
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
    queue = Queue()
    statdata = [0, 0, 0, []]
    aidata = {}
    pool = Pool(5)
    if RECORD:
        aidata = load()
    print "\t\t\t\tRunning %i games" % (times)
    if PROGRESSBAR:
        bar = ProgressBar(times)
    timer = Timer(times)
    try:
        for a in range(0, times):
                #pool.apply_async(worker, [queue, aidata, statdata])
                pool.apply_async(play, [aidata, statdata])
                #play(aidata, statdata)
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
    del timer
    printStats(statdata)
    #printAIData(aidata)
    if RECORD:
        dump(aidata)

    #import time
    #time.sleep(.1)
    pool.close()
    pool.terminate()    
    pool.join()
