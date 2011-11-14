times = 2

from tictac import *

# * * * * * * * * *
# * New Functions *
# * * * * * * * * *

class ProgressBar:
    def __init__(self, max):
        self.max = max
        self.number = 0
        print
        self.display()
    def update(self, current):
        number = (current * 100) / self.max + 1
        if number != self.number:
            self.number = number
            self.display()
        if self.number == 100:
            print 
    def display(self):
        print "\r\t[" + "*" * self.number + " " * (100 - self.number) + "] %2i%%" % (self.number),
    

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
    #printGameGrids(gamegrids, grid)
    for index in [1, 2]:
        handleGameOver(winner, startingplayer, gamegrids[:], index, aidata)

DEBUG = 0

if __name__ == '__main__':
    #printAIData(aidata)
    statdata = [0, 0, 0, []]
    aidata = load()
    #bar = ProgressBar(times)
    for a in range(0, times):
#        try:
#            aidata = load()
            play(aidata, statdata)
            #bar.update(a)            
#            dump(aidata)
#        except:
#            handleError()

    printStats(statdata)
    #printAIData(aidata)
    dump(aidata)

