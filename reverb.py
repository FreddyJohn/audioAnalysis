"""
effects
	reverb
"""

from struct import *
from matplotlib import pyplot as plt
from playsound import playsound
import pcmExplore
import wavExplore


def mix(a, b):
  y=0
  if a<=0 or b<=0:
    y=a+b
  else:
    y=a+b-((a*b)/65536)
  return y

def recursiveSum(sample,previous_sample_list):
  return mix(sample,sum(previous_sample_list))    

def stacker(stack,length,s):
  if len(stack)>length:
    stack.pop()
  else:
    stack.append(s)

path="creation_test.pcm"
file=open(path)
x=0
with open(path,'rb') as file:
	x=bytes(file.read())
	file.close()

dtype=str(len(x)//2)+'h'
bits=[s for s in unpack(dtype,x) if str(s)!='nan']


creation="oneSampleDelay.pcm"
file1=open(creation)
delay_array=[]
with open(creation,'wb') as file1:
  for index, element in enumerate(bits):
    stacker(delay_array,1000,element)   # rolling stack that implements reverb
    print(delay_array)
    s=recursiveSum(element,delay_array)
    if abs(s)<32767:
      buf=pack("h",int(s))
      file1.write(buf)
  file1.close()
	
raw_pcm,pcm_size=pcmExplore.getBytesFromTrack(creation)
wav_track="StarWars60.wav"
raw_wav,wav_size=pcmExplore.getBytesFromTrack(wav_track)

metadata=wavExplore.getWavMetaData(raw_wav)

test='pcmtowav.wav'
wavExplore.doPcmToWavMagic(48000,16,1,test,raw_pcm,metadata)
result=pcmExplore.getBytesFromTrack(test)
wavExplore.getWavMetaData(result[0])

playsound(test)