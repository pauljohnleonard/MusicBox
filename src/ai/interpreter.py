__author__ = 'pjl'

import atexit,copy


class Interpretter:


    def __init__(self,sonify,chan):

        atexit.register(self.quit)

        self.last_state=None

        self.thresh=0.9
        self.sonify=sonify
        self.chan=chan


    def set_seq_threshold(self,thresh):
        self.thresh=thresh

    def process(self,state,mute=False):

        # print "process"
        if self.last_state == None:
            self.last_state=copy.deepcopy(state)


        cnt=0
        chan=self.chan
        if not mute:
            for s,sl in zip(state,self.last_state):

                if s >= self.thresh and sl < self.thresh:
                    self.sonify.note_on(chan,cnt,s-sl)
                elif s< self.thresh and sl >= self.thresh:
                    self.sonify.note_off(chan,cnt)
                cnt+=1

        self.last_state[:]=state


    def quit(self):
        self.sonify.quit()
        print " Shutting down interpretter "


    def size(self):
        return self.sonify.size()