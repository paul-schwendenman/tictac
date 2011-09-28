# * * * * * * * * * * * *  
# * Paul Schwendenman   *
# * 09/20/11            * 
# * If you have to ask: * 
# * You aren't allowed  * 
# * * * * * * * * * * * * 

# * * * * * * *
# * Imported  * 
# * * * * * * *
import pickle
from UserList import UserList

# * * * * * * * * * * *
# * Global Variables  * 
# * * * * * * * * * * *
aidata = {}
  # this is a dictionary of numbers that point to a dictionary with choices and success rates
  # ex. aidata = {121000000 : [2,3,2, 3,4,4, 1,-3,4]} where [2]=3
statdata = [0,0,0, []]


DEBUG = 0

# * * * * * * * *
# * Grid Class  * 
# * * * * * * * *
class Grid(UserList):
  def __init__(self, initlist=None):
    #From the userlist 
    self.data = []
    if initlist is not None:
      if type(initlist) == type(self.data):          
        self.data[:] = initlist
      elif isinstance(initlist, UserList):
        self.data[:] = initlist.data[:] 
      else:                              
        self.data = list(initlist)
    else:                              
      self.data = [0] * 9
    if DEBUG:
      print self
      
  def __str__(self):
    a=''.join([str(a) for a in self.data])
    return a

  def toString(self):
    return ':'.join([str(a) for a in self.data])
    
  def fromString(self, a):
    self.data = [int(b) for b in a.split(':')]
  
  def returnXO(self):
    b = {0: " ",1: "X", 2: "O"}
    return [b[a] for a in self.data]

  def getEmptySpaces(self):
    return [a for a, b in enumerate(self.data) if b == 0]

  def getUsedSpaces(self):
    return [a for a, b in enumerate(self.data) if b != 0]


# * * * * * * * * * * * * * *
# * Grid Display Functions  * 
# * * * * * * * * * * * * * *
def printXO(b):
  printGrid(b.returnXO())
  
  
def printGrid(a):
  print
  print " %c | %c | %c " % (a[0], a[1], a[2])
  print "---+---+---"
  print " %c | %c | %c " % (a[3], a[4], a[5])
  print "---+---+---"
  print " %c | %c | %c " % (a[6], a[7], a[8])

def printHelp():
  print
  print " 1 | 2 | 3 "
  print "---+---+---"
  print " 4 | 5 | 6 "
  print "---+---+---"
  print " 7 | 8 | 9 "

# * * * * * * * * * * * * * * * *
# * Mostly Depricated Functions * <-- Remove? 
# * * * * * * * * * * * * * * * * 
def convertGridToNumber(a):
  c = 0
  for b in a:  
    c = c * 10
    c = c + b
  return c

def convertNumberToGrid(a):
  b = []
  for c in str(a):
    b.append(int(c))
  return b
  
def convertGridToXO(a):
  b = []
  c = {0: " ",1: "X", 2: "O"}
  for e in a:
    b.append(c[e])
  return b

def getEmptySpaces(a):
  b = []
  for c, d in enumerate(a):
    if d == 0:
      b.append(c)
  return b

def getUsedSpaces(a):
  b = []
  for c, d in enumerate(a):
    if d != 0:
      b.append(c)
  return b

def getInitialValues(a):
  b = {"0": 0, "1": -2, "2": -2}
  return [b[c] for c in a.split(":")]


# * * * * * * * * * * * * 
# * Game Over Function  * <-- Add to Grid? 
# * * * * * * * * * * * *
def gameOver(a):
  if a[0] == a[1] == a[2] and a[0] != 0:
    return (a[0], 1)
  elif a[3] == a[4] == a[5] and a[3] != 0:
    return (a[3], 2)
  elif a[6] == a[7] == a[8] and a[6] != 0:
    return (a[6], 3)

  elif a[0] == a[3] == a[6] and a[0] != 0:
    return (a[0], 4)
  elif a[1] == a[4] == a[7] and a[1] != 0:
    return (a[1], 5)
  elif a[2] == a[5] == a[8] and a[2] != 0:
    return (a[2], 6)

  elif a[0] == a[4] == a[8] and a[0] != 0:
    return (a[0], 7)
  elif a[6] == a[4] == a[2] and a[2] != 0:
    return (a[6], 8)
  elif sum(a) >= 13:
    return (-1, 0)
  else:
    return (0, 0)

# * * * * * * * * * * * *
# * Translation Helpers *
# * * * * * * * * * * * *

def join(a):
  return ":".join(a)

def split(a):
  if type(a) == type(""):
    return a.split(":")
  elif type(a) == Grid:
    return a
  elif type(a) == type([]):
    return a
  else:
    print type(a)
    raise TypeError

# * * * * * * * * * * * * *  
# * Translation Functions * 
# * * * * * * * * * * * * * 
def translateMove(a, c):
  b = [[0,1,2,  3,4,5,  6,7,8], [2,1,0, 5,4,3, 8,7,6], [6,7,8, 3,4,5, 0,1,2], [8,5,2, 7,4,1, 6,3,0], [0,3,6, 1,4,7, 2,5,8], [6,3,0, 7,4,1, 8,5,2], [8,7,6, 5,4,3, 2,1,0], [2,5,8, 1,4,7, 0,3,6]]
  if type(a) == type(""):
    a = int(a)
  return  b[c].index(a)

def translateGrid(a, e):
  return translateArray(a)[e]
#  b = [[0,1,2,  3,4,5,  6,7,8], [2,1,0, 5,4,3, 8,7,6], [6,7,8, 3,4,5, 0,1,2], [8,5,2, 7,4,1, 6,3,0], [0,3,6, 1,4,7, 2,5,8], [6,3,0, 7,4,1, 8,5,2], [8,7,6, 5,4,3, 2,1,0], [2,5,8, 1,4,7, 0,3,6]]
#  return ":".join([str(a[f]) for f in b[e]])

def translateArray(a):
  a = split(a)
  b = [[0,1,2,  3,4,5,  6,7,8], [2,1,0, 5,4,3, 8,7,6], [6,7,8, 3,4,5, 0,1,2], [8,5,2, 7,4,1, 6,3,0], [0,3,6, 1,4,7, 2,5,8], [6,3,0, 7,4,1, 8,5,2], [8,7,6, 5,4,3, 2,1,0], [2,5,8, 1,4,7, 0,3,6]]
  return [":".join([str(a[f]) for f in e]) for e in b]


def findMaxTranslation(a):
  a = split(a)
  b = [[0,1,2,  3,4,5,  6,7,8], [2,1,0, 5,4,3, 8,7,6], [6,7,8, 3,4,5, 0,1,2], [8,5,2, 7,4,1, 6,3,0], [0,3,6, 1,4,7, 2,5,8], [6,3,0, 7,4,1, 8,5,2], [8,7,6, 5,4,3, 2,1,0], [2,5,8, 1,4,7, 0,3,6]]
  c = [(Grid([a[f] for f in e]), d) for d, e in enumerate(b)]
  if DEBUG:
    print "find max\n\t c: ", c, "\n\t max: ", max(c)
  return max(c)[1] 




# * * * * * * * * * * * * * * *
# * Player Movement Functions *
# * * * * * * * * * * * * * * *

def swapPlayer(n):
  if n == 1:
    return 2
  else: # n == 2:
    return 1

def getMove(n, a):
  b  = 1000
  
  while b not in a.getEmptySpaces():
    if n == 1:
      b = getMoveComputer(a)
      if b not in a.getEmptySpaces():
        print "\n\t b: ", b, " is not in ", a.getEmptySpaces()
        raise ValueError
    else: #n == 2:
      b = getMovePlayer(a)

  return b

def getMovePlayer(a):
  printXO(a)
  b = raw_input("Move? ")[0]
  if b == "h" or b == "H":
    printHelp()
    b = "110"
  b = int(b) - 1
  return b

def getMoveComputer(a):
  # global aidata
  e = findMaxTranslation(a.toString())
  b = translateGrid(a, e)
  if DEBUG:
    print "\n\t a: ", a, "\n\t b: ", b, "\n\t e: ", e, "\n\t translate array: ", translateArray(a), "\n\t convert: ", a.toString(), "\n\t simplify: ", b, "\n\t AI data: ", aidata
  if b in aidata:
    c  = aidata[b]
    d = translateMove(c.index(max(c)), e)
    
    if DEBUG:
      print "AI\n\t C (scores): ", c, "\n\t D (move): ", d, 
      print "\n\t sorted: ", sorted(c), "\n\t first: ", max(c)
  else:
    d = pickOne(a.getEmptySpaces()) 
    if DEBUG:
      print "AI\n\t empty: ", a.getEmptySpaces(), "\n\t move: ", d
  return d
  #return getEmptySpaces(a)[0]

def pickOne(a):
  # Picks one from list. 
  return a[0]


# * * * * * * * * * * * * * * * * *
# * Player Finalization Handlers  *
# * * * * * * * * * * * * * * * * *
def handleGameOver(a, b, c, d):
  if d == 2:
    handleGameOverPlayer(a, d)
  elif d == 1:
    handleGameOverComputer(a, b, c, d)
  else:
    print "Player not 1 or 2", d

def handleGameOverPlayer(a, b):
  if a == b:
    print "You won! computer lost"
  elif a == -1:
    print "You tied!"
  elif a == [2, 1][b - 1]:
    print "You lost, computer won"
  else:
    print "Winner not -1, 1, or 2\n\tWinner: ", winner
    raise IndexError

def handleGameOverComputer(a, b, c, d):
  adjustAI(a,b,c,d)

def adjustAI(a, b, c, j):
  global aidata
  l = {'win': 1, 'lose': -1, 'draw': 0}
  
  self = j
  if a == -1: #draw
    k = l['draw']
  elif a == self: #win
    k = l['win']
  else: #loss
    k = l['lose']
    
  if b != j:
    if DEBUG:
      print "encountered b = ", b, " should be ", j
    c.pop()
  while len(c) > 2:
    d, e, g = c.pop() # AI move
    if g != j:
      d, e, g = c.pop()
    h = findMaxTranslation(d)
    i = translateGrid(d, h)
    if i in aidata:
      f = aidata[i]
    else:
      # Fix this:
      #	Add initial values to Grid?
      f = getInitialValues(d)

    if DEBUG:
      print "f: ", f

    f[e] += k

    aidata[d] = f

    if DEBUG:
      print "AI win\n\t A: ", a, "\n\t B: ", d, "\n\t C: ", c, "\n\t D: ", d, "\n\t E: ", e, "\n\t F: ", f,
      print "\n\t index : ", e, "\n\t score: ", f[e], "\n\t aidata: ", aidata[d]


# * * * * * * * * * * * * * 
# * Statistical Functions * 
# * * * * * * * * * * * * * 

def pushStats(b, a):
  b.reverse()
  b.append(a)
  b.reverse()
  if len(b) > 15:
    b.pop()
  return b

def printStats(a):
  b = a[0]
  c = a[1]
  d = a[2]
  e = a[3]
  f = b + c + d
  print "Success for X\n\twins: ",
  print b, (b * 100.) / f, "%\n\tloses: ", c, (c * 100.) / f, "%\n\tties: ", d, (d * 100.) / f, "%"
  b = e.count(1)
  c = e.count(2)
  d = e.count(-1)
  f = b + c + d
  print "Last 15 games:\n\twins: ", 
  print b, (b * 100.) / f, "%\n\tloses: ", c, (c * 100.) / f, "%\n\tties: ", d, (d * 100.) / f, "%"

def analyzeStats(a, b):
  if a == 1:
    b[0] += 1
  elif a == 2:
    b[1] += 1
  elif a == -1:
    b[2] += 1
  else:
    "Winner not -1, 1, or 2\n\tWinner: ", winner
    raise IndexError
    
  b[3] = pushStats(b[3], a)
  
  
# * * * * * * * * * * * * * *
# * File Control Functions  *
# * * * * * * * * * * * * * *
def load():
  try:
    a = open("data")
    c = pickle.load(a)
    a.close()
  except IOError:
    print "IO Error, line 287"
    c = {}
  return c
  
def dump(a):
  b = open("data", "w")
  pickle.dump(a, b)
  b.close()

# * * * * *
# * Main  *
# * * * * *
  
def play():
  grid = Grid()
  startingplayer = 2
  winner = 0
  gamegrids = []
  global statdata

  player = startingplayer
  while winner == 0:
    move = getMove(player, grid)
    if DEBUG:
      print "move (190): ", move
    gamegrids.append((grid.toString(), move, player))
    grid[move] = player
    player = swapPlayer(player)    
    winner, row = gameOver(grid)
  analyzeStats(winner, statdata)

  printXO(grid)
  for index in range(1,3):
    handleGameOver(winner, startingplayer, gamegrids, index)

def main():
  #a = 'y'
  
  global aidata
  global statdata
  #b = raw_input("Enter name to load previous memory or \"new\" to start a new account: ")
  try:  
    while 1: #a == 'y' or a == 'Y':
      if DEBUG:
        try:
          print "AI data: ", aidata
        except:
          print "locals: ", locals()
      aidata = load()
      play()
      dump(aidata)
      #a = raw_input("Play again? ")[0]
  except (ValueError, IndexError, EOFError):
    if DEBUG:
      print "Caught Error "
  printStats(statdata)
  dump(aidata)

if __name__ == "__main__":
  main()  

  
