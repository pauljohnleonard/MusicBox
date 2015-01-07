import wx

class MyFrame(wx.Frame):

    def __init__(self,parent):
        wx.Frame.__init__(self, parent, -1, size=(200,200))
       # self.timer = wx.Timer(self)
       # self.Bind(wx.EVT_TIMER, self.on_timer, self.timer)
       # self.timer.Start(750)
        self.sketch = SketchWindow(self, -1)

    def on_timer(self,evt):
        print "Hello"




class SketchWindow(wx.Window):

    def __init__ (self, parent,ID):

        wx.Window.__init__(self, parent, ID)
        self.Buffer = None

        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_ERASE_BACKGROUND, self.OnEraseBack)

    def InitBuffer(self):
        size=self.GetClientSize()
        # if buffer exists and size hasn't changed do nothing

        if self.Buffer:
            print self.Buffer,self.Buffer.GetWidth(),size.width,self.Buffer.GetHeight(),size.height

        if self.Buffer is not None and self.Buffer.GetWidth() == size.width and self.Buffer.GetHeight() == size.height:
            return False

        self.Buffer=wx.EmptyBitmap(size.width,size.height)
        dc=wx.MemoryDC()
        dc.SelectObject(self.Buffer)
        dc.SetBackground(wx.Brush(self.GetBackgroundColour()))
        dc.Clear()
        self.Drawcircle(dc)
        dc.SelectObject(wx.NullBitmap)
        return True

    def Drawcircle(self,dc):
        size=self.GetClientSize()
        pen=wx.Pen('blue',4)
        dc.SetPen(pen)
        dc.DrawCircle(size.width/2,size.height/2,50)

    def OnEraseBack(self, event):
        pass # do nothing to avoid flicker

    def OnPaint(self, event):

        print "Paint"
        if self.InitBuffer():
            self.Refresh() # buffer changed paint in next event, this paint event may be old
          #  return


        print " really  "
        dc = wx.PaintDC(self)
        dc.DrawBitmap(self.Buffer, 0, 0)
        self.Drawcircle(dc)

app = wx.PySimpleApp()
t=MyFrame(None)
t.Show(True)
app.MainLoop()
