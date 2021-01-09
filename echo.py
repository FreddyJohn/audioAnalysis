from struct import *
from matplotlib import pyplot as plt
from playsound import playsound
#import fftExplore
import pcmExplore
import wavExplore
import sys

"""
when mixing n number of audio tracks normalization via ampiltude modulation is essential to staying within a given data types range.
"""

def mix(a, b):
  y=0
  if a<=0 or b<=0:
    y=a+b
  else:
    y=a+b-((a*b)/65536)
  return y

path="creation_test.pcm"
file=open(path)
x=[]
with open(path, "rb") as file:
  b=bytes(file.read())
  dtype=str(len(b)//2)+'h'
  x=[s for s in unpack(dtype,b) if str(s)!='nan']
plt.plot(x)
plt.show()

creation="oneSampleDelay.pcm"	
file1=open(creation)
test=[]

volume=1.2
num_signals=int(sys.argv[1])
mutliplier=int(sys.argv[2]) # at least 2


with open(creation,'wb') as file1:
  for i in range(len(x)):
      try:
        yn=0

        for signal in range(num_signals):
          yn+=.1*x[i-mutliplier**signal]

      except IndexError:
        yn=.1*x[i]
      test.append(yn)
      buf=pack("h",int(yn))
      file1.write(buf)
  file1.close()

plt.plot(test)
plt.show()

raw_pcm,pcm_size=pcmExplore.getBytesFromTrack(creation)
wav_track="StarWars60.wav"
raw_wav,wav_size=pcmExplore.getBytesFromTrack(wav_track)

metadata=wavExplore.getWavMetaData(raw_wav)

test='pcmtowav.wav'
wavExplore.doPcmToWavMagic(48000,16,1,test,raw_pcm,metadata)
result=pcmExplore.getBytesFromTrack(test)
wavExplore.getWavMetaData(result[0])

playsound(test)
