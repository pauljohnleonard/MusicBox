import sys
import time
import random
sys.path.append(sys.path[0] + "/..")


from MB import pygui
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


analysis=Analysis(dt=.01,input_window_duration=20,spread=0.1,noise_floor=50)



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
 



    class Proc(Thread):

        def __init__(self,gui):
            Thread.__init__(self)
            self.running=False
            self.daemon=True
            self.gui=gui
    
        def run(self):

            while(1):
                t = time.time() - tref          
                periods=analysis.find_periods(t)                    
                tempo.process(periods)

                print("A")
                if len(self.analysis.periods) >0:
                    A=numpy.array(self.analysis.periods)
                    AT=numpy.transpose(A)
                    xx=[analysis.t,AT[0]]
                    yy=[analysis.input,AT[1]]
                    gui.doplot(xx,yy)
                else:
                    xx=[analysis.t,[0]]
                    yy=[analysis.input,[0]]
                    gui.doplot(xx,yy)
            
                print("\n2:",time.time() - t  - tref)
       
                time.sleep(0.5)
                self.gui.draw([(1,2*random.random()),(2,3*random.random()),(3,1*random.random())])


    gui = pygui.PygGUI((600,400),tmax=20,ymax=5)

    proc=Proc(gui)
    proc.start()
    gui.run()


except midi.MidiError:
    print(" MIDI ERROR ")

finally:
    mid.quit()

