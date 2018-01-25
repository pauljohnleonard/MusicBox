import time

from MB import music,midi
from MB import sequencer
from MB import setup

mid = midi.MidiEngine()
seq = sequencer.Sequencer()
dev = mid.open_midi_out(setup.MIDI_OUT_NAMES)

#  MetroNome
inst = midi.Instrument(dev.out,9)
accent = music.NoteOn(61,100)
weak = music.NoteOn(60,80)
metro = music.Metro(0,4,seq,inst,accent,weak)


seq.start()
time.sleep(100)
    
