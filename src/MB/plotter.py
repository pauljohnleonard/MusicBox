import matplotlib.pyplot as plt
import numpy as np


class Plotter:

    def __init__(self,nx,ny,types,lims):
        plt.ion() 
        fig, ax = plt.subplots(nrows=ny,ncols=nx,sharex=True) 
        if nx*ny> 1:
            self.ax = ax
        else:
            self.ax =[ax]
        self.lines = None
        self.fig=fig
        self.types=types
        self.lims=lims

    def doplot(self,x,y):

        if self.lines is None:
            self.lines=[]

            for xx,yy,axx,t,lim in zip(x,y,self.ax,self.types,self.lims):

                if t == 'stem':
                    markerline, lines, baseline = axx.stem(xx, yy)
                    axx.set_ylim(lim)
        
                else:
                    lines = axx.plot(xx, yy)
                self.lines.append(lines[0])

        else:
            for yy,xx,line,axx,t,lim in zip(y,x,self.lines,self.ax,self.types,self.lims):

                if t == 'stem':
                      axx.cla()
                      markerline, stemlines, baseline = axx.stem(xx, yy)
                      axx.set_ylim(lim)
                else:
                    line.set_ydata(yy)
                    line.set_xdata(xx)



        self.fig.canvas.draw()
        plt.show()

    def pause(self,dur):
        plt.pause(dur)


if __name__ == "__main__":
    import time
    import numpy

    dt=1
    dur=20
    n=dur//dt
    plot = Plotter(1,1,['stem'],[(0,10)])
   
    t=numpy.linspace(0, (n-1)*dt,num=n)

    for i in range(2):
        y1 = t/(i+5)
        y2 = t/(i+10)
        plot.doplot([t],[y1])
        plot.pause(.4)
    
    print ("X")
    plot.pause(1000)
    print ("Y")