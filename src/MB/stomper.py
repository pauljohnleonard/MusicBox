import numpy 
import numpy.fft
import time
import math
import random

import sys
sys.path.append(sys.path[0] + "/..")

from MB.circularbuffer import CircularBuffer


class Stomper:

    """
    Kepps a history of events in a quantized circular buffer
    """
    
    def __init__(self,dt,dur):
        
        assert dur > dt
        self.events=[]
        n=(int)(dur/dt+1)
        self.buf=CircularBuffer(n)
        self.dt=dt
        self.time=0
        
    def add_event(self,time,val):
        
        ptr_next=int(time/self.dt)
        ptr_now=self.buf.get_count()
        # print ptr_next,ptr_now          
        
        if ptr_now == ptr_next:
            val_old=self.buf.get_head()
            if (val > val_old):
                self.buf.replace(val)
        else:
            while ptr_now < ptr_next: 
                self.buf.append(0.0)
                #print "0:", self.buf.get_count()
                ptr_now+=1
                
            #print "1:", self.buf.get_count()
            self.buf.append(val)
        
        

class Analysis:
    
    
    def __init__(self,dt,dur,nspread,noise_level):
        self.stomper=Stomper(dt,dur) 
        self.n=self.stomper.buf.N
        self.t=numpy.linspace(0, (self.n-1)*dt,num=self.n) 
        self.win=numpy.bartlett(nspread)
        self.noise_level=noise_level


    def doit(self,t):
        #print "DOIT",self.stomper.buf.get_window()
        self.stomper.add_event(t,0)
        x1=self.stomper.buf.get_window()
        
        self.x=numpy.convolve(x1,self.win,mode="full")
        z1=numpy.correlate(self.x, self.x, mode="full")
        # print(z1.size)
     
        z=z1[(z1.size-1)//2:]
        self.find_peaks(z)
        self.filter_peaks()

        return zip(self.times2,self.peaks2)
      

     
    def add_average_peak(self,bt,bp):
        # try to return a guess at a peak form a cluster
        # Use a weighted average 
        sum=0
        sumt=0
        for p,t in zip(bp,bt):
            sum  += p
            sumt += p*t
    
        tav=sumt/sum
        self.peaks2.append(sum)
        self.times2.append(tav)
           
    def filter_peaks(self):   
        self.peaks2=[]
        self.times2=[]
        
        t1=-100.0
        p1=0
        gap=.1
        
        bp=None
        bt=None

        for p,t in zip(self.peaks,self.peakst):
            if t - t1 > gap:     #  big enough gap 
                if bp != None:   #  send cluster of peaks to the decission maker 
                    self.add_average_peak(bt,bp)
                bp=[]            #   start new batch
                bt=[]
                t1=t

            bp.append(p)        #  append peak to cluster    
            bt.append(t)

        if bp != None:
            self.add_average_peak(bt,bp)

            
    def find_peaks(self,z,minI=None,maxI=None):
        self.peaks=[]
        self.peakst=[]

        if minI == None:
            minI=1
            
        if maxI==None:
            maxI=len(z)-2
            
        for i in range(minI+1,maxI-1):
            if z[i-1]<=z[i]>=z[i+1] and z[i] > self.noise_level: 
                self.peaks.append((z[i]))
                self.peakst.append(self.t[i])
        

   

if __name__ == "__main__": 
    
    def r():
        return 0.1*(random.random()-0.5)

    dt=.01   
    T=20.0

    bpmMax=180
    bpmMin=40

    periodMax=60.0/bpmMin
    periodMin=60.0/bpmMax

    nnMax=int(periodMax/dt)
    nnMin=int(periodMin/dt)

    analysis=Analysis(dt,T,10,0.1)
    stomper = analysis.stomper

    for i in range(100):
        tt=.5*(i+1)+r()
        if random.random() < 0.5:
            stomper.add_event(tt,1.0)
 
    peaks = analysis.doit(tt)
    
   

    tt=None

    for t,p in peaks:
        if tt == None:
            tt=t
        
        xx = t/tt   #  should be integer if perfect data
        
        xi = round(xx)
        
        tt2 = t/xi

        print(t,tt2,p)

        if t > 4 :
            break 

    
    