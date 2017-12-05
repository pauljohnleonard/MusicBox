import sys
import time
sys.path.append(sys.path[0] + "/..")


from MB import music

  
if __name__ == "__main__":    
    
        
    seq=music.Sequencer()
        
    
    
    class Factory:
        def create(self,when):
            print (" Factory create",when)
            
    factory=Factory()
    
    mess=music.Repeater(3,2.5,seq,factory.create)
    
    seq.start()
    

time.sleep(1000)
    