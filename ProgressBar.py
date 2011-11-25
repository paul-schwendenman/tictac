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

    def __del__(self):
        '''
        Destructor
        '''
        print

from Timer import Timer, units
class ProgressTimer(ProgressBar, Timer):
    def __init__(self, max, topbound=100, itter=None):
        ProgressBar.__init__(self, max, topbound)
        Timer.__init__(self)
        #self.peek = Timer.peek
        self.update2 = ProgressBar.update
        
        
    def update(self, current):
        if current != 0:
            time = (self.peek() / current) * (self.max - current) 
            unit = units(time, 1)
            self.tail = " ETA: " + str(int(time*unit[1])) + " " + unit[0] + "s  "
        self.update2(self, current)
