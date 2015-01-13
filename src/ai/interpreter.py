__author__ = 'pjl'

import atexit,copy


class Interpretter:


    def __init__(self,client):

        atexit.register(self.quit)

        self.last_state=None

        self.thresh=0.9
        self.client=client


    def set_seq_threshold(self,thresh):
        self.thresh=thresh

    def process(self,state,mute=False):

       # print "process"
        if self.last_state == None:
            self.last_state=copy.deepcopy(state)


        cnt=0
        if not mute:
            for s,sl in zip(state,self.last_state):

                if s >= self.thresh and sl < self.thresh:
                    self.client.note_on(cnt,s-sl)
                elif s< self.thresh and sl >= self.thresh:
                    self.client.note_off(cnt)
                cnt+=1

        self.last_state[:]=state


    def quit(self):
        self.client.quit()
        print " Shutting down interpretter "


    def size(self):
        return self.client.size()