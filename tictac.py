'''
 * * * * * * * * * * * *
 * Paul Schwendenman   *
 * 01/29/13            *
 * If you have to ask: *
 * You aren't allowed  *
 * * * * * * * * * * * *
'''

# * * * * * * * * * * *
# * Global Constants  *
# * * * * * * * * * * *

EMPTY = " "
P1 = "X"
P2 = "Y"

# * * * * * * * *
# * Grid Class  *
# * * * * * * * *
class Grid(UserList):
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
            if self.board[p0] == "-": continue
            if self.board[p0] == self.board[p1] == self.board[p2]:
                self.winner = self.board[p0]
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

    def handleGameOver(self, *args):
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
    def getMove(self, grid, error):
        '''
        Get the move.
        '''
        try:
            printXO(grid)
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

    def handleGameOver(self, grid):
        '''
        Finalize the game.
        '''
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


# * * * * * * * * * *
# * Computer Class  *
# * * * * * * * * * *


                                                                                                         for line in lines:
                                                                                                                     p1,p2,p3 = line
                                                                                                                                 if self.board[p1] == "-": continue
                                                                                                                                             if self.board[p1] == self.board[p2] == self.board[p3]:
                                                                                                                                                             self.winner = self.board[p1]
                                                                                                                                                                             return True
