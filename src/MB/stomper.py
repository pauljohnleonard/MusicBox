import time
import math
import random
import numpy
import  threading 
from scipy import signal

import sys
sys.path.append(sys.path[0] + "/..")

from MB.circularbuffer import CircularBuffer


class Stomper:

    """
    Kepps a history of events in a quantized circular buffer
    """
    
    def __init__(self,dt,input_window_duration):
        
        assert input_window_duration > dt
        self.events=[]
        self.n=(int)(input_window_duration/dt+1)
        self.buffer=CircularBuffer(self.n)
        self.dt=dt
        self.time=0
        self.lock=threading.Lock()

    def add_event(self,time,val):
        
        # I think midi handler runs on real time thread so better mke sure we don't have concurency problems       
        self.lock.acquire()

        try:
            ptr_next=int(time/self.dt)
            ptr_now=self.buffer.get_count()
            # print ptr_next,ptr_now          
            
            if ptr_now == ptr_next:
                val_old=self.buffer.get_head()
                if (val > val_old):
                    self.buffer.replace(val)
            else:
                while ptr_now < ptr_next: 
                    self.buffer.append(0.0)
                    #print "0:", self.buffer.get_count()
                    ptr_now+=1
                    
                #print "1:", self.buffer.get_count()
                self.buffer.append(val)
        finally:
            self.lock.release()

        

class Analysis:

    def __init__(self,dt,input_window_duration,spread,noise_floor,min_period=0.4,max_period=4):
        self.stomper=Stomper(dt,input_window_duration) 
        self.n=self.stomper.buffer.N
        self.t=numpy.linspace(0, (self.n-1)*dt,num=self.n) 
   
        self.n_spread=round(spread/dt)
        if (self.n_spread %2 == 0):
            self.n_spread += 1
        print(self.n_spread*dt/2)
        self.spread_win=numpy.bartlett(self.n_spread)

        NN=self.n+self.n_spread

        self.t_spread = numpy.linspace(0, (NN-2)*dt,num=NN-1) - dt*(self.n_spread//2) 

        self.noise_level=noise_floor
        self.input_window_duration=input_window_duration
        self.dt=dt
        self.min_period=min_period
        self.max_period=max_period
        self.periods=[]

    def find_periods(self,tnow):
        #print "DOIT",self.stomper.buffer.get_window()

        self.tnow=tnow
        self.stomper.add_event(tnow,0)
        self.input=self.stomper.buffer.get_window()
        
        self.input_spread=numpy.convolve(self.input,self.spread_win,mode="full")

        input_self_correlated=numpy.correlate(self.input_spread, self.input_spread, mode="same")
        
        # print(input_self_correlated.size)
     
        self.correlated=input_self_correlated[(input_self_correlated.size-1)//2:]

        peaks  = self.find_peaks(self.correlated,self.t)
        peaks2 = self.filter_peaks(min_gap=.1,peaks=peaks)


        # self.result=zip(self.times2,self.peaks2)
        periods=[]

        base_period=None
        for pk in peaks2:

            if (pk[0] < self.min_period):
                continue

         
            periods.append(pk)

            if pk[0] > self.input_window_duration / 4 :
                break

        self.periods=numpy.array(periods)
        return self.periods


    def find_average_peak(self,bt,bp):
        # try to return a guess at a peak form a cluster
        # Use a weighted average 
        # sum=0
        # sumt=0
     
        # for p,t in zip(bp,bt):
        #     sum  += p
        #     sumt += p*t
    

        sumt = numpy.sum(bt*bp)
        sum=numpy.sum(bp)

        tav=sumt/sum

        return (tav,sum)
        #self.peaks2.append(sum)
        #self.times2.append(tav)
           
    def filter_peaks(self,min_gap,peaks):   
      
        peaks2 = []

        t1= None
        p1=0
        
        bp=None
        bt=None

        for pp in peaks:
            
            t=pp[0]
            p=pp[1]

            if (t1 is None) or (abs(t - t1) > min_gap):     #  big enough gap 
                if bp != None:   #  send cluster of peaks to the decission maker 
                    ap=self.find_average_peak(numpy.array(bt),numpy.array(bp))
                    peaks2.append(ap)
                bp=[]            #   start new batch
                bt=[]
            t1=t

            bp.append(p)        #  append peak to cluster    
            bt.append(t)

        
        if bp != None:
            ap=self.find_average_peak(numpy.array(bt),numpy.array(bp))
            peaks2.append(ap)

        return numpy.array(peaks2)

    def find_peaks(self,z,t,minI=None,maxI=None):

        #  self.peaks=[]
        #  self.peakst=[]

        peaks=[]
   
        if minI == None:
            minI=1
            
        if maxI == None:
            maxI=len(z)-2
            
        for i in range(minI+1,maxI-1):
            if z[i-1]<=z[i]>=z[i+1] and z[i] > self.noise_level: 
                peaks.append([t[i],z[i]])

        return numpy.array(peaks)



    def find_peaks2(self,z,t,minI=None,maxI=None):

        #  self.peaks=[]
        #  self.peakst=[]

        mean = numpy.mean(z)

        peaks=[]
   
        if minI == None:
            minI=1
            
        if maxI == None:
            maxI=len(t)-2
            
        for zz,tt in zip(z,t):
            if zz > mean : 
                peaks.append([tt,zz])

        return numpy.array(peaks)
        

    def find_phases(self,period):
        n = math.floor(period/self.dt) * 4
        n = min(n,len(self.t)) 
        
        self.phase_cor_t=numpy.linspace(n*self.dt , 0 ,num=n+1)  
        ramp=numpy.linspace(0,(n-1)*self.dt  ,num=n) 
        
        duty= 4*self.n_spread/n

        #  self.triang = 2 * abs( ramp%period - period/2 ) / period
        self.sampler=1.0 +  signal.square(2 * numpy.pi * ramp/period ,duty=duty)
        self.phase_cor = numpy.convolve( self.sampler , self.input_spread[-n*2:] , mode="valid")
    
        p1=self.find_peaks2(self.phase_cor,self.phase_cor_t)

        p2=self.filter_peaks(min_gap=.1,peaks=p1)
     
        
        return p2




if __name__ == "__main__": 
    
    import stomper_plot


   

    NOISE=0.0
    PERIOD=.713
    PROB=1.0
    DT=0.01
    PHASE=.23

    def r():
       return (NOISE*(random.random()-0.5))


    analysis=Analysis(dt=DT,input_window_duration=20.0,spread=.1,noise_floor=0.1)
    plot = stomper_plot.StomperPlot(analysis)
    stomper = analysis.stomper

    for i in range(20):
        tt=PERIOD*(i+1)+r()
        if random.random() < PROB:
            stomper.add_event(tt,1.0)
 
    
    t=time.time()
    tt += PHASE

    periods=analysis.find_periods(tt)
    n=analysis.n
    

    print("ACTUAL PHASE="+str(tt%PERIOD))

    print(" periods ")
    for p in periods:
        print(p)

    if (len(periods)>0):
        phases=analysis.find_phases(PERIOD)
        print(" Phases ")
        for p in phases:
            print(p % PERIOD)
    

    plot.update()

    plot.pause(1000)
    print(time.time()-t)