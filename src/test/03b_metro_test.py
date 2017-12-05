import sys
import time
sys.path.append(sys.path[0] + "/..")
from MB import music,midi,MB
from MB.players import *

mid = midi.MidiEngine()
seq = music.Sequencer()
dev = mid.open_midi_out(MB.MIDI_OUT_NAMES)

#  MetroNome
inst = midi.Instrument(dev.out,9)
accent = music.NoteOn(61,100)
weak = music.NoteOn(60,80)
metro = music.Metro(0,4,seq,inst,accent,weak)


seq.start()
time.sleep(100)
    
