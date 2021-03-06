import sys
sys.path.append(sys.path[0] + "/..")

from MB import beatclient
from MB.context import Context

import subprocess
import time



class BeatObserver:
    
    def __init__(self,drum_player):
        self.player=drum_player
        
        
    def notify(self):
        pass
        

          
import wx
  
  
class PlayerPanel(wx.Panel):
    
    def __init__(self,parent,player):
        wx.Panel.__init__(self, parent)
        self.player=player
        self.make_panels()
        self.parent=parent
        
    def make_panels(self):
        box=wx.BoxSizer(wx.HORIZONTAL)
        
        name=wx.StaticText(self,-1,self.player.get_name())
        
        
        focusBut=wx.Button(self,1,'FOCUS')
        focusBut.Bind(wx.EVT_BUTTON, self.focus)
        
        learnBut=wx.Button(self,1,'LEARN')
        
        box.Add(name,1)
        box.Add(focusBut,1)
        box.Add(learnBut,1)
        
        self.SetAutoLayout(True)
        self.SetSizer(box)
        self.Layout()
            
    def focus(self,event):
        self.parent.set_focus(self)
        

    def play(self,toks,data): 
        self.player.play(toks,data)
        
        
    
class MyFrame(wx.Frame):
 
        
    def __init__(self,parent, title, pos, size=(300, 250)):
        wx.Frame.__init__(self, parent, -1, title, pos, size)


        context=Context(beat_analysis=True)
        self.context=context
        self.player_panels=[]
        melody_player=context.create_player(chan=0,pipe_to_beat=True)
        
        melody_player.set_instrument('Piano')
        pp=PlayerPanel(self,melody_player)
        self.player_panels.append(pp)
        
        vibe_player=context.create_player(chan=2,pipe_to_beat=False)
        vibe_player.set_instrument('Vibes')
        pp=PlayerPanel(self,vibe_player)
        self.player_panels.append(pp)
        
        drum_player=context.create_player(chan=9,pipe_to_beat=False)
        drum_player.set_instrument("Drum")
        pp=PlayerPanel(self,drum_player)
        self.player_panels.append(pp)
        
      #  self.Bind(wx.EVT_IDLE,self.monit)
        self.make_panels()
        self.timer=wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.update, self.timer)
     
        print("TTT=",self.timer.Start(500))
          
          
        melody_player.set_ghost()  
        drum_player.set_ghost()
        vibe_player.set_ghost()
      
        self.focus=None
        
        # take responsibility for mapping melody event
        map={"melody":self.play}
        
        context.start(map)  
   
      
    
    def set_focus(self,focus):
        self.focus=focus
        
    def play(self,toks,data):
        if self.focus:
            self.focus.play(toks,data)
        
        
        
        
        
    def update(self,evt):
        context=self.context
        beatlen=context.get_beatlength()
        str1="{:5.1f}".format(60.0/beatlen)
        self.bpm_val.SetLabel(str1)
        barlen=context.get_barlength()
        str1="{:5.1f}".format(4*60.0/barlen)
        self.bpm2_val.SetLabel(str1)
 
  #      self.but.after(1000,self.monit)  
    
    def make_panels(self):
        
        context=self.context
        box = wx.BoxSizer(wx.VERTICAL)
        for pp in  self.player_panels:
            box.Add(pp,1,wx.EXPAND)

        pg=wx.Button(self, 1, 'PyGame FrontEnd')
        box.Add(pg,1,wx.EXPAND)   
        pg.Bind(wx.EVT_BUTTON, self.pygame_frontend)
            
        quit=wx.Button(self, 1, 'Quit')    
        box.Add(quit,1,wx.EXPAND)   
        quit.Bind(wx.EVT_BUTTON, self.OnClose)
         
        self.bpm=wx.StaticText(self,-1,"Beats Per Min")
        self.bpm_val=wx.StaticText(self,-1,"???")
        
        self.bpm2=wx.StaticText(self,-1,"Bars Per Min * 4")
        self.bpm2_val=wx.StaticText(self,-1,"???")
        midi_out=wx.StaticText(self,-1,"MidiOut:"+str(context.midi_out_dev.name))
      
        h1=wx.BoxSizer(wx.HORIZONTAL)
        v1 = wx.BoxSizer(wx.VERTICAL)
        v1.Add(self.bpm2, 1, wx.EXPAND)
        v1.Add(self.bpm, 1, wx.EXPAND)
        v1.Add(midi_out, 1, wx.EXPAND)
        h1.Add(v1,1)
         
        v2 = wx.BoxSizer(wx.VERTICAL)
        v2.Add(self.bpm2_val, 1, wx.EXPAND)
        v2.Add(self.bpm_val, 1, wx.EXPAND)
        h1.Add(v2,1)
#         
        box.Add(h1, 1)
#         
        self.SetAutoLayout(True)
        self.SetSizer(box)

        self.Layout()
        
        
    def  make_button_panel(self,parent):
        
        
        panel=wx.Panel(parent,-1, style=wx.SUNKEN_BORDER)
        box = wx.BoxSizer(wx.HORIZONTAL)
        
        panel.SetSizer(box)
        return panel

    def pygame_frontend(self,event):
        self.pid=subprocess.Popen([MB.PYTHON_CMD, "../FrontEnds/pg_ui.py"])
#pid=subprocess.Popen(["ls", "../FrontEnds"])

        
   
    def OnClose(self,event):
        print( "CLosing" )
        if self.pid != None:
            self.pid.terminate()
        
        self.err_t = None
        self.context.quit()
       
        # wait for the pipes to flush
        time.sleep(.2)
        self.Destroy()
        print ("OnClose End")
     



app = wx.PySimpleApp()
mainFrame = MyFrame(None, title='PYO-GA', pos=(50,50), size=(800,300))
mainFrame.Show()
app.MainLoop()

print (" EXIT?")
  

