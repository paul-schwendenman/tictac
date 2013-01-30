'''
 * * * * * * * * * * * *
 * Paul Schwendenman   *
 * 01/29/13            *
 * If you have to ask: *
 * You aren't allowed  *
 * * * * * * * * * * * *
'''

# * * * * * * * * * * *
# * Libraries         *
# * * * * * * * * * * *

from random import randint, random


# * * * * * * * * * * *
# * Global Constants  *
# * * * * * * * * * * *

EMPTY = " "
P1 = "X"
P2 = "O"

# * * * * * * * *
# * Grid Class  *
# * * * * * * * *
class Grid():
    '''
    The Basic 3 by 3 grid
    '''
    def __init__(self):
        self.data = [EMPTY for i in range(0, 9)]
        self.history = []
        self.winner = None

    def __str__(self):
        '''
        Prints the list as a continuous word.
        '''
        a = ''.join([str(a) for a in self.data])
        return a

    def __getitem__(self, i):
        return self.data[i]
    
#    def __hash__(self):
#        '''
#        Okay to hash despite being mutable, hash reveals state not variable
#        '''
#        #return int(self.__str__())
#        #return Translate.Hash(self)
    
    def getEmptySpaces(self):
        '''
        Return the index of all positions with value '0'
        '''
        return [a for a, b in enumerate(self.data) if b == EMPTY]

    def setMark(self, pos, marker):
        '''
        Set the players marker on the board.
        '''
        self.history.append(pos)
        self.data[pos] = marker

    def undoMark(self):
        '''
        Undo the last mark on the board.
        '''
        pos = self.history.pop()
        self.data[pos] = EMPTY
        self.winner = None
        return pos

    def prettyPrint(self):
        a = self.data
        print " %c | %c | %c " % (a[0], a[1], a[2])
        print "---+---+---"
        print " %c | %c | %c " % (a[3], a[4], a[5])
        print "---+---+---"
        print " %c | %c | %c " % (a[6], a[7], a[8])

    def isDone(self):
        lines = [(0,1,2), (3,4,5), (6,7,8),
                 (0,3,6), (1,4,7), (2,5,8),
                 (0,4,8), (2,4,6)]
        
        for p0, p1, p2 in lines:
            if self.data[p0] == EMPTY: continue
            if self.data[p0] == self.data[p1] == self.data[p2]:
                self.winner = self.data[p0]
                return True

        if self.data.count(EMPTY) == 0:
            self.winner = EMPTY
            return True

        return False

    def map(self, f):
        lines = [(0,1,2), (3,4,5), (6,7,8),
                 (0,3,6), (1,4,7), (2,5,8),
                 (0,4,8), (2,4,6)]
        g = self.data
        return [f(g[l[0]], g[l[1]], g[l[2]]) for l in lines]        

    def filter(self, f):
        lines = [(0,1,2), (3,4,5), (6,7,8),
                 (0,3,6), (1,4,7), (2,5,8),
                 (0,4,8), (2,4,6)]
        g = self.data
        return [l for l in lines if f(g[l[0]], g[l[1]], g[l[2]])]        

    def testDone(self):
        f = lambda a, b, c: a != EMPTY and a == b == c
        if True in self.map(f):
            return True
        
        if self.data.count(EMPTY) == 0:
            self.winner = EMPTY
            return True
        return False


# * * * * * * * * *
# * Player Class  *
# * * * * * * * * *
class Player():
    '''
    The base player class for a game.
    '''
    def __init__(self, symbol):
        self.symbol = symbol

    def getMove(self, *args):
        '''
        This function should take a variable number
        of inputs and return a single number.

        Typically takes two inputs:
        - the current grid
        - an error raised flag

        Output:
        - should be in [0...8] (3x3 grid)
        '''
        pass

    def finalize(self, *args):
        '''
        The method should handle all end game
        activities for the player.

        Typical Input:
        - winner
        - startingplayer
        - gamegrids
        - index, aidata <-- local
        '''
        pass

# * * * * * * * * *
# * Human Class   *
# * * * * * * * * *

class Human(Player):
    '''
    Player designed for human input.
    '''
    def getMove(self, grid, error=None):
        '''
        Get the move.
        '''
        try:
            print "%s's move" % (self.symbol)
            grid.prettyPrint()
            if error != None:
                print "Invalid Move: ", error + 1
            input = raw_input("Move? ")[0]
            if input == "h" or input == "H":
                self.printHelp()
                input = raw_input("Move? ")[0]
            else:
                return int(input) - 1
        except (ValueError, IndexError, KeyError, EOFError, KeyboardInterrupt):
            raise UserError("User Quit")

    def finalize(self, grid):
        '''
        Finalize the game.
        '''
        grid.prettyPrint()
        winner = grid.winner
        if winner == EMPTY:
            print "You tied!"
        elif (winner == self.symbol):
            print "You won! computer lost."
        else:
            print "You lost, computer won."
        
    @staticmethod
    def printHelp():
        '''
        Helpful grid for seeing desired output
        
        Move to player.
        '''
        print
        print " 1 | 2 | 3 "
        print "---+---+---"
        print " 4 | 5 | 6 "
        print "---+---+---"
        print " 7 | 8 | 9 "

class UserError(Exception):
    '''
    When the User quits pass a unique exception to
    eliminate confusion between other valid exceptions.
    '''
    pass

# * * * * * * * * * *
# * Computer Class  *
# * * * * * * * * * *

class Comp(Player):
    def getMove(self, grid, *args):
        # Win
        f = lambda *a: a.count(self.symbol) == 2 and a.count(EMPTY) == 1
        r = grid.filter(f)
        if len(r) > 0:
            a, b, c = r[0]
            if grid[a] == EMPTY:
                return a
            elif grid[b] == EMPTY:
                return b
            else:
                assert grid[c] == EMPTY
                return c
        # Don't Lose
        f = lambda *a: a.count(self.symbol) == 0 and a.count(EMPTY) == 1
        r = grid.filter(f)
        if len(r) > 0:
            a, b, c = r[0]
            if grid[a] == EMPTY:
                return a
            elif grid[b] == EMPTY:
                return b
            else:
                assert grid[c] == EMPTY
                return c
        # Try win
        # Block Loss
        # Finish Line     
        return pickOne(grid.getEmptySpaces())

    def finalize(self, *args):
        pass

def pickOne(list):
    '''
    Picks one.
    First: a[0], last: a[-1], random: r(0, len(a) - 1)
    '''
    return list[randint(0, len(list) - 1)]

class CompProb(Player):
    def __init__(self, *args):
        Player.__init__(self, *args)
        self.dict = {}

    def getMove(self, grid, error = None):
        if grid not in self.dict:
            self.dict[grid] = [1., 1., 1., 1., 1., 1., 1., 1., 1.]
        lst = self.dict[grid]
        
        if error:
            print error, lst
            lst[error] = 0
            print error, lst
            self.dict[grid] = lst
            
        pdfs = [item/sum(lst) for item in lst]
        
        num = random()
        print "n:", num       
        accum = 0
        for i, pdf in enumerate(pdfs):
            accum += pdf
            print "a:", i, accum
            if num < (accum):
                return i
        print "s:", accum
        return i

    def finalize(self, grid, *args):
        print self.dict
        if grid.winner == self.symbol:
            move = grid.undo()
            self.dict[grid][move] += 2
            
        elif grid.winner == EMPTY:
            move = grid.undo()
            self.dict[grid][move] += 1
        
        else:
            pass 
        print self.dict
        

# * * * * *
# * Main  *
# * * * * *

def main(players):
    grid = Grid()
    current = 0
    error = None
    
    while not grid.isDone():
        move = players[current].getMove(grid, error)
        if move in grid.getEmptySpaces():
            grid.setMark(move, players[current].symbol)
            current = 1 - current
            error = None
        else:
            error = move
    
    assert grid.testDone()
    
    for player in players:
        player.finalize(grid)

if __name__ == "__main__":
    players = [Human(P1), CompProb(P2)]
    main(players)
