'''
 * * * * * * * * * * * *
 * Paul Schwendenman   *
 * 09/28/11            *
 * If you have to ask: *
 * You aren't allowed  *
 * * * * * * * * * * * *
'''


# * * * * * * * * * *
# * Error Catching  *
# * * * * * * * * * *
def handleError():
    '''
    An in-house display for Error Handling.
    '''
    import sys
    import traceback
    stop = 1
    tb = sys.exc_info()[2]
    lines = [(t[1], t[0]) for t in traceback.extract_tb(tb)]
    print "\t", sys.exc_info()[0], sys.exc_info()[1],
    print "\n\t line no: ", lines[-1][0], "\n\t traceback: ", \
        [line[1][:-3] + ":" + str(line[0]) for line in lines]
