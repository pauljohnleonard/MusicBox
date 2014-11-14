

import wx
import  gui
 
app = wx.PySimpleApp()
mainFrame = gui.MyFrame(None, title='PYO-GA', pos=(50,50), size=(800,300))
mainFrame.Show()
app.MainLoop()
