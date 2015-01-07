import sys


import MB.music as music
import numpy,random,atexit,copy
import MB.linkedlist as linkedlist
import math
from scipy.special import expit

class Sequencer(music.Engine):
    
    """
    Plays a sequence of messages
    Delegates the timing to an engine which
    must call play_events_at(at) with at incrementing each call
    
    stamp is the beat 
    """
    
    def __init__(self,tick_len,callback,dt=0.005):
                
                
        print "tick_dt",tick_len
        self.sequence=linkedlist.OrderedLinkedList()        
        self.sequence.insert(-sys.float_info.max,None,None)
        self.sequence.insert(sys.float_info.max,None,None)
        
        music.Engine.__init__(self,dt,self._play_next_dt)
        
        # self.prev is last event to be played
        self.prev=self.sequence.head
        self.set_tick_len(tick_len)    
           
        self.tick=0.0
        self.time=0.0
        self.callback=callback
        self.next_tick=0
     
    def set_tick_len(self,tick_len):
        self.ticks_per_sec=1.0/tick_len


    def schedule(self,beat,event):
        # time=self.beat_to_time(beat)  
        self.sequence.insert(beat,event,self.prev)


#        
#    def beat_to_time(self,beat):
#        
#        #  how many beats from the last count
#        ttt=beat-self.beat    
#        
#        tt_time=self.tclock+self.beats_per_sec*ttt
#        return tt_time
#  
      
      
      
    def quit(self):
        """
        Stop the engines. 
        """
        
        self.stop()
        
                    
    def _play_next_dt(self):
        
        """
        advanve beat by dt and 
        play any pending events
        """
        
        #print "SEQ PLAY NEXT"
        self.time+=self.dt
        self.tick+=self.ticks_per_sec*self.dt
        
        
# call the client every tick
        if self.tick >= self.next_tick:
            self.callback()
            self.next_tick += 1
             
        # if next event is after at just return
   
        if self.prev.next.time > self.tick:
            return
        
   
        # play pending events   
        while self.prev.next.time <= self.tick:
            self.prev=self.prev.next
            self.prev.data.fire(self.prev.time)

    def get_stamp(self):
        return self.tick
     
     
    def get_real_stamp(self):
        """
        Get the time using the clock (TODO MAKE THIS ACCURATE).
        """
        return self.tick
    



def sigmoid(x):
    """
    Effecient numpy implementation of sigmoid function
    :param x:
    :return    sigmoid(x):
    """
    return expit(numpy.clip(x,-500,500))
   
class Rythm:

    """
    Called every tick
    Sets state[] according to divisions[]
         That is state[i]  has a period = tick_length *divisions[i]
    """

    def __init__(self,client,divisions):
        self.divisions=divisions   #  must be reference to allow on the fly control
        self.client=client
        self.count=0
        self.state=numpy.zeros(len(divisions),dtype='i')
        
    def tick(self):
        
        for i,div in enumerate(self.divisions):
            if div != 0:
                
                if False:
                    self.state[i]=(self.count%div)==0
                else:
                    self.state[i]=(self.count%div)<(div/2)
            else:
                self.state[i]=0
                
                
        self.client(self.state)
        self.count+=1
        
   
def rand_matrix(nrow,ncol,range=[-1,1]): 
    low=range[0]
    scale=range[1]-range[0]
    return numpy.matrix(low+numpy.random.rand(nrow,ncol)*scale)


class Layer:
    
    def __init__(self,nin,nout,func,matrix=None):
        
        self.nin=nin
        self.nout=nout
        
        if matrix==None:
            self.matrix=rand_matrix(ncol=nin,nrow=nout)
        else:
            self.matrix=numpy.matrix(matrix)
        
        self.func=func
        
        self.input=numpy.zeros(nin)
        self.z=numpy.zeros(nout)
        self.output=numpy.zeros(nout)
    
        
    def fire(self):
        self.z[:]=numpy.dot(self.matrix,self.input)

        self.output[:]=self.func(self.z) 
        return self.output
    
    def radomize(self):
        self.matrix=rand_matrix(ncol=self.nin,nrow=self.nout)
        
        
    
            
class ElmanNet:

    def __init__(self,nin,nhid,nout,noise):
        
        self.nin=nin
        self.nhid=nhid
        self.nout=nout
        self.layer1=Layer(nin+nhid+2,nhid,sigmoid)
        self.layer2=Layer(nhid+2,nout,sigmoid)
        self.noise=noise
    
    def fire(self,input):
        self.layer1.input[:self.nin]=input
        
 #  feed back output of layer1 (which should be stored as input to layer2
        self.layer1.input[self.nin:-2]=self.layer2.input[:self.nhid]
        
        self.layer1.input[-1]=self.noise()
        self.layer1.input[-2]=1.0
        
        self.layer2.input[:-2]=self.layer1.fire()
        
        self.layer2.input[-1]=self.noise()
        self.layer2.input[-2]=1.0
  
        self.layer2.fire()
        return self.layer2.output          
# 

class Brain:
    """
    client is fed the output state every tick
    
    """
    
    def __init__(self,bpm,ticks_per_beat,divisions,nmod,client,nout,nhid):

        
        self.nin=len(divisions)+nmod
        self.nhid=nhid
        self.nout=nout
        self.ticks_per_beat=ticks_per_beat
        self.nrythm=len(divisions)
        
        self.input=numpy.zeros(self.nin)
        self.modulations=numpy.zeros(nmod)    
       
        r=Rythm(self.rythm2net,divisions=divisions)  
        
        dt=self.bpm2dt(bpm)
        
        # sequencer will call the rythm generator tick every dt  
        self.seq=Sequencer(tick_len=dt,callback=r.tick)
        self.client=client
        self.net=None
        self.noise_fact=0.0
        
    def set_nn_noise(self,fact):
        self.noise_fact=fact
        
    def bpm2dt(self,bpm):
        return 60.0/self.ticks_per_beat/bpm
            
    def random_net(self):
        self.net=ElmanNet(self.nin,self.nhid,self.nout,self.noise)
        
        
    def set_bpm(self,bpm):
        dt=self.bpm2dt(bpm)
        self.seq.set_tick_len(dt)
        
            
    def noise(self):
        return random.random()*self.noise_fact
       
    def quit(self):
        self.seq.quit()
        
    def start(self):
        #  start up the sequencer on a seperate thread
        #  TODO  kill this at exit
        self.seq.start()
        
    def rythm2net(self,state):
        
        if self.net == None:
            return
        
        self.input[:self.nrythm]=state
        self.input[self.nrythm:]=self.modulations
        
        out=self.net.fire(self.input)
        
        if self.client != None:
            self.client.process(out)
        else:
            print state,"->",out
            
    def freewheel(self,ncycle):
        
        for _ in range(ncycle):
            out=self.net.fire(self.input)
        
        if self.client != None:
            self.client.process(out,mute=True)
    
        
class Interpretter:
    
    
    def __init__(self,client):
       
        atexit.register(self.quit)
    
        self.last_state=None
        
        self.thresh=0.9
        self.client=client
        
     
    def set_seq_threshold(self,thresh):
        self.thresh=thresh
            
    def process(self,state,mute=False):
        
       # print "process"
        if self.last_state == None:
            self.last_state=copy.deepcopy(state)
            
                  
        cnt=0
        if not mute:
            for s,sl in zip(state,self.last_state):
                
                if s >= self.thresh and sl < self.thresh:
                    self.client.note_on(cnt,s-sl)
                elif s< self.thresh and sl >= self.thresh:
                    self.client.note_off(cnt)
                cnt+=1
                    
        self.last_state[:]=state
                
      
    def quit(self):        
        self.client.quit()
        print " Shutting down interpretter "



    
