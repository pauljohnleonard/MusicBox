# PLug in to send  heart beat events using OSC

# TO test this run test_OSC_server first

import sys
import OSC
import atexit
import numpy
import time
import traceback

class OSCSonify:
    
    def __init__(self,addr):
        
        self.osc_client=OSC.OSCClient()
        
        try:
            self.osc_client.connect(addr)
            
        except:
            print "Failed to connet "
            raise 
            
        self.addr=addr
    
    def message(self,mess,arg=()):
        try:
            msg=OSC.OSCMessage(mess,arg)
            self.osc_client.send(msg)
        except OSC.OSCClientError:
            print "OSClientError  is server ",self.addr," down?"
             
    
    def note_on(self,ii,vel):
        self.message('/noteon',(ii,vel))
    
    def note_off(self,ii):
        self.message('/noteoff',(ii,))
      
        
            
    def quit(self):
        print " OSC sonify QUITTING "
        try:
            msg=OSC.OSCMessage("/quit")
            self.osc_client.send(msg)
        except OSC.OSCClientError:
            e = sys.exc_info()[0]
            print e
            traceback.print_exc()
  
        self.osc_client.close()
 

if __name__  ==  "__main__":
    # define a message-handler function for the server to call.
    import random
    print "HELLO"
    sonify=OSCSonify(addr=("127.0.0.1",9001))
    period=5
    state=0
    t=0
    val=0
    tnow=time.time()    
    tref=tnow   
    tNext=tnow
    
    SLEEP_TIME=1/200.0
    
    tBeat=tnow
    bpm=70
    while(True):
           
    # spin until next tick
    
        while tnow < tNext:
            # yeild to other threads
            time.sleep(0.001) 
            tnow=time.time()       
        tNext += SLEEP_TIME
     
        if tnow >=tBeat:      
                
            sonify.note_on(bpm-50,100)
             # bpm for next interval
            bpm=50+random.random()*20
            delta=60.0/bpm        
            tBeat=tBeat+delta
          
    sonify.quit()
    time.sleep(0.5)
   
