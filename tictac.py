# * * * * * * * * * * * *  
# * Paul Schwendenman   *
# * 09/20/11            * 
# * If you have to ask: * 
# * All Rights Reserved * 
# * * * * * * * * * * * * 


aidata = {}
# this is a dictionary of numbers that point to a dictionary with choices and success rates
# ex. aidata = {121000000 : ([2,3],[-3,4]} where 2=>-3

def printGrid(a):
  a = convertGridToXO(a)
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
  print " 6 | 7 | 9 "

def convertGridToNumber(a):
  c = 0
  for b in a:  
    c = c * 10
    c = c + b
  return c
  
def convertGridToXO(a):
  b = []
  c = {0: " ",1: "X", 2: "O"}
  for e in a:
    b.append(c[e])
  return b

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

def simplifyGrid(a):
  # should find matching grids
  return a

def swapPlayer(n):
  if n == 1:
    return 2
  else: # n == 2:
    return 1

def getEmptySpaces(a):
  b = []
  for c, d in enumerate(a):
    if d == 0:
      b.append(c)
  return b

def getMove(n, a):
  if n == 1:
    return getMoveComputer(a)
  else: #n == 2:
    return getMovePlayer(a)

def getMoveComputer(a):
  b = convertGridToNumber(a)
  if b in aidata:
    c, d  = aidata[b]
    e = zip(c,d)[sorted(c)[0]]
  else:
    e = pickOne(getEmptySpaces(a)) 
  return e

  #return getEmptySpaces(a)[0]



def pickOne(a):
  # Picks one from list. 
  return a[0]

def getMovePlayer(a):
  printGrid(a)
  b = -1
  while b not in getEmptySpaces(a):
    b = raw_input("Move? ")[0]
    if b == "h" or b == "H":
      printHelp()
      b = "110"
    b = int(b) - 1
  return b

def adjustAI(a, b, c):
  self = 1
  if a == -1: #draw
    pass
  elif a == self: #win
    if b == 2:
      c.pop()
    while len(c) > 2:
      d, e = c.pop() # AI move

      if d in aidata:
        f, g = aidata[d]
      else
        f = getEmptySpaces(d)
        g = [0] * len(f)
      zip(f,g)[e] +=1
      aidata[d] = (f,g)
  else: #loss
    if b == 2:
      c.pop()
    while len(c) > 2:
      d, e = c.pop() # AI move

      if d in aidata:
        f, g = aidata[d]
      else
        f = getEmptySpaces(d)
        g = [0] * len(f)
      zip(f,g)[e] -= 1
      aidata[d] = (f,g)
      
      

      # * * * * * * * * * * * 
      # * Do Something here
      # * * * * * * * * * * *  
      c.pop() # Competitor
        

def play():
  grid = [0,0,0, 0,0,0, 0,0,0,]
  startingplayer = 1
  winner = 0
  gamegrids = []

  printGrid(grid)
  player = startingplayer
  while winner == 0:
    move = getMove(player, grid)
    grid[move] = player
    player = swapPlayer(player)    
    winner, row = gameOver(grid)
    gamegrids.append((convertGridToNumber(grid), move))

  adjustAI(winner, startingplayer, gamegrids)
  printGrid(grid)

play()