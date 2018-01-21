import pygame
import sys
import os
import time
from threading import Thread
import random
#from pygame.locals import *

import  threading 
class PygGUI:

    """
    pygame frontend for events.
    delegates the interpretation of events to a user supplied cleint.
    """

    def __init__(self,dim,tmax,ymax):
       # threading.Thread.__init__(self)
        pygame.init()

        self.w=dim[1]
        self.h=dim[1]
        self.margin=20
        self.display = pygame.display.set_mode(dim)
        self.clock=pygame.time.Clock()
        self.surf = pygame.Surface(dim)
    
        pygame.display.set_caption('Music Box')
        self.running = False
        self.ybase=self.h-self.margin
        self.xscale=(self.w - 2*self.margin)/tmax
        self.yscale = - (self.h - 2*self.margin)/ymax
        self.xoff = self.margin
        self.yoff = self.h - self.margin

        self.lock=threading.Lock()
        self.fps=10
        self.pts=[]

    def process(self, event):

            print("QUITING")
            self.running = False
       
    def run(self):

        print("PGDRIVER RUN")
        self.running = True
        while self.running:
            event=pygame.event.poll()
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                self.running = False
                self.stop()
                return
  
            self.lock.acquire()
            self._draw()    
            self.display.blit(self.surf,(0,0))
            pygame.display.flip()
            pygame.display.flip()
            self.clock.tick(self.fps)
            print("DOING STUFF ")
            self.lock.release()

            #self.process(pygame.event.wait())
        
        
        print("PGDRIVER QUIT")

    def stop(self):
        pygame.event.clear()
        pygame.quit()  # TODO check that midi subsystem is notconfused by this
        print(" STOPPED")



    def _draw(self):
        
        self.surf.lock()
        self.surf.fill((0,0,0))

        for xx,yy in self.pts:
            x=xx*self.xscale+self.xoff
            y=yy*self.yscale+self.yoff
            
            pygame.draw.line(self.surf, (0,0,255), (x,self.yoff), (x,y) )
        self.surf.unlock()
    
    def draw(self,pts):
        self.lock.acquire()
        self.pts = pts
        self.lock.release()


if __name__ == "__main__":

    class Proc(Thread):

        def __init__(self,gui):
            Thread.__init__(self)
            self.running=False
            self.daemon=True
            self.gui=gui
    
        def run(self):

            while(1):
                time.sleep(0.5)
                self.gui.draw([(1,2*random.random()),(2,3*random.random()),(3,1*random.random())])


    gui = PygGUI((600,400),tmax=20,ymax=5)

    proc=Proc(gui)
    proc.start()
    gui.run()

    print("EXITING")
    sys.exit(-1)
    print(" EXITED")
#    pe.stop()
