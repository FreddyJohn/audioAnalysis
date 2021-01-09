#future research
#https://www.researchgate.net/publication/228686217_An_automatic_maximum_gain_normalization_technique_with_applications_to_audio_mixing
"""
amplitude modulation is cool because we can peserve a signal that is beyond
the dynamic range of a given data type 16 bit short pcm data for example:

if |x[n]| > 32767

  y[n]=x[n]*(32767/x[n])

"""

from struct import *
from matplotlib import pyplot as plt
from playsound import playsound
#import fftExplore
import pcmExplore
import wavExplore

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

with open(creation,'wb') as file1:
  for i in range(len(x)):
      yn=x[i]*volume
      test.append(yn)
      buf=pack("h",x[i])
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
