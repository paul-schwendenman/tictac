times = 1000

# * * * * * *
# * Imports *
# * * * * * *

from tictac import *
from ProgressBar import ProgressProcess
from Timer import Timer

# * * * * * *
# * Globals *
# * * * * * *

RECORD = 1
PROGRESSBAR = 1
SMARTAI = 0
PRINTGAMEGRIDS = 0
PRINTLASTFIFTEEN = 0
DISPLAYSTATS = 1
CHECKAIDATA = 0
SHOWGAME = 0
TIMERS = 1

# * * * * * * * * *
# * New Functions *
# * * * * * * * * *

# * * * * * * * * * * * *
# * Modified Functions  *
# * * * * * * * * * * * *

# * * * * * 
# * Main  * 
# * * * * * 
if __name__ == '__main__':
    if TIMERS:
        timer2 = Timer()
    #printAIData(aidata)
    statdata = [0, 0, 0, []]
    aidata = {}
    games = []
    players = [None, CompLearning(1), CompTwo(2)]
    if RECORD:
        aidata = load()
    players[1].setAIdata(aidata)
    print "\t\t\t\tRunning %i games" % (times)
    if PROGRESSBAR:
        bar = ProgressProcess(times, 50)
        #bar.setNewline()
    if TIMERS:
        timer = Timer(times)
    try:
        for a in range(0, times):
                play(players, statdata, games)
                if PROGRESSBAR:
                    bar.update(a)            
        if PROGRESSBAR:
            bar.success()
            #del bar
    except KeyboardInterrupt:
        print
        if TIMERS:
            timer.setItter(a)
    except:
        if TIMERS:
            timer.setItter(a)
        handleError()
    finally:
        print "Ran", a, " times."
        
    if TIMERS:
        del timer
    if PRINTLASTFIFTEEN:
        printGames(games)
    if DISPLAYSTATS:
        printStats(statdata)
    #printAIData(aidata)
    if RECORD:
        dump(aidata)

