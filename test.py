from tictac import *

print "Test translations"

a = [0, 1, 2, 3, 4, 5, 6, 7, 8]
b = translateArray(a)


def testTranslateArray():
    print "Translate Array"
    for c in b:
        #printGrid(c)
        printNine([int(q) for q in c])


def testTranslateGrid():
    print "Translate Grid"
    for c in a[:8]:
        if translateGrid(a, c) == b[c]:
            print "\tPass"
        else:
            print "\tFail"


def testTranslateMove2():
    print "Translate Move 2"
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
    for c in range(0, 8):
        d = translateGrid(a, c)

        printGrid(a)
        printGrid(d)

        for e in range(0, 9):
            f = d[e]

            #print "\n\t a (list): \t", a, "\n\t c (trans): \t", c, \
            #       "\n\t d (new grid): \t", d, "\n\t e (move): \t", \
            #       e, "\n\t f (new move): \t", f, "\n\t g (old move): \t", g
            g = translateMove(f, c)
            #print "\n\t a (list): \t", a, "\n\t c (trans): \t", c, \
            #       "\n\t d (new grid): \t", d, "\n\t e (move): \t", e, \
            #       "\n\t f (new move): \t", f, "\n\t g (old move): \t", g
            print "\n\t e (move): \t", e, "\n\t f (new move): \t", f, \
                  "\n\t g (old move): \t", g
            if e == g:
                print "\tPass"
            else:
                print "\tFail"


def testTranslateMove3():
    print "Translate Move 3"
    for c in range(0, 8):
        print "----------%i-----------" % c
        printNine(a)
        b = translateGrid(a, c)
        b = [int(q) for q in b]
        printNine(b)
        d = [translateMove(z, c) for z in b]
        printNine(d)
        print "----------------------"


def testTranslateMove5():
    print "Translate Move 5"
    for c in range(0, 8):
        print "----------%i-----------" % c
        printNine(a)
        b = translateGrid(a, c)
        #b = [int(q) for q in b]
        printNine(b)
        d = translateGridReverse(b, c)
        printNine(d)
        print "----------------------"


def testTranslateMove4():
    print "Translate Move 4"
    e = [[1, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 1, 0, 0, 0, 2, 2, 0, 0],
         [0, 1, 0, 0, 0, 0, 0, 2, 0],
         [0, 1, 1, 0, 0, 0, 2, 0, 0],
         [0, 0, 0, 1, 0, 0, 0, 0, 0],
         [0, 1, 0, 0, 1, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 1, 0, 0, 0],
         [0, 1, 2, 0, 0, 0, 1, 0, 0],
         [0, 0, 0, 0, 2, 0, 0, 1, 0],
         [0, 1, 0, 0, 0, 0, 2, 0, 1]]
    for f in e:
        print "----------------------"
        printNine(f)
        b, c = translateGridMax(f)
        b = [int(q) for q in b]
        printNine(b)
        d = translateGridReverse(b, c)
        printNine(d)
        b = translateGrid(a, c)
        b = [int(q) for q in b]
        printNine(b)
        print "--------%i-------------" % c


def testGetMove():
    b = Grid([13, -2, 0, 0, 4, -1, -1, -2, 1])
    a = Grid([2, 1, 1, 0, 0, 2, 1, 2, 0])
    aidata = {a: b}

    print "data"
    printGrid(e)
    printGrid(b)
    print "----------\n findings"
    printGrid(a)
    printGrid(f)

print "Test Load, Dump"


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
    a = {'102020100': [-2, 1, -2, 0, -2, 0, -2, 0, 0], \
         '100020000': [-2, -1, 0, 0, -2, 0, 1, 0, 0], \
         '120020100': [-2, -2, -1, 1, -2, 0, -2, 0, 0], \
         '100020120': [-2, -2, -1, 1, -2, 0, -2, 0, 0], \
         '112020000': [-2, -2, -2, -1, -2, 0, 0, 0, 0], \
         '112020102': [-2, -2, -2, 1, -2, 0, -2, 0, -2]}
    dump(a)
    b = load()
    if a == b:
        print "\tPass"
    else:
        print "\tFail"

testTranslateArray()
#testTranslateGrid()
#testTranslateMove2()
#testTranslateMove3()
#testTranslateMove4()
#testTranslateMove()
#testTranslateMove5()
#testLoad()
#testDump()
#testLoadandDump()
#testGetMove()
