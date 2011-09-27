from tictac import *

print "Test translations"

a = [0,1,2,3,4,5,6,7,8]
b = [split(b) for b in translateArray(a)]

def testTranslateArray():
  for c in b:
    printGrid(c)

def testTranslateGrid():
  for c in a[:8]:
    if split(translateGrid(a, c)) == b[c]:
      print "Pass"
    else:
      print "Fail"

def testTranslateMove2():
  for c in a[:8]:
    for d in a[:]:
      if d == translateMove(b[c][d], c):
        print "Pass"
      else:
        print "Fail"
def testTranslateMove():
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
        print "Pass"
      else:
        print "Fail"


