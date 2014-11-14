# allow GUI to run even if sqlalchemy is absent
try:
    import sqlalchemy
    import database
    db_loaded = True 
except ImportError: 
    print "sqlalchemy  not found. No database capabilities."
    db_loaded = False
        

import sonify
import brain
import stub

import wx
import time

#import threading
import Queue

import wx.lib.scrolledpanel


labelCol=wx.BLUE

def error_message(mess,parent):
    wx.MessageDialog(parent,message=mess, caption="MessageBoxCaptionStr",style=wx.OK).ShowModal()
    
        

class MyFrame(wx.Frame):
   
        
    def __init__(self,parent, title, pos, size=(300, 250)):
        wx.Frame.__init__(self, parent, -1, title, pos, size)
        self.pheno=None
        self.divisions=[32,16,8,4]
        
        self.make_panels()
        if db_loaded:
            self.db=database.DataBase()
        else:
            self.db=None
            
        self.playing=False
      #  self.Bind(wx.EVT_IDLE,self.monit)
        self.editor=None
         
        self.sonify=sonify.Sonify()
        
        self.interpretter=brain.Interpretter(self.sonify)
        
        self.brain=None
        self.stub=stub.Stub(None)
        

        
    def monit(self,evt):
        
        try:
            text=client.q.get(block=False)
            self.console.AppendText(text)
        except Queue.Empty:
            pass    
        
        #self.text=client.stdout.readline()
        #print self.text
            
    
    def make_panels(self):
        
        
        spin=self.make_spin_panel(self)
        
        but=self.make_button_panel(self)
        self.cmdbox = wx.TextCtrl (self, -1, style=wx.TE_PROCESS_ENTER )
        self.console = wx.TextCtrl(self, -1, " server console ", style=wx.TE_MULTILINE)
        
        box = wx.BoxSizer(wx.VERTICAL)
        
        box.Add(spin, 2, wx.EXPAND)
        box.Add(but, 1, wx.EXPAND)
        box.Add(self.cmdbox,0,wx.EXPAND)
        box.Add(self.console,4,wx.EXPAND)
        
        self.cmdbox.Bind(wx.EVT_TEXT_ENTER,self.cmd)
        
        self.SetAutoLayout(True)
        self.SetSizer(box)
        self.Layout()
        
    def cmd(self,ev):
        print " CMD : ",self.cmdbox.GetValue()
        strx=self.cmdbox.GetValue()
        eval(strx)
        self.cmdbox.Clear()
        
    def add_spinner(self,parent,minV,maxV,val,tit):
        """
        Add a spinner returns the ctrl and the panel
        """
        
        panel=wx.Panel(parent,-1,style=wx.SUNKEN_BORDER)
     
        
        box = wx.BoxSizer(wx.VERTICAL)
      
        tit=wx.StaticText(panel, -1, tit)
      
        ctrl=wx.SpinCtrl(panel, -1, '')
        ctrl.SetRange(minV, maxV)
        ctrl.SetValue(val)
        
        box.Add(tit)
        box.Add(ctrl)
        
        panel.SetSizer(box)
        
        
        return ctrl,panel
        
        
        
        
    def  make_spin_panel(self,parent):
        
        panel=wx.Panel(parent,-1, style=wx.SUNKEN_BORDER)
        
        sizer=wx.BoxSizer(wx.HORIZONTAL)
        
        self.bpm,pan=self.add_spinner(panel,40,100,60,"BPM")
        sizer.Add(pan)
        self.bpm.Bind(wx.EVT_SPINCTRL,self.bpm_set)
 
        self.freq,pan=self.add_spinner(panel,50,200,100,"Train Freq mHz")
        self.freq.Bind(wx.EVT_SPINCTRL,self.bpm_set)
        sizer.Add(pan)
 
        self.depth,pan=self.add_spinner(panel,0,10,0,"Train Depth [bpm]")
        self.depth.Bind(wx.EVT_SPINCTRL,self.bpm_set)
        sizer.Add(pan)
 
        self.t_noise,pan=self.add_spinner(panel,0,10,0,"Train Noise [bpm]")
        self.t_noise.Bind(wx.EVT_SPINCTRL,self.bpm_set)
        sizer.Add(pan)
 
        self.div_ctrl=[]
        for div in self.divisions:
            ctrl,pan=self.add_spinner(panel,0,60,div,"DIV")
            ctrl.Bind(wx.EVT_SPINCTRL,self.div_set)
            self.div_ctrl.append(ctrl)
            sizer.Add(pan)
            
       
        self.nn_noise,pan=self.add_spinner(panel,0,100,0,"NN Noise [%]")
        self.nn_noise.Bind(wx.EVT_SPINCTRL,self.brain_set)
        sizer.Add(pan)


        self.seq_thresh,pan=self.add_spinner(panel,0,100,50,"Seq Thresh [%]")
        self.seq_thresh.Bind(wx.EVT_SPINCTRL,self.thresh_set)
        sizer.Add(pan)

   
             
        panel.SetSizer(sizer)
        
        return panel
     
    def div_set(self,evt):
        """
        self.divisions should be referenced by the Rythm gen.
        """
        for i,ctrl in enumerate(self.div_ctrl):
            self.divisions[i]=ctrl.GetValue()
            
    def brain_set(self,evt):
        
        self.brain.set_nn_noise(self.nn_noise.GetValue()/100.0)
    
        
    def thresh_set(self,evt):
        self.interpretter.set_seq_threshold(self.seq_thresh.GetValue()/100.0)
        
        
        
        
        
    def bpm_set(self,evt):
        self.stub.set_bpm(self.bpm.GetValue())
        self.stub.set_freq(self.freq.GetValue()/1000.0)
        self.stub.set_freq_depth(self.depth.GetValue())
        self.stub.set_noise_depth(self.t_noise.GetValue())
        
        self.console.AppendText(" BPM SET"+str(self.stub)+"\n")
                 
    def  make_button_panel(self,parent):
        
        
        panel=wx.Panel(parent,-1, style=wx.SUNKEN_BORDER)
        box = wx.BoxSizer(wx.HORIZONTAL)
        
        
        creat=wx.Button(panel, 1, 'Create')    
        box.Add(creat,1,wx.EXPAND)
        
        kill=wx.Button(panel, 1, 'Kill')    
        box.Add(kill,1,wx.EXPAND)
 
        load=wx.Button(panel, 1, 'Load')    
        box.Add(load,1,wx.EXPAND)
        
        breed=wx.Button(panel, 1, 'Breed')    
        box.Add(breed,1,wx.EXPAND)
        
        save=wx.Button(panel, 1, 'Save')    
        box.Add(save,1,wx.EXPAND)  
        
        quit=wx.Button(panel, 1, 'Quit')    
        box.Add(quit,1,wx.EXPAND)
        
        
        quit.Bind(wx.EVT_BUTTON, self.OnClose)
        kill.Bind(wx.EVT_BUTTON, self.kill_pheno)
        
        creat.Bind(wx.EVT_BUTTON, self.create_pheno)   
        
        breed.Bind(wx.EVT_BUTTON,self.breed_pheno)
        save.Bind(wx.EVT_BUTTON,self.save_pheno)
        load.Bind(wx.EVT_BUTTON,self.load_pheno)
                         
        #panel.SetAutoLayout(True)

        panel.SetSizer(box)
        #panel.Layout()
        return panel
        
        
   
    def OnClose(self,event):
        print "Closing"
        if self.brain != None:
            self.brain.quit()
            
        if self.stub != None:
            self.stub.quit()
            
        time.sleep(.2)
        self.Destroy()

    def kill_pheno(self,evt):
        pass
        
    def create_pheno(self,evt):

        if self.brain == None:
    
                        
            self.brain=brain.Brain(bpm=60,ticks_per_beat=4,divisions=self.divisions,nmod=0,nout=36,nhid=36,client=self.interpretter)
            
            self.brain.start()
            self.stub.set_client(self.brain)
            
        self.brain.random_net()
        self.brain.freewheel(16)
      
 
        
    def load_pheno(self,evt):
        if not db_loaded:
            return
               
        self.kill_pheno()
        self.pheno=self.db.load_random()
        self.build_server_pheno()
        
    def breed_pheno(self,evt):
        self.kill_pheno()
        b=ga.Breeder()
        dad=self.pheno
        mum=self.db.load_random()
        child=b.mate(mum,dad)
        self.pheno=child
        print child
        self.build_server_pheno()
        
    def save_pheno(self,evt):
        self.db.save_nome(self.pheno)
        
    def load_pool(self):
        self.db.load_all_nomes()

 