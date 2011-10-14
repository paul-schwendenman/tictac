aidata = {}

times = 100

from tictac import *

# * * * * * * * * * * * * 
# * Modified Functions  * 
# * * * * * * * * * * * *
def getMove(n, a):
    b = -1
    while b not in a.getEmptySpaces():
        b = getMoveComputer(a)
        if b not in a.getEmptySpaces():
            print "\n\t b: ", b, " is not in ", a.getEmptySpaces()
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
    b = [0,0,0, []]
    for a in range(0,times):
        grid = Grid()
        startingplayer = 1
        winner = 0
        gamegrids = []

        player = startingplayer
        while winner == 0:
            move = getMove(player, grid)
            gamegrids.append((grid.toString(), move, player))
            grid[move] = player
            player = swapPlayer(player)        
            winner, row = gameOver(grid)
        
        printXO(grid)
        
        analyzeStats(winner, b)

        for index in range(1,3):
            handleGameOver(winner, startingplayer, gamegrids, index)
    
    printStats(b)
    
    dump(aidata)