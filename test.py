from tictac import *

print "Test translations"

a = [0,1,2,3,4,5,6,7,8]
b = [split(b) for b in translateArray(a)]

def testTranslateArray():
  print "Translate Array"
  for c in b:
    printGrid(c)

def testTranslateGrid():
  print "Translate Grid"
  for c in a[:8]:
    if split(translateGrid(a, c)) == b[c]:
      print "\tPass"
    else:
      print "\tFail"

def testTranslateMove2():
  print "Translate Move2"
  for c in a[:8]:
    for d in a[:]:
      if d == translateMove(b[c][d], c):
        print "\tPass"
      else:
        print "\tFail"
def testTranslateMove():
  print "Translate Move"
  c = d = e = f = g = 0

  c = 0
  e = 2
  for c in range(0,8):
    d = split(translateGrid(a, c))

    for e in range(0,9):
      f = d[e]
      #printGrid([str(b) for b in a])
      #printGrid(d)

      #print "\n\t a (list): \t", a, "\n\t c (trans): \t", c, "\n\t d (new grid): \t", d, "\n\t e (move): \t", e, "\n\t f (new move): \t", f, "\n\t g (old move): \t", g
      g = translateMove(f, c)
      #print "\n\t a (list): \t", a, "\n\t c (trans): \t", c, "\n\t d (new grid): \t", d, "\n\t e (move): \t", e, "\n\t f (new move): \t", f, "\n\t g (old move): \t", g
      if e == g:
        print "\tPass"
      else:
        print "\tFail"


print "Test Load, Dump"

def printNine(a):
  print "%2i %2i %2i\n%2i %2i %2i\n%2i %2i %2i\n" % (a[0], a[1], a[2], a[3], a[4], a[5], a[6], a[7], a[8])


def testLoad():
  print "Load"
  a = load()
  for b in a.keys():
    c = Grid([int(d) for d in split(b)])
    printXO(c)
    printNine(a[b])
  print a  
def testDump():
  pass
def testLoadandDump():
  print "Load and Dump"
  a = {'1:0:2:0:2:0:1:0:0': [-2, 1, -2, 0, -2, 0, -2, 0, 0], '1:0:0:0:2:0:0:0:0': [-2, -1, 0, 0, -2, 0, 1, 0, 0], '1:2:0:0:2:0:1:0:0': [-2, -2, -1, 1, -2, 0, -2, 0, 0], '1:0:0:0:2:0:1:2:0': [-2, -2, -1, 1, -2, 0, -2, 0, 0], '1:1:2:0:2:0:0:0:0': [-2, -2, -2, -1, -2, 0, 0, 0, 0], '1:1:2:0:2:0:1:0:2': [-2, -2, -2, 1, -2, 0, -2, 0, -2]}
  dump(a)
  b = load()
  if a == b:
    print "\tPass"
  else:
    print "\tFail"

testLoad()