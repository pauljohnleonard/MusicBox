import wx
import random,math,numpy

class MyFrame(wx.Frame):

    def __init__(self,parent):

        wx.Frame.__init__(self, parent, -1, size=(200,200))
        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.on_timer, self.timer)
        self.timer.Start(20)
        self.nNote=40
        self.x=[0.0]*self.nNote
        self.nSeg=32
        self.segI=0
        self.sketch = SketchWindow(self, -1,self.nSeg,self.nNote)

    def on_timer(self,evt):

        self.x[:]= [random.random() for i in range(self.nNote)]
        self.sketch.draw(self.x,self.segI)
        self.segI=(self.segI+1)%self.nSeg



class SketchWindow(wx.Window):

    def __init__ (self, parent,ID,nx,ny):

        wx.Window.__init__(self, parent, ID)
        self.Buffer = None
        self.Buffer=wx.EmptyBitmap(nx,ny)
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_ERASE_BACKGROUND, self.OnEraseBack)
        self.buf = numpy.empty((ny,nx,4), numpy.uint8)

        self.nx=nx
        self.ny=ny

           # finally, use the array to create a bitmap

    def OnEraseBack(self, event):
        pass # do nothing to avoid flicker


    def draw(self,x,segI):

        size=self.GetClientSize()

        dc=wx.MemoryDC()
        dc.SelectObject(self.Buffer)
        dc.SetBackground(wx.Brush(self.GetBackgroundColour()))

        pen=wx.Pen('blue',4)

        for i in range(len(x)):
            self.buf[i][segI][0]=random.randint(0,255)
            self.buf[i][segI][1]=random.randint(0,255)
            self.buf[i][segI][2]=random.randint(0,255)
            self.buf[i][segI][3]=wx.ALPHA_OPAQUE

        self.Refresh()



    def OnPaint(self, event):
       # print "paint"


        self.bmp = wx.BitmapFromBufferRGBA(self.nx, self.ny, self.buf)

        dc = wx.PaintDC(self)
        dc.SetLogicalScale(1,1)
        dc.DrawBitmap(self.bmp,0,0)


app = wx.App()
t=MyFrame(None)
t.Show(True)
app.MainLoop()
