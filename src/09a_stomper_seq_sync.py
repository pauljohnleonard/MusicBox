import time
import threading
import random


import numpy
from guipy import pygui
from MB.stomper import Analysis,Stomper
from MB import midi,setup,music,sequencer
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


analysis=Analysis(dt=.01,input_window_duration=20,spread=0.1,noise_floor=0.001,min_period=0.8,max_period=8)



tref=time.time()

def myTime():
    return time.time() - tref

try:

    midi_in=mid.open_midi_in(setup.MIDI_IN_NAMES)   
    
    # simple handler to pass events to midi_out device
    # define a hander for midi events

    def myhandler(evts):
        t = myTime()
        val=0
        # print(evts)
        for evt in evts:
            if evt[0][0] == 144:
                val += (evt[0][2]/127.0)
            
            
        analysis.stomper.add_event(t,val)


    # register the handler
    mid.set_callback(myhandler) 
    # start deamon
    mid.start()
 



    class Proc(threading.Thread):

        def __init__(self,gui):
            threading.Thread.__init__(self)
            self.running=False
            self.daemon=True
            self.gui=gui

        def run(self):

            while(1):
                t = myTime()
                periods=analysis.find_periods(t)
                print("periods :",str(periods))
                # tempo.process(periods)
                # self.gui.updateInput(analysis.t, analysis.input)

                if len(analysis.periods) >0:
                    A=numpy.array(analysis.periods)
                    AT=numpy.transpose(A)
                    self.gui.periodsurf.update(AT[0],AT[1])


                time.sleep(1.0)



    gui = pygui.PygGUI((600,400),tmax=8,ymax=40)

    proc=Proc(gui)
    proc.start()
    gui.run()


except midi.MidiError:
    print(" MIDI ERROR ")

finally:
    mid.quit()

