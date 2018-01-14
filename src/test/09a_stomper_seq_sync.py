import sys
sys.path.append(sys.path[0] + "/..")
import time
import random

from MB.stomper import Analysis,Stomper
from MB import midi,setup,music,sequencer
from MB import stomper_plot
from MB import tempo_decider

mid = midi.MidiEngine()
seq = sequencer.SequencerBPM()
dev = mid.open_midi_out(setup.MIDI_OUT_NAMES)
tempo = tempo_decider.TempoDecider(0.5,2,seq,0.1)

#  MetroNome
inst = midi.Instrument(dev.out,9)
accent = music.NoteOn(61,100)
weak = music.NoteOn(60,80)
metro = music.Metro(0,4,seq,inst,accent,weak)


seq.start()



analysis=Analysis(dt=.01,input_window_duration=20,spread=0.1,noise_floor=50)
plot = stomper_plot.StomperPlotP(analysis)
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
        t = time.time() - tref          
        periods=analysis.find_periods(t)            
        tempo.process(periods)
        print("\n1:",time.time() - t  - tref)
        plot.update()
        print("\n2:",time.time() - t  - tref)
        plot.pause(10)
       # time.sleep(.5)
 

except midi.MidiError:
    print(" MIDI ERROR ")

finally:
    mid.quit()

