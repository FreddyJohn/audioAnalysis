from struct import *
from matplotlib import pyplot as plt
from playsound import playsound
import numpy as np
import pcmExplore
import wavExplore
import time

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
C=1000

with open(creation,'wb') as file1:
  for i in range(len(x)):
        if x[i]>0 or x[i]<0:
          yn=.1*(x[i]/abs(x[i]))*C*np.floor((abs(x[i])/C)+.5)
          buf=pack("h",int(yn))
          test.append(yn)
          file1.write(buf)
        else:
          buf=pack("h",x[i])
          test.append(x[i])
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
