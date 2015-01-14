__author__ = 'pjl'


import config
import numpy


class Rhythm:

    """
    Called every tick
    Sets state[] according to divisions[]
         That is state[i]  has a period = tick_length *divisions[i]
    """

    def __init__(self,divisions):
        self.divisions=divisions   #  must be reference to allow on the fly control
        self.count=0
        self.state=numpy.zeros(len(divisions),dtype='i')

    def tick(self):

        for i,div in enumerate(self.divisions):
            if div != 0:

                if config.SPIKES:
                    self.state[i]=(self.count%div)==0
                else:
                    self.state[i]=(self.count%div)<(div/2)
            else:
                self.state[i]=0

        self.count+=1

    def size(self):
        return len(self.state)
