import numpy

import sys
sys.path.append(sys.path[0] + "/..")

from MB.filters import Median

class TempoDecider:


    def __init__(self,min_period,max_period,seq,thresh):
        self.min_period=min_period
        self.max_period=max_period
        self.period  = 1
        self.std = 1.0
        self.filter = Median(5)
        self.seq=seq
        self.thresh=thresh
        

    def process(self,periods):

        if len(periods) == 0:
            return

        for p in periods:

            if p[0] < self.min_period :
                continue

            if p[0] > self.max_period :
                break

            self.filter.process(p[0])    
            print( self.filter.x )
            self.std = numpy.std(self.filter.x)
            self.period = self.filter.median_val()
            if self.period == 0: 
                continue
            print(" BPM :" + str(60.0/self.period) + " std:"+ str(self.std))
            if self.std < self.thresh:
                self.seq.set_bpm(60.0/self.period)


