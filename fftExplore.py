from scipy.fft import fft, ifft, fftfreq
from pcmExplore import getBytesFromTrack,getFloatsfromTrack,generateSamplePCM
import matplotlib.pyplot as plt
from struct import *
import numpy as np

#assumes data is stored as 16 bit encoding little endian short
def plotTimeAndFreqDomainOfAudio(sample_rate,file_path):
  raw_bytes=getBytesFromTrack(file_path)[0]
  file=open(file_path)
  l=len(raw_bytes)
  a=0
  b=0
  samples=[]
  for i in range(l):
    b+=2
    try:
      samples.append(unpack('<h',raw_bytes[a:b])[0])
    except error:
      pass
    a+=2
  N=len(samples)
  freq_res=sample_rate/N
  print("amount of samples: ",N)
  print("sample rate: ", sample_rate)
  print("frequency resolution: ",freq_res)
  print("min: ",min(samples))
  print("max: ",max(samples))
  y=fft(samples)
  yinv=ifft(y)
  x=fftfreq(N,1/sample_rate)
  plt.plot(x,np.abs(y))
  plt.show()
  plt.plot(yinv)
  plt.show()


plotTimeAndFreqDomainOfAudio(48000,"creation_test.pcm")
