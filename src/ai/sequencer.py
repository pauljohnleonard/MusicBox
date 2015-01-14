__author__ = 'pjl'


from MB import MBmusic as music
from MB import linkedlist


import sys

class Sequencer(music.Engine):

    """
    Plays a sequence of messages
    Delegates the timing to an engine which
    must call play_events_at(at) with at incrementing each call

    stamp is the beat
    """

    def __init__(self,tick_len=1,callback=None,dt=0.005):


        print "tick_dt",tick_len
        self.sequence=linkedlist.OrderedLinkedList()
        self.sequence.insert(-sys.float_info.max,None,None)
        self.sequence.insert(sys.float_info.max,None,None)

        music.Engine.__init__(self,dt,self._play_next_dt)

        # self.prev is last event to be played
        self.prev=self.sequence.head
        self.set_tick_len(tick_len)

        self.tick=0.0
        self.time=0.0
        self.callback=callback
        self.next_tick=0

    def set_tick_len(self,tick_len):
        self.ticks_per_sec=1.0/tick_len


    def schedule(self,beat,event):
        # time=self.beat_to_time(beat)
        self.sequence.insert(beat,event,self.prev)


#
#    def beat_to_time(self,beat):
#
#        #  how many beats from the last count
#        ttt=beat-self.beat
#
#        tt_time=self.tclock+self.beats_per_sec*ttt
#        return tt_time
#



    def quit(self):
        """
        Stop the engines.
        """

        self.stop()


    def _play_next_dt(self):

        """
        advanve beat by dt and
        play any pending events
        """

        #print "SEQ PLAY NEXT"
        self.time+=self.dt
        self.tick+=self.ticks_per_sec*self.dt


# call the client every tick
        if self.tick >= self.next_tick:
            self.callback()
            self.next_tick += 1

        # if next event is after at just return

        if self.prev.next.time > self.tick:
            return


        # play pending events
        while self.prev.next.time <= self.tick:
            self.prev=self.prev.next
            self.prev.data.fire(self.prev.time)

    def get_stamp(self):
        return self.tick


    def get_real_stamp(self):
        """
        Get the time using the clock (TODO MAKE THIS ACCURATE).
        """
        return self.tick