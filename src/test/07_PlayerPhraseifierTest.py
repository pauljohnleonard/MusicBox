import sys
import subprocess,time
sys.path.append(sys.path[0] + "/..")

from MB import context,midi,music,players


context=context.Context()
melody_player=context.create_player(chan=1)
echo_player=context.create_player(chan=2)

melody_player.set_instrument('Piano')

accent=music.NoteOn(61,100)
weak=music.NoteOn(60,80)
metro_player=context.create_player(chan=9)
metro=music.Metro(0,4,context.seq,metro_player.inst,accent,weak)

map={"melody":melody_player.play}
        
context.start(map)  

pid=subprocess.Popen([MB.PYTHON_CMD, "pg_ui.py"])



tbreak=0.5

class Client:
    
    
    def notify(self,phrase):
        
        tnow=melody_player.seq.get_real_stamp()
#         tstart=phrase.head.
        player=MB.PhrasePlayer(phrase,echo_player)
        player.start(4)
        print ("Phrase ing ")
        
        
client=Client()

phrasifier=MB.Phrasifier(melody_player.list,melody_player.parser,tbreak,client)


while True:
    tnow=melody_player.seq.get_real_stamp()
    phrasifier.visit(tnow)
    time.sleep(.1)