import sys

import  config
from  MB import MBmidi
from MB import MBmusic



import brain
import atexit
import numpy,math
import time,random
import copy


MIDI_OUT_NAMES=["Qsynth1",
                "FluidSynth virtual port (Qsynth1)",
                "to ARGO Appli Fluidsynth v9 1",
                "Synth input port (Qsynth1:0)",
                "IAC Driver IAC Bus 1"]
         
class Sonify:
    
    
    def __init__(self):
       
        self.tonality=MBmusic.ii
        self.key=MBmusic.D
               
        self.mid=MBmidi.MidiEngine()

        try:
            midi_out=self.mid.open_midi_out(MIDI_OUT_NAMES)
        except:
            self.mid.device_info()
            raise

# bank 0
        self.inst=MBmidi.Instrument(midi_out.out,0)  
        self.inst.set_reverb(70)    
        self.inst.set_volume(127)
        
        atexit.register(self.quit)
        
        
    def toScale(self,i):
       
        """
        i is in range 0 -  nout (from the NN)
        we have to map this onto the sample we want to play
        """
        base=16    #        3 octave   (3*8) 
        ipitch=self.tonality.get_note_of_chordscale(i+base,self.key)
         
        return max(min(config.MAX_PITCH,ipitch),config.MIN_PITCH)
        
    def toScaleDrone(self,i):
        
        i=max(i,0)
        i=i%len(self.scale_drone)
        ipitch=self.scale_root+36+self.scale_drone[i]
        
        return max(min(config.MAX_PITCH,ipitch),config.MIN_PITCH)
   

   
    def note_on(self,ii,vel):
        
        vel=int(math.sqrt(vel)*127)    
        pit=self.toScale(ii)
        self.inst.note_on(pit,vel)
 
    def note_off(self,ii):
        pit=self.toScale(ii)
        self.inst.note_off(pit,100)
        
                    
    def size(self):
        return config.SONIFY_SIZE



    def quit(self):
        self.mid.quit()
