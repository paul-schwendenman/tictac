#aidata = {}

times = 20

from tictac import *

# * * * * * * * * *
# * New Functions *
# * * * * * * * * *

def printAIData(a):
    print len(a)
    for b, c in a.iteritems():
        d = b.returnXO()
        printEighteen(d, c)    

def printEighteen(a, b):
    print "%c %c %c %2i %2i %2i" % (a[0], a[1], a[2], b[0], b[1], b[2])
    print "%c %c %c %2i %2i %2i" % (a[3], a[4], a[5], b[3], b[4], b[5])
    print "%c %c %c %2i %2i %2i" % (a[6], a[7], a[8], b[6], b[7], b[8])
    print

def printGameGrids(a, e):
    b = [d[0].returnXO() for d in a]
    b.append(e.returnXO())
    for c in b:
        print c[0], c[1], c[2], "|",
    print
    for c in b:
        print c[3], c[4], c[5], "|",
    print
    for c in b:
        print c[6], c[7], c[8], "|",
    print
# * * * * * * * * * * * *
# * Modified Functions  *
# * * * * * * * * * * * *
count = 0

def getMove(n, a, c=None):
    b = getMoveComputer(a, c)

    if b not in a.getEmptySpaces():
        global count
        count += 1
        #print "\n\t b: ", b, " is not in ", a.getEmptySpaces()
    if b not in a.getEmptySpaces():
        b = getMove(n, a, b)
        if b not in a.getEmptySpaces():
            raise ValueError
                
    return b



def handleGameOver(a, b, c, d):
    handleGameOverComputer(a, b, c, d)

# * * * * * 
# * Main  * 
# * * * * * 


DEBUG = 0

if __name__ == '__main__':
    global aidata
    aidata = load()
    printAIData(aidata)
    b = [0,0,0, []]
    for a in range(0,times):
        grid = Grid()
        startingplayer = 1
        winner = 0
        gamegrids = []

        player = startingplayer
        while winner == 0:
            move = getMove(player, grid)
            gamegrids.append((grid[:], move, player))
            grid[move] = player
            player = swapPlayer(player)        
            winner, row = gameOver(grid)
        
        #printXO(grid)
        
        analyzeStats(winner, b)
        printGameGrids(gamegrids, grid)

        for index in [1, 2]:
            handleGameOver(winner, startingplayer, gamegrids[:], index)
    
    printStats(b)
    printAIData(aidata)
    dump(aidata)
