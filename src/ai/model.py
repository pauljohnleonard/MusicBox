__author__ = 'pjl'




import config,rhythm
from MB import MBmusic

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
import interpreter
import random


class Channel:



    def __init__(self,sonify,channel_id,model):

        self.channel_id=channel_id
        self.interpreter=interpreter.Interpretter(sonify,channel_id)
        self.brain=brain.Brain(nin=model.rhythm.size(),output=self.interpreter)

        self.model=model


    def tick(self,pulse):
        """
        Use brain to process the pulse
        :param pulse:
        :return:
        """
        if self.brain.tick(pulse):
            self.interpreter.process(self.brain.out)

    def set_nhid(self,nhid):
        self.nhid=nhid

    def kill_pheno(self,evt):
        pass

    def create_pheno(self,evt):

        self.brain.random_net(self.nhid)
        self.brain.freewheel(16)

    def set_elman_feedback(self,val):
        if self.brain.net:
            self.brain.net.feedback=val



class Model:


    def __init__(self,nChannel=1):

        self.pheno=None


        channel_ids=[0,1,7,5]
        self.divisions=[32,16,8,4]

        if db_loaded:
            self.db=database.DataBase()
        else:
            self.db=None

        self.playing=False

        self.sonify = sonify.Sonify(channel_ids)

        self.rhythm = rhythm.Rhythm(divisions=self.divisions)
        times =   [0.,.25, .5, .75]




       # sequencer will call the rhythm generator tick every dt
        self.seq=MBmusic.SequencerBPM()
        self.set_bpm(config.INIT_BPM)
        self.groover = MBmusic.Groover(0.0,self.seq,times,self,loop=1.0)
        self.channels=[]

        for i in channel_ids:
            chan=Channel(self.sonify,i,self)
            self.channels.append(chan)


        self.seq.start()



    def set_bpm(self,bpm):
        self.bpm=bpm
        self.seq.set_bpm(bpm)




    def play_count(self,count,beat):

        # print "Model Tick"
        self.rhythm.tick()

        for chan in self.channels:
            chan.tick(self.rhythm.state)



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

    def quit(self):
        self.seq.quit()
        self.sonify.quit()