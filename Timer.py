class Timer():
    '''
    Basic Class for recording run time.
    '''
    def __init__(self, itter = None):
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

    def __del__(self):
        '''
        Prints the lifetime
        '''
        change = self.peek()
        if self.itter:
            prefix, multip = units(change, self.itter)
            print "Took %d seconds. Per unit: %i %sseconds" % (change, change*multip/self.itter, prefix)
        else:
            print "Took", change, "seconds."


def units(a, b):
    '''
    Doesn't Work... Idea Space Holder
    '''
    from math import log
    n = int((log(b / a) / log(10)) / 3 + 1)
    prefix = {None: 'milli', 0: '', 1: 'milli', 2: 'micro', 3: 'nano', 4: 'pico'}
    multip = {None: 1000, 0: 1, 1: 1000, 2: 1000000, 3: 1000000000, 4: 1000000000000}
    return (prefix[n], multip[n])
