
from MB import music,sequencer
import time
  
if __name__ == "__main__":    
    
        
    seq=sequencer.Sequencer()
        
    
    
    class Factory:
        def create(self,when):
            print (" Factory create",when)
            
    factory=Factory()
    
    mess=music.Repeater(3,2.5,seq,factory.create)
    
    seq.start()
    

time.sleep(1000)
    