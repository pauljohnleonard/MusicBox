import sys
import time
sys.path.append(sys.path[0] + "/..")

from MB import music


    
seq=music.SequencerBPM()
    

class Player:
    
    def play_count(self,count,beat):
        print (count,seq.beat,beat)
 

times =   [0.3,  1.0, 2.0, 3.0]
     
player=Player()
when=0.0

groover=music.Groover(when,seq,times,player,loop=4)




seq.start()

import time
time.sleep(10)
    


        
    