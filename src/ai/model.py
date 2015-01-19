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

class Model:


    def __init__(self):

        self.pheno=None



        self.divisions=[32,16,8,4]

        if db_loaded:
            self.db=database.DataBase()
        else:
            self.db=None

        self.playing=False

        self.sonify = sonify.Sonify()

        self.interpreter=interpreter.Interpretter(self.sonify)

        self.rhythm = rhythm.Rhythm(divisions=self.divisions)


            # sequencer will call the rhythm generator tick every dt
        self.seq=MBmusic.SequencerBPM()
        self.brain=brain.Brain(nin=self.rhythm.size(),output=self.interpreter)

        self.set_bpm(config.INIT_BPM)
        times =   [0.,.25, .5, .75]


        groover = MBmusic.Groover(0.0,self.seq,times,self,loop=1.0)

        self.seq.start()


    def set_nhid(self,nhid):
        self.nhid=nhid


    def kill_pheno(self,evt):
        pass


    def set_bpm(self,bpm):
        self.bpm=bpm
        self.seq.set_bpm(bpm)

    def play_count(self,count,beat):
        self.tick()

    def tick(self):
        # print "Model Tick"
        self.rhythm.tick()
        self.brain.tick(self.rhythm.state)

    def create_pheno(self,evt):

        self.brain.random_net(self.nhid)
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

    def quit(self):
        self.seq.quit()
        self.sonify.quit()