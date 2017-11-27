

import wx
import sys
sys.path.append(sys.path[0] + "/..")



from ai import gui,model
 
app = wx.App()
model=model.Model()
mainFrame = gui.MyFrame(model,None, title='PYO-GA', pos=(50,50), size=(800,300))
mainFrame.Show()
app.MainLoop()
