times = 100000

# * * * * * *
# * Imports *
# * * * * * *

from improveAIData import *
from multiprocessing import Pool


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

# * * * * * 
# * Main  * 
# * * * * * 
DEBUG = 0

if __name__ == '__main__':
    #printAIData(aidata)
    statdata = [0, 0, 0, []]
    aidata = {}
    pool = Pool(5)
    if RECORD:
        aidata = load()
    print "\t\t\t\tRunning %i games" % (times)
    if PROGRESSBAR:
        bar = ProgressBar(times)
    try:
        for a in range(0, times):
                print len(pool.apply_async(play, [aidata, statdata]).get(timeout = 1))
                #play(aidata, statdata)
                if PROGRESSBAR:
                    bar.update(a)            
    except KeyboardInterrupt:
        print
    except:
        print
        handleError()
    printStats(statdata)
    #printAIData(aidata)
    if RECORD:
        dump(aidata)

    #import time
    #time.sleep(.1)
    pool.close()
    pool.terminate()    
    pool.join()
