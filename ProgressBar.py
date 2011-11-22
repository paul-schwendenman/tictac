class ProgressBar:
    '''
    Displays a drop dead simple progressbar
    '''
    def __init__(self, max, topbound=100):
        self.char = '\r'
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

    def setCarriageReturn(self):
        '''
        Sets the first character of display to a carriage return
        '''
        self.char = '\r'

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
              (self.number * 100 / self.topbound),

    def success(self):
        '''
        Finish at 100%
        '''
        self.number = self.topbound
        self.display()

    def __del__(self):
        '''
        Destructor
        '''
        print
