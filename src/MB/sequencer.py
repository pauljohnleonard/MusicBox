from . import linkedlist
import sys
import time
from threading import Thread

CSI = "\x1B["
RED = '\033[91m'
ENDC = '\033[0m'

SLEEP_TIME = 0.001    # tick to yield in engine event loop

class Engine(Thread):

    """Engine calls a call_back every tick (dt)
       The Engine will attempt to keep the tick synchrounized with
       real time using  a sleep (which will yield. to allow multithreading)
       For usage see Sequencer.
    """

    def __init__(self,dt,call_back=None):
        
        self.dt=dt
        self.call_back=call_back
        self.tclock=0.0
        Thread.__init__(self)
        self.running=False
        self.daemon=True
        
        
    
    
    def run(self):
        self.run2()
        
    def run1(self):
        self.running=True
        
        tnext=tnow=time.time()
        
        while self.running:
            
            # spin until next tick
            
            while tnow < tnext:
                # yeild to other threads
                time.sleep(SLEEP_TIME) 
                tnow=time.time()       
            
            self.call_back()
            
            
            self.tclock+=self.dt
            tnext+=self.dt
    
    
    def run2(self):
        self.running=True
        
        
        self.call_back()
            
        tnow=time.time()
        tnext=tnow+self.dt
        
        while self.running:
            tnow=time.time()
            sleep_time=tnext-tnow
            
            if sleep_time>0:
            # spin until next tick
            # yeild to other threads
                time.sleep(sleep_time)
            else:
                print ('>',)
                   
            self.call_back()
            tnext+=self.dt
            
            
    def stop(self):
        
        print ( "Engine stopping" )
        if not self.running:     # make sure we don't do this twice
            return
        
        self.running=False      # flag deamon to halt.
        self.join()            
        print  ("Engine stopped (threads joined)")




class Sequencer(Engine):
    
    """
    Plays a sequence of messages
    Delegates the timing to an engine which
    must call play_events_at(at) with at incrementing each call
    
    stamp is real time
    """
    
    def __init__(self,dt=0.005):
        """
        Create a Sequencer that services events at a rate of dt
        """     
        self.sequence=linkedlist.OrderedLinkedList()        
        self.sequence.insert(-sys.float_info.max,None,None)
        self.sequence.insert(sys.float_info.max,None,None)
        
        Engine.__init__(self,dt,self._play_next_dt)
        
        # self.prev is last event to be played
        self.prev=self.sequence.head
        self.time=0.0
        self.tstart=time.time()
     
    def schedule(self,at,event):
        """
        add an event to the queue at time = at
        
        """
        
        # time=self.beat_to_time(beat)  
        if at+self.dt < self.time:
            print (RED+"Schedule underrun "+ENDC,at,self.time)
            
        self.sequence.insert(at,event,self.prev)
      
          
    def quit(self):
        """
        Stop the engines. 
        """
        
        self.stop()
        
                    
    def _play_next_dt(self):
        
        """
        advance self.time by self.dt 
        play any pending events up to and including   
        self.time
        """
        
        #print "SEEQ PLAY NEXT"

        self.time+=self.dt
        # if next event is after at just return
        if self.prev.next.time > self.time:
            return
        
        # play pending events   
        while self.prev.next.time <= self.time:
            self.prev=self.prev.next
            # pass the unquantized version of the time to the player.
            # this would allow higher resolution playback if we could be bothered.
            self.prev.data.fire(self.prev.time)
            
    def get_real_stamp(self):
        """
        Get the time using the clock
        """
        return time.time()-self.tstart

    def get_stamp(self):
        """
        Get the stamp according to the schedulers last schedule
        """
        return self.time

class SequencerBPM(Engine):
    
    """
    Plays a sequence of messages
    Delegates the timing to an engine which
    must call play_events_at(at) with at incrementing each call
    
    stamp is the beat 
    """
    
    def __init__(self,beats_per_sec=1.0,dt=0.005):
                
        self.sequence=linkedlist.OrderedLinkedList()        
        self.sequence.insert(-sys.float_info.max,None,None)
        self.sequence.insert(sys.float_info.max,None,None)
        
        Engine.__init__(self,dt,self._play_next_dt)
        
        # self.prev is last event to be played
        self.sequence.head
        self.beats_per_sec=beats_per_sec        
        self.beat=0.0
        self.time=0.0
     
     
    def schedule(self,beat,event):
        # time=self.beat_to_time(beat)  
        self.sequence.insert(beat,event)


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
        advance beat by dt and 
        play any pending events
        """
        
        #print "SEEQ PLAY NEXT"
        self.time+=self.dt
        self.beat+=self.beats_per_sec*self.dt
        # if next event is after at just return
        if self.sequence.head.next.time > self.beat:
            return
        

        next=self.sequence.head.next
        # play pending events   
        while next.time  <= self.beat:        
            next.data.fire(next.time)
            next = next.next  
   

        self.sequence.head.next=next
       

    def get_stamp(self):
        return self.beat
     
     
    def get_real_stamp(self):
        """
        Get the time using the clock (TODO MAKE THIS ACCURATE).
        """
        return self.beat
    
    def set_bpm(self,bpm):
            self.beats_per_sec=bpm/60.0