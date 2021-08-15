"""
Parameterized Digital Distortion effect
applied to primitive waveform
"""

from matplotlib import pyplot as plt
from struct import unpack, pack
import numpy as np
import math

sr=48000
l=5
f=4782
p=9.1
a=1
v=5000

filename="digitalDistortion.wav"

# generate waveform
t=np.linspace(0,l,sr*l)
y=np.sin(f*t)

# apply parameterized distortion effect
dd=v*(y/np.abs(y))*(1-np.exp(a*(pow(y,p)/np.abs(y))))

#convert to 16bit
dd=dd.astype(np.short)

#plot and show result
plt.plot(dd)
plt.show()

# write and attach wav file header then play effect
with open("pcm.pcm", 'wb') as f:
  for i in dd:
        f.write(pack('h',i))

  f.close() 

pcm=0
with open("pcm.pcm", 'rb') as f:
  pcm=bytes(f.read())

num_channels=1
samples=len(pcm)
subchunk2size=samples*num_channels*(16//8)+36
byterate=sr*1*(16//8)
blockalign=1*(16//8)

with open(filename,'wb') as f:
  f.write(pack('>I',0x52494646)) #RIFF
  f.write(pack('<i',samples+36))  
  f.write(pack('>I',0x57415645)) #WAVE
  f.write(pack('>I',0x666d7420)) #FMT
  f.write(pack('<L',16))
  f.write(pack('<H',1))  
  f.write(pack('<H',1))    
  f.write(pack('<L',44100))
  f.write(pack('<L',byterate))
  f.write(pack('<H',blockalign))
  f.write(pack('<H',16))
  f.write(pack('>I',0x64617461)) #data
  f.write(pack('<i',samples))
  f.write(pcm)


from playsound import playsound
playsound(filename)
