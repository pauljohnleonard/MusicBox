"""
DEPreCATED OR FIX ME

"""

from src.MB import context,sequencer,music
from src.util import dlinkedlist


context=context.Context(seqtype=sequencer.SequencerBPM)
context.seq.set_bpm(100)

pl=dlinkedlist.OrderedDLinkedList()


pl.append(0,("1",("1",)))
pl.append(1,("2",("0.8",)))
pl.append(2,("2",("1",)))
pl.append(3,("2",("0.8",)))


phrase=music.Phrase(pl.head,pl.tail)

player=context.create_player(chan=9,pipe_to_beat=False)


context.start(None)
player.play_phrase(pl,2,4)



    


        
    