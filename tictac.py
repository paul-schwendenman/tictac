# * * * * * * * * * * * *  
# * Paul Schwendenman   *
# * 09/20/11            * 
# * If you have to ask: * 
# * You aren't allowed  * 
# * * * * * * * * * * * * 

import pickle

aidata = {}
# this is a dictionary of numbers that point to a dictionary with choices and success rates
# ex. aidata = {121000000 : [2,3,2, 3,4,4, 1,-3,4]} where [2]=3

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
  print " 7 | 8 | 9 "

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

def getUsedSpaces(a):
  b = []
  for c, d in enumerate(a):
    if d != 0:
      b.append(c)
  return b

def getInitialValues(a):
  b = []
  for c in a:
    if c != 0:
      b.append(-2)
    else:
      b.append(0)
  return b

def getMove(n, a):
  b  = 1000
  
  while b not in getEmptySpaces(a):
    if n == 1:
      b = getMoveComputer(a)
      if b not in getEmptySpaces(a):
        print "\n\t b: ", b, " is not in ", getEmptySpaces(a)
        raise ValueError
    else: #n == 2:
      b = getMovePlayer(a)

  return b

def getMovePlayer(a):
  printGrid(a)
  b = raw_input("Move? ")[0]
  if b == "h" or b == "H":
    printHelp()
    b = "110"
  b = int(b) - 1
  return b

def getMoveComputer(a):
  b = simplifyGrid(convertGridToNumber(a))
  print "\n\t a: ", a, "\n\t b: ", b, "\n\t convert: ", convertGridToNumber(a), "\n\t simplify: ", simplifyGrid(convertGridToNumber(a)), "\n\t AI data: ", aidata
  if b in aidata:
    c  = aidata[b]
    d = c.index(max(c))

    print "AI\n\t C (scores): ", c, "\n\t D (move): ", d, 
    print "\n\t sorted: ", sorted(c), "\n\t first: ", max(c)
  else:
    d = pickOne(getEmptySpaces(a)) 
    print "AI\n\t empty: ", getEmptySpaces(a), "\n\t move: ", d
  return d
  #return getEmptySpaces(a)[0]

def pickOne(a):
  # Picks one from list. 
  return a[0]

def adjustAI(a, b, c):
  self = 1
  if a == -1: #draw
    pass
  elif a == self: #win
    if b == 2:
      c.pop()
    while len(c) > 2:
      d, e, g = c.pop() # AI move
      if g == 2:
        d, e, g = c.pop()
      d = simplifyGrid(d)
      if d in aidata:
        f = aidata[d]
      else:
        f = getInitialValues(convertNumberToGrid(d))

      print "f: ", f

      f[e] += 1

      aidata[d] = f

      print "AI win\n\t A: ", a, "\n\t B: ", d, "\n\t C: ", c, "\n\t D: ", d, "\n\t E: ", e, "\n\t F: ", f,
      print "\n\t index : ", e, "\n\t score: ", f[e], "\n\t aidata: ", aidata[d]

  else: #loss
    if b == 2:
      c.pop()
    while len(c) > 2:
      d, e, g = c.pop() # AI move
      if g == 2:
        d, e, g = c.pop()

      d = simplifyGrid(d)
      if d in aidata:
        f = aidata[d]
      else:
        f = getInitialValues(convertNumberToGrid(d)) 

      print "f: ", f

      f[e] -= 1

      aidata[d] = f

      aidata[d] = f
      print "AI win\n\t A: ", a, "\n\t B: ", d, "\n\t C: ", c, "\n\t D: ", d, "\n\t E: ", e, "\n\t F: ", f,
      print "\n\t index : ", e, "\n\t score: ", f[e], "\n\t aidata: ", aidata[d]

        
def load():
  a = open("data")
  c = pickle.load(a)
  a.close()
  return c
  
def dump(a):
  b = open("data", "w")
  pickle.dump(a, b)
  b.close()
  
def play():
  grid = [0,0,0, 0,0,0, 0,0,0,]
  startingplayer = 1
  winner = 0
  gamegrids = []

  printGrid(grid)
  player = startingplayer
  while winner == 0:
    move = getMove(player, grid)
    print "move (190): ", move
    gamegrids.append((convertGridToNumber(grid), move, player))
    grid[move] = player
    player = swapPlayer(player)    
    winner, row = gameOver(grid)

  if winner == 1:
    print "You lost, computer won"
  elif winner == 2:
    print "You won! computer lost"
  elif winner == -1:
    print "You tied!"
  else:
    raise IndexError
  
  adjustAI(winner, startingplayer, gamegrids)
  printGrid(grid)

def main():
  a = 'y'
  while a == 'y' or a == 'Y':
    print "AI data: ", aidata
    aidata = load()
    play()
    dump(aidata)
    a = raw_input("Play again? ")[0]
main()  
