import pygame
import sys
import time
from threading import Thread
import random
import fontmgr

import  threading

fontMgr = fontmgr.FontManager((('Courier New', 16), (None, 48), (None, 24), ('arial', 24)))


class PygGUI:

    """
    guipy frontend for events.
    delegates the interpretation of events to a user supplied cleint.
    """

    def __init__(self,dim,tmax,ymax):
       # threading.Thread.__init__(self)
        pygame.init()

        self.display = pygame.display.set_mode(dim)
        self.clock=pygame.time.Clock()

        pygame.display.set_caption('Music Box')
        self.running = False

        self.lock=threading.Lock()
        self.fps=10
        self.periodsurf=PeriodSurf(dim,tmax,ymax,(0,0),self.lock)
        self.surfs=[self.periodsurf]


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

            for surf in self.surfs:
                if (surf.dirty):
                    surf.draw()
                    self.display.blit(surf.surf,surf.pos)

            pygame.display.flip()
            self.clock.tick(self.fps)
            self.lock.release()

            #self.process(guipy.event.wait())
        
        
        print("PGDRIVER QUIT")

    def stop(self):
        pygame.event.clear()
        pygame.quit()  # TODO check that midi subsystem is notconfused by this
        print(" STOPPED")



class PeriodSurf:


    def __init__(self,dim,tmax,ymax,pos,lock):

        self.pos=pos
        self.w = dim[0]
        self.h = dim[1]
        self.margin = 20

        self.ybot = self.h - self.margin
        self.xleft = self.margin

        self.ytop = self.margin
        self.xright = self.w - self.margin


        self.xscale=(self.w - 2*self.margin)/tmax
        self.yscale = - (self.h - 2*self.margin)/ymax
        self.xoff = self.margin
        self.yoff = self.h - self.margin
        self.surf = pygame.Surface(dim)
        self.dirty = True
        self.pts = []
        self.lock = lock

    def draw(self):
        
        self.surf.lock()
        self.surf.fill((0,0,0))

        pygame.draw.line(self.surf, (255, 255, 255), (self.xleft, self.ybot), (self.xleft, self.ytop))
        pygame.draw.line(self.surf, (255, 255, 255), (self.xleft, self.ybot), (self.xright, self.ybot))




        for xx,yy in self.pts:
            x=xx*self.xscale+self.xoff
            y=yy*self.yscale+self.yoff

            pygame.draw.line(self.surf, (0, 0, 255), (x, self.yoff), (x, y),2)

        self.surf.unlock()
        x = 0.0

        while (1):
            xscreen = x * self.xscale + self.xoff
            if (x > self.xright):
                break
            text = str(x)
            fontMgr.Draw(self.surf, 'Courier New', 16, text, (xscreen, self.ybot + 2), (20, 255, 255))
            x += 1

        self.dirty = False

    def update(self, x,y):
        self.lock.acquire()
        self.pts=zip(x,y)
        self.dirty = True
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
