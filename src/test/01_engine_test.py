import sys
sys.path.append(sys.path[0] + "/..")
from MB import music
import time

def callback():
    print (time.time()-tref)
    

dt=1.0
engine=music.Engine(dt,callback)
tref=time.time()
engine.start()
time.sleep(1000)
