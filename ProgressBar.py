'''
 * * * * * * * * * * * *
 * Paul Schwendenman   *
 * 11/14/11            *
 * If you have to ask: *
 * You aren't allowed  *
 * * * * * * * * * * * *
'''


class ProgressBar:
    '''
    Displays a drop dead simple progressbar
    '''
    def __init__(self, max, topbound=100):
        self.char = '\r'
        self.tail = ''
        self.max = max
        self.topbound = topbound
        self.number = 0
        print
        self.display()

    def setNewline(self):
        '''
        Sets the first character of display to a newline
        '''
        self.char = '\n'
        self.tail = '\n'

    def setCarriageReturn(self):
        '''
        Sets the first character of display to a carriage return
        '''
        self.char = '\r'
        self.tail = ''

    def update(self, current):
        '''
        Advance the position of the counter.
        - reprint the display
        '''
        number = (current * self.topbound) / self.max
        if number != self.number:
            self.number = number
            self.display()

    def clear(self):
        '''
        Set the count to zero.
        '''
        self.update(0)

    def display(self):
        '''
        Print the progressbar
        '''
        print self.char + "[" + "*" * self.number + " " * \
              (self.topbound - self.number) + "] %2i%%" % \
              (self.number * 100 / self.topbound) + self.tail,

    def success(self):
        '''
        Finish at 100%
        '''
        self.number = self.topbound
        self.tail = " " * 20
        self.display()
        print

    def __del__(self):
        '''
        Destructor
        '''
        self.success()


from Timer import Timer, units


class ProgressTimer(ProgressBar, Timer):
    def __init__(self, max, topbound=100, itter=None):
        ProgressBar.__init__(self, max, topbound)
        Timer.__init__(self)
        #self.peek = Timer.peek
        self.update2 = ProgressBar.update

    def update(self, current):
        '''
        Advance the position of the counter.
        - reprint the display
        - print ETA
        '''
        if current != 0:
            time = (self.peek() / current) * (self.max - current)
            if self.max > current:
                self.tail = " ETA: " + eta(time)
            else:
                self.tail = '\t'
        self.update2(self, current)


def eta(time):
    '''
    Finds the estamated time remaining
    - Returns a strind to append to display
    '''
    if int(time / 60) != 0:
        return str(int(time / 60)) + "m " + \
               str(int(time - int(time / 60) * 60)) + "s  "

    else:
        unit = units(time, 1)
        return str(int(time * unit[1])) + " " + unit[0] + "s  "


class ProgressLock(ProgressTimer):
    def update(self, current, lock):
        '''
        Advance the position of the counter.
        - gain and release the lock
        '''
        lock.acquire()
        ProgressTimer.update(self, current)
        lock.release()


class ProgressProcess(ProgressTimer):
    def __init__(self, *args):
        from multiprocessing import Process
        self.Process = Process
        ProgressTimer.__init__(self, *args)

    def update(self, current):
        '''
        Advance the position but in a new process.
        '''
        self.process = self.Process(target=ProgressTimer.update, \
                                    args=[self, current])
        self.process.start()

    def success(self):
        '''
        Join all remaining processes
        '''
        self.process.join()
        ProgressTimer.success(self)


def demo():
    '''
    Runs a basic demo of each progressbar and the timers
    '''
    from Timer import Timer
    from time import sleep

    def run(bar, max):
        for a in range(0, max):
            sleep(.001)
            bar.update(a)

    timer2 = Timer()

    max = 3000

    timer = Timer(max)
    bar = ProgressBar(max, 50)
    run(bar, max)
    del bar
    print
    del timer

    sleep(.125)

    timer = Timer(max)
    bar = ProgressTimer(max, 30)
    run(bar, max)
    del bar
    print
    del timer

    sleep(.125)

    timer = Timer(max)
    bar = ProgressProcess(max, 25)
    run(bar, max)
    bar.success()
    del bar
    print
    del timer
    print


if __name__ == '__main__':
    print "Running demo of three progressbars and two timers:"
    demo()
