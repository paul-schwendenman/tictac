
def printGrid(a):
  a = convertGrid(a)
  print
  print " %c | %c | %c " % (a[0], a[1], a[2])
  print "---+---+---"
  print " %c | %c | %c " % (a[3], a[4], a[5])
  print "---+---+---"
  print " %c | %c | %c " % (a[6], a[7], a[8])
  
def convertGrid(a):
  b = []
  c = {0: " ",1: "X", 2: "O"}
  for e in a:
    b.append(c[e])
  return b
def gameOver(a):
  if a[0] == a[1] == a[2] and a[0] != 0:
    return 1
  elif a[3] == a[4] == a[5] and a[3] != 0:
    return 2
  elif a[6] == a[7] == a[8] and a[6] != 0:
    return 3

  elif a[0] == a[3] == a[6] and a[0] != 0:
    return 4
  elif a[1] == a[4] == a[7] and a[1] != 0:
    return 5
  elif a[2] == a[5] == a[8] and a[2] != 0:
    return 6

  elif a[0] == a[4] == a[8] and a[0] != 0:
    return 7
  elif a[6] == a[4] == a[2] and a[2] != 0:
    return 8
  else:
    return 0

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
  b = getEmptySpaces(a)[0]
  return b

  #return getEmptySpaces(a)[0]

def getMovePlayer(a):
  printGrid(a)
  b = -1
  while b not in getEmptySpaces(a):
    b = int(raw_input("Move? ")[0])
  return b


def play():
  grid = [0,0,0, 0,0,0, 0,0,0,]
  startingplayer = 1
  winner = 0

  printGrid(grid)
  player = startingplayer
  while winner == 0:
    grid[getMove(player, grid)] = player
    player = swapPlayer(player)    
    winner = gameOver(grid)
    
  printGrid(grid)

play()