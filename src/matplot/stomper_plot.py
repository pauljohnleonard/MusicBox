import numpy
import sys
sys.path.append(sys.path[0] + "/..")

from MB import plotter


class StomperPlot:

    def __init__(self,analysis):
        self.plot= plotter.Plotter(ny=2,nx=1,lims=[(),(0,10)],types=('plot','plot'))
        self.analysis=analysis

    def update(self):
        analysis=self.analysis
        
        xx=[analysis.t,analysis.t_spread]
        yy=[analysis.input,analysis.input_spread]

        self.plot.doplot(xx,yy)

    def pause(self,t):
        self.plot.pause(t)


        
class StomperPlotP:

    def __init__(self,analysis):
        self.plot= plotter.Plotter(ny=2,nx=1,lims=[(),(0,10)],types=('plot','plot'))
        self.analysis=analysis

    def update(self):

        analysis=self.analysis
        print("A")
        if len(self.analysis.periods) >0:
            A=numpy.array(self.analysis.periods)
            AT=numpy.transpose(A)
            xx=[analysis.t,AT[0]]
            yy=[analysis.input,AT[1]]
            self.plot.doplot(xx,yy)
        else:
            xx=[analysis.t,[0]]
            yy=[analysis.input,[0]]
            self.plot.doplot(xx,yy)

        print("B")


    def pause(self,t):
        self.plot.pause(t)