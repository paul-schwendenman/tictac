#aidata = {}

times = 20

from tictac import *

# * * * * * * * * *
# * New Functions *
# * * * * * * * * *

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
