
from MB import sequencer
import time

def callback():
    print (time.time()-tref)
    

dt=1.0
engine=sequencer.Engine(dt,callback)
tref=time.time()
engine.start()
time.sleep(1000)
