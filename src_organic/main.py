__author__ = 'pjl'



import pyo

s = pyo.Server(sr=44100, nchnls=2, buffersize=256, duplex=1, audio='portaudio', jackname='pyo')

s.boot()
s.start()

fund = 100.

noise = pyo.Sine(freq=1)

noise.ctrl( [pyo.SLMap(0, 5, "lin", "freq", 0),pyo.SLMap(0, 5, "lin", "mul", 0)])

freq = fund+noise

blit1 = pyo.Blit(freq=freq, harms=40, mul=1, add=0)

blit1.out()


s.gui('locals()')