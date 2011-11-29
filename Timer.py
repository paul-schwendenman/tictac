class Timer():
    '''
    Basic Class for recording run time.
    '''
    def __init__(self, itter=None):
        '''
        Saves its creation time
        '''
        from time import time
        self.time = time
        self.start = self.time()
        self.itter = itter

    def peek(self):
        '''
        Returns the current duration
        '''
        return self.time() - self.start

    def setItter(self, itter):
        self.itter = itter

    def __del__(self):
        '''
        Prints the lifetime
        '''
        change = self.peek()
        if self.itter:
            prefix, multip = units(change, self.itter)
            print "Took", round(change, 2), "seconds. Per unit:", \
                round(change * multip / self.itter), "%sseconds" % (prefix)
        else:
            print "Took", round(change, 3), "seconds."


def units(time, count):
    '''
    Finds the correct units for a time given a count.
    '''
    from math import log
    n = int((log(count / time) / log(10)) / 3 + 1)
    prefix = {None: 'milli', 0: '', 1: 'milli', 2: 'micro', 3: 'nano', \
              4: 'pico'}
    multip = {None: 1000, 0: 1, 1: 1000, 2: 1000000, 3: 1000000000, \
              4: 1000000000000}
    return (prefix[n], multip[n])
