import random,math
from MB import music as music

class Stub:
    
    
    
    def __init__(self,client):
        
        
        self.time=0.0
        self.dt=0.01
        self.engine=music.Engine(self.dt,self.callback)
        self.bpm_average=60.0
        self.freq=0.1
        self.freq_depth=0.0  
        self.noise_depth=0.0
        self.client=client
        self.engine.start()
        
        
    def quit(self):
        self.engine.stop()
        
        
    def set_client(self,client):
        self.client=client
        
    def noise(self):
        return 2*(0.5-random.random())
    
    def set_bpm(self,bpm):
        self.bpm_average=bpm
        
        
    def set_freq(self,freq):
        self.freq=freq
        
    def set_freq_depth(self,d):
        self.freq_depth=d
        
    def set_noise_depth(self,d):
        self.noise_depth=d
        
        
          
    def callback(self):
        
        if self.client==None:
            return
        
        bpm=self.bpm_average\
        # +self.freq_depth*math.sin(2*math.pi*self.freq*self.time)
        # bpm+=self.noise_depth*self.noise()
        self.client.set_bpm(bpm)