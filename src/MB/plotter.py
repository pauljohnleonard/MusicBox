import matplotlib.pyplot as plt
import numpy as np


class Plotter:

    def __init__(self,nx=1,ny=1):
        plt.ion() 
        fig, ax = plt.subplots(nrows=ny,ncols=nx,sharex=True) 
        self.ax = ax
        self.line = None
        self.fig=fig
     
        
    def doplot(self,x,y):

        if isinstance(self.ax , (list, tuple, np.ndarray)):
            if self.line is None:
                self.line=[]

                for xx,yy,axx in zip(x,y,self.ax):


                    line, = axx.plot(xx, yy)
                    self.line.append(line)

            else:
                for yy,line in zip(y,self.line):
                    line.set_ydata(yy)

        else:
            if self.line is None:
                self.line, = self.ax.plot(x, y)
            else:
                self.line.set_ydata(y)


        self.fig.canvas.draw()
        plt.show()
        plt.pause(0.005)

    def pause(self,dur):
        plt.pause(dur)


if __name__ == "__main__":
    import time
    import numpy

    dt=.01
    dur=20
    n=dur//dt
    plot = Plotter(1,1)
   
    t=numpy.linspace(0, (n-1)*dt,num=n)
    
    for i in range(1):
       
        y1 = t/(i+5)
        y2 = t/(i+10)
        plot.doplot(t,y1)
  
    plot.pause(10000)
  