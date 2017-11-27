__author__ = 'pjl'


from . import config
import numpy



type_spike,type_square=range(2)


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
        self.type=type_spike


    def set_type(self,type):
        self.type=type


    def tick(self):

        for i,div in enumerate(self.divisions):
            if div != 0:

                if self.type == type_spike:
                    self.state[i]=(self.count%div)==0
                else:
                    self.state[i]=(self.count%div)<(div/2)
            else:
                self.state[i]=0

        self.count+=1

    def size(self):
        return len(self.state)
