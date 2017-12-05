import sys
sys.path.append(sys.path[0] + "/..")
import time

from MB.stomper import Analysis,Stomper 
from MB import midi,setup 
 
#  create PyMidi to initialize misi system.

# Note since midi input runs on 

mid=midi.MidiEngine()

# bpmMax=180
# bpmMin=40

# periodMax=60.0/bpmMin
# periodMin=60.0/bpmMax

# nnMax=int(periodMax/dt)
# nnMin=int(periodMin/dt)


dt=.01  
T=12.0
analysis=Analysis(dt,T,20)

tref=time.time()

try:

    midi_in=mid.open_midi_in(setup.MIDI_IN_NAMES)   
      
    # simple handler to pass events to midi_out device
    # define a hander for midi events

    def myhandler(evts):
        t = time.time() - tref
        val=0
        for evt in evts:
            if evt[0][0] == 144:
                val += evt[0][2]
        analysis.stomper.add_event(t,val)

    # register the handler
    mid.set_callback(myhandler) 
    # start deamon
    mid.start()
    
    while(1):
        time.sleep(1)
        t = time.time() - tref
        peaks = analysis.doit(t)
        print("-------------")
        for t,p in peaks:
            print(t,p)


except midi.MidiError:
    print(" MIDI ERROR ")

finally:
    mid.quit()
