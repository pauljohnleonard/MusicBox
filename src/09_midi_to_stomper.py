import sys
sys.path.append(sys.path[0] + "/..")
import time

from MB.stomper import Analysis,Stomper 
from MB import midi,setup,stomper_plot
 
#  create PyMidi to initialize misi system.

# Note since midi input runs on 

mid=midi.MidiEngine()

# bpmMax=180
# bpmMin=40

# periodMax=60.0/bpmMin
# periodMin=60.0/bpmMax

# nnMax=int(periodMax/dt)
# nnMin=int(periodMin/dt)



analysis=Analysis(dt=.01,input_window_duration=20,spread=.1,noise_floor=50)
plot = stomper_plot.StomperPlot(analysis)


tref=time.time()

def tNow():
    return time.time()-tref

try:

    midi_in=mid.open_midi_in(setup.MIDI_IN_NAMES)   
      
    # simple handler to pass events to midi_out device
    # define a hander for midi events

    def myhandler(evts):
        val=0
        for evt in evts:
            if evt[0][0] == 144:
                val += evt[0][2]
            
        t = tNow()          
        analysis.stomper.add_event(t,val)


    # register the handler
    mid.set_callback(myhandler) 
    # start deamon
    mid.start()
    
    while(1):

        #    print("-------------")
        t = tNow()          
        periods=analysis.find_periods(t)
        
        for p in periods:
            print(p)
                
        if (len(periods)>0):
          
            plot.update()
            plot.pause(.5)
          
except midi.MidiError:
    print(" MIDI ERROR ")

finally:
    mid.quit()
