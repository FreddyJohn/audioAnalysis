from matplotlib import pyplot as plt
from playsound import playsound
import wavExplore
import numpy as np
from struct import *
import pcmExplore

"""
encoding notes
32 bit has some 4 billion dynamic range in the trailing decimals of -1 to 1. Any two numbers within
this range has the amazing property that when mutliplied the result will always fall within the range
of -1 to 1 this solves many issues that result from mixing 8 and 16 bit signals such as clipping 
and removes the need for normalization

generative synthesis primitives for 8 and 16 bit signals notes
the issues metioned in encoding notes in respect to mixing are extremely important going forward
for example what happens when I try to mix two different waves with amplitudes above the square root of 65,536 ?
this number is 256 dont try to generate signals bigger than than this or you will have to perform
normalization when mixing in order to avoid clipping

pratical implementation of synthesis with non pure carrier signal
tighten the range of your modulation wave with an 
amplitude of -1,1 so that frequency information gets through
without clipping the signal. amplitude in audio directly relates to
volume. for example try to play a sine wave of any frequency with an amplitude
of 100. 


"""
path="creation_test.pcm"
file=open(path)
file_bytes=[]
m=[]
with open(path, 'rb') as file:
  file_bytes=bytes(file.read())
  file.close()

def generateSine(length,sampleRate,frequency,amplitude):
  t = np.linspace(0, length, sampleRate * length)
  y = amplitude*np.sin(frequency * t)
  return y

def generateSinef(length,sampleRate,frequency,amplitude):
  f = np.linspace(0,frequency,sampleRate * length)
  t = np.linspace(0, length, sampleRate * length)
  y=[]
  for i in range(len(t)):
    y.append( amplitude*np.sin(f[i] * t[i]) )
  return y

dtype=str(len(file_bytes)//2)+'h'
m=[s for s in unpack(dtype,file_bytes) if str(s)!='nan']

#y=generateSine(5,44100,440,100)
#y=generateSine(5,44100,4400,100)
lf=generateSinef(50,44100,2000,1)
#lf=generateSine(50,44100,2,1)
#^^source https://issuu.com/petergoldsborough/docs/thesis

test=[]
for i in range(len(m)):
  test.append(m[i]*lf[i])

plt.plot(m)
plt.show()
plt.plot(test)
plt.show()

path="sine.pcm"
file=open(path)
x=[]
with open(path, 'wb') as file:
  for i in test:
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