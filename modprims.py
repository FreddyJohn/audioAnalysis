from matplotlib import pyplot as plt
from playsound import playsound
import wavExplore
import numpy as np
from struct import *
import pcmExplore

#recall that p and f are different things
# y(x)= 2*a/pi * arcsin(sin(2*pi*x/p))

def generateTriangle(length,sampleRate,a,p):
  x = np.linspace(1, length, sampleRate * length)
  triangle=((2*a)/np.pi)*np.arcsin(np.sin((2*np.pi*x)/p))
  return triangle


def generateSaw(length,sampleRate,a,p):
  x = np.linspace(1, length, sampleRate * length)
  #saw=-((2*a)/np.pi)* np.arctan(1/np.tan((x*np.pi)/p) )
  saw=-((2*a)* np.arctan(np.tan((x*np.pi)/p)**-1 ) )/ np.pi
  return saw

def generateSquare(length,sampleRate,a,f):
  x = np.linspace(1, length, sampleRate * length)
  sqaure = a*np.sign(np.sin(2*np.pi*f*x))
  return sqaure

a=generateSquare(5,44100,100,220)
b=generateSaw(5,44100,100,.01)
c=generateTriangle(5,44100,100,.01)
plt.plot(c)
plt.show()

path="sine.pcm"
file=open(path)
with open(path, 'wb') as file:
  for i in c:
    buf=pack('h',int(i))
    file.write(buf)
  file.close()

pcm_track="sine.pcm"
raw_pcm,pcm_size=pcmExplore.getBytesFromTrack(pcm_track)
wav_track="StarWars60.wav"
raw_wav,wav_size=pcmExplore.getBytesFromTrack(wav_track)

metadata=wavExplore.getWavMetaData(raw_wav)

test='pcmtowav.wav'
wavExplore.doPcmToWavMagic(44100,16,1,test,raw_pcm,metadata)
print("METADATA FROM CONVERSION RESULT:")
result=pcmExplore.getBytesFromTrack(test)[0]
wavExplore.getWavMetaData(result)

playsound('pcmtowav.wav')
