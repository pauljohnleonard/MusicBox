
import sys
sys.path.append('../MB')

import music
import midi 
import setup
import oscserver
import math

try:
    mid = midi.MidiEngine()
    
    midi_out_dev = mid.open_midi_out(setup.MIDI_OUT_NAMES)
    
    
    seq = music.SequencerBPM(beats_per_sec=2)
    
    # Score
    beats_per_bar=4
    bars_per_section=1
    key=music.G
    start=0
    
    score = music.Score(bars_per_section,beats_per_bar,key)
    score.set_tonality(music.I, 0)
    

    # MetroNome
    accent = music.NoteOn(61, 100)
    weak = music.NoteOn(60, 80)
    metro_inst = midi_out_dev.allocate_channel(9)
    
    #metro = music.Metro(0, 4,seq, metro_inst, accent, weak) 
    
    # bass line

    
    class BassData:
        
        def __init__(self):
            self.times =   [0.0,  1.0, 2.0, 3.0]
            self.vels =    [100,  70,  90,  70]                 
            self.durs =    [0.6, 0.4, 0.4 , 0.4]
            self.pattern=  [0,   2,  4,  2]


    bass_inst = midi_out_dev.allocate_channel(1)  
    bass_player = music.BassPlayer(seq, bass_inst, score,30,48)
    bass_data=BassData()
    bass_factory=music.GrooverFactory(seq,bass_data,bass_player)
    music.Repeater(0, 4, seq, bass_factory.create) 
    
    # Vamp
       
    vamp_inst = midi_out_dev.allocate_channel(0)
    vamp = music.ChordPlayer(seq, vamp_inst, score, 50,[0,1,2,3])

    class VampData:
        
        def __init__(self):
            self.times = [0.5, 1.5, 2.0]
            self.vels =  [80,  70,  70]                 
            self.durs =  [0.6, 0.4, 0.4]
       
            
   
    vamp_data=VampData()
    factory=music.GrooverFactory(seq,vamp_data,vamp)   
    music.Repeater(0, 4, seq, factory.create) 
    
    solo_inst=midi_out_dev.allocate_channel(2)
    
    # ready to go
    
    seq.start()

    import mapper      
    mapper=mapper.Mapper(seq,score,vamp_inst,bass_inst)
    
    addr=setup.get_osc_ip()
    drv=oscserver.Server(addr,mapper.map)
    drv.run()
    
    xx=raw_input(" enter to quit ")
    
    seq.quit()
    mid.quit()
    
    
except:
    import traceback
    traceback.print_exc()  
 
