import matplotlib.pyplot as plt
import numpy as np
import sys
from struct import *
import math

#recorded min -3.309757629918933e+38
#MIN -3.574048043601211e+30
#MAX: 3.574048043601211e+30
# (a+b)-(a*b)/min if a < 0 and b < 0
# (a+b)-(a*b)/max if a > 0 and b > 0
# a + b
def mixEquation2(a,b):
  if a<0 and b<0:
    return (a+b)-((a*b)/np.iinfo(np.int16).min)
  elif a>0 and b>0:
    return (a+b)-((a*b)/np.iinfo(np.int16).max)
  else:
    return a+b

def mixEquation3(a,b):
  maximum=3.574048043601211e+30
  minimum=-3.574048043601211e+30
  a+=maximum
  b+=maximum
  if a<maximum and b<maximum:
    return (a+b)/maximum
  else:
    return 2*(a+b)-(a*b)/maximum
  if m==maximum*2:
    return minimum

#frames/rate = time
def getTrackTime(frames,rate):
  return frames/rate

def mixEquation1(x,y,q):
  norm=((x*y)/32768)-65536
  func=2*(x+y)-norm
  #func = x+y-((x*y)/256)
  z=round(func,q)
  if z!=65536.0:
    return z
  if z == 65536.0:
    return z

def getMinMaxFromTwoSamples(x,y):
  x.extend(y)
  a=min(x)
  b=max(x)
  return a,b

def arangeLargestSmallest(x,y):
  a=len(x)
  b=len(y)
  if a>=b:
    return x,y
  if a<=b:
    return y,x

def mixEquation(x1,x2,a1,a2):
  #norm=(x*y)/65536
  #func=x+y-norm
  func = x1*a1+x2*a2
  return func
  """
  if x<0 and y>0:
    func = x-y
    return round(func,q)
  if y<0 and x>0:
    func = y-x
    return round(func,q)
  else:
    func = x-y
    return round(func,q)
  """

def getFloatsfromTrack(track,nan=False):
  floats=[]
  file = open(track)
  raw_bytes,size=getBytesFromTrack(track)
  if nan is False:
    floats=[b for b in unpack(size,raw_bytes) if str(b)!='nan']
    return floats
  elif nan is True:
    floats=[b for b in unpack(size,raw_bytes)]
    return floats

def getBytesFromTrack(track):
  raw_bytes=0
  file = open(track)
  with open(track, 'rb') as file:
   raw_bytes=bytes(file.read())
  size=str(len(raw_bytes)//4)+'f'
  return raw_bytes,size

#this function takes n plots to make 4 subplots for each n
def doRecursivePlot(plots,size,Fs):
  diems=(4,len(plots))
  fig, axes = plt.subplots(nrows=diems[0],
                           ncols=diems[1],
                           figsize=size)
  y=0
  for p in plots:
    sample=plots[p]
    for x in range(diems[0]):
      print(x,y)
      if x==0:
        axes[x,y].magnitude_spectrum(sample, Fs=Fs, scale='dB', color='C1')
      if x==1:
        axes[x,y].magnitude_spectrum(sample, Fs=Fs, color='C2')
      if x==2:
        axes[x,y].angle_spectrum(sample, Fs=Fs, color='C3')
      if x==3:
        axes[x,y].plot(sample)
    y+=1
  plt.show()

#there is 0 information loss from float > byte > float
def doConversionLossTest(filepath,testpath,orignal):
  test = open(filepath)
  floats = []
  with open(testpath, 'wb') as test:
    for i in range(len(orignal)):
      buf = pack('>f',orignal[i])
      floats.append(orignal[i])
      test.write(buf)
  test.close
  print("orignal - conversion = ", np.sum(orignal)-np.sum(floats))
  return floats

#has the effect of adding static
def shiftandWrite(track,shifted_track,rate,floats):
  track = open(track)
  with open(shifted_track, 'wb') as track:
    for i in range(len(floats)):
      if str(floats[i])=='nan':
        buf=pack('f',floats[i])
      else:
        buf=pack('f',floats[i]+10)
      track.write(buf)
  track.close

def generateSamplePCM(filepath):
  sample = open(filepath)
  with open(filepath, 'wb') as sample:
    for i in range(44100):
      x=(i/44100)*44100*2*math.pi
      buf=pack('f',math.sin(x))
      sample.write(buf)
  sample.close

def createEchoWith(filepath,testpath,floats,delay):
  echo=[]
  test = open(filepath)
  count=0
  with open(testpath, 'wb') as test:
    for i in range(len(floats)):
      count+=1
      if count<delay:
        buf = pack('f',floats[i])
        test.write(buf)
      if count>delay:
        try:
          mix=mixEquation1(floats[i],floats[i-delay],25)
          echo.append(mix)
          byte=pack('f',mix)
          test.write(byte)
        except IndexError:
          pass
  test.close
  return echo

#this function takes x[a to z] and returns x[z to a]
def writeBytesBackwards(filepath,testpath,floats):
  test = open(filepath)
  reverse=[]
  with open(testpath, 'wb') as test:
    for i in range(len(floats)):
      buf = pack('f',floats[len(floats)-i-1])
      reverse.append(floats[len(floats)-i-1])
      test.write(buf)
  test.close
  return reverse

#this function adds signal a to signal b index wise
def sumSignals(floats1,floats2,testpath):
  x,y=arangeLargestSmallest(floats1,floats2)
  composed_signal=open(testpath)
  sum=[]
  with open(testpath,'wb') as composed_signal:
    for i in range(len(x)):
       try:
         #z=round(mixEquation2(int(x[i]),int(y[i])),5)
         z=mixEquation(x[i],y[i],0.8,0.9)
         #z=(x[i]+y[i])
         #print(z)
         byte=pack('f',z)
         composed_signal.write(byte)
         sum.append(z)
       except IndexError:
         byte = pack('f',x[i])
         composed_signal.write(byte)
         sum.append(x[i])
  composed_signal.close
  return sum

#y(n) = x(n) + x(n-1)
def lowPassFilter(filepath,testpath,x):
  unfiltered=open(filepath)
  y=[]
  with open(testpath,'wb') as unfiltered:
    for n in range(len(x)):
      yn=x[n]+x[n-1]
      y.append(yn)
      byte=pack('f',yn)
      unfiltered.write(byte)
  unfiltered.close
  return y

#this function rolls x samples by n
def rolltrack(track,testpath,x):
  unrolled=open(track)
  rolled=np.roll(x,len(x)+len(x)//3)
  with open(testpath,'wb') as unrolled:
    for i in range(len(rolled)):
      byte=pack('f',rolled[i])
      unrolled.write(byte)
  unrolled.close
  return rolled

#this function appends x to y
def appendSignals(floats1,floats2,appended_track):
  x,y=arangeLargestSmallest(floats1,floats2)
  track=open(appended_track)
  with open(appended_track,'wb') as track:
    for i in range(len(x)):
      byte=pack('f',x[i])
      track.write(byte)
    for i in range(len(y)):
      byte=pack('f',y[i])
      track.write(byte)

def multipleIndexWiseDistortion(x,unnorm,filepath,multiple):
  track=open(unnorm)
  test=[]
  with open(filepath,'wb') as track:
    for i in range(len(x)):
      byte=pack('f',x[i]*multiple)
      test.append(x[i]*multiple)
      track.write(byte)
  track.close()
  return test

def getStats(x,y):
  npx=np.array(x)
  npy=np.array(y)
  print('difference in x - y = ',sum(x)-sum(y))
  print('std of x = ',np.std(npx))
  print('std of y = ',np.std(npy))
  print('range of x is between ',min(x),' and ',max(x))
  print('range of y is between ',min(y),' and ',max(y))

"""
Fs=1/48000
track2="convertLoss.pcm"
track1="pcm_float.pcm"
floats1=getFloatsfromTrack(track1,nan=False)
test=multipleIndexWiseDistortion(floats1,track1,track2,.99999)
plots={'track1':floats1,'track2':test}
getStats(floats1,test)
doRecursivePlot(plots,(7,7),Fs)
"""
"""
Fs=1/48000
track1="appendTest.pcm"
track2="gucci.pcm"
floats1=getFloatsfromTrack(track1,nan=False)
floats2=getFloatsfromTrack(track2,nan=False)
appendSignals(floats1,floats2,'convertLoss.pcm')
"""

"""
Fs=1/48000
trackpath="gucci.pcm"
unrolled=getFloatsfromTrack(trackpath,nan=False)
rolled=rolltrack(trackpath,'convertLoss.pcm',unrolled)
doPlot(unrolled,rolled,Fs)
"""

"""
Fs=1/48000
trackpath="gucci.pcm"
unfiltered=getFloatsfromTrack(trackpath,nan=False)
filtered=lowPassFilter(trackpath,'convertLoss.pcm',unfiltered)
doPlot(unfiltered,filtered,Fs)
"""


Fs=1/48000
track1="appendTest.pcm"
track2="gucci.pcm"
floats1=getFloatsfromTrack(track1,nan=False)
floats2=getFloatsfromTrack(track2,nan=False)
#test=[]
#m=min(floats2)
#for i in range(len(floats2)):
#  test.append(m-floats2[i])
s=sumSignals(floats1,floats2,'convertLoss.pcm')
#s=np.convolve(floats1,floats2,mode='full')
print("the range of track1: ", max(floats1), " <-> ", min(floats1))
print("the range of track2: ", max(floats2), " <-> ", min(floats2))
#plots={'appendTest':floats1,'gucci':floats2,'test':test,'sum':s}
plots={'appendTest':floats1,'gucci':floats2,'sum':s}
doRecursivePlot(plots,(10,10),Fs)


"""
Fs=1/48000
trackpath="gucci.pcm"
floats=getFloatsfromTrack(trackpath,nan=False)
reverse=writeBytesBackwards(trackpath,'convertLoss.pcm',floats)
doPlot(floats,reverse,Fs)
"""

"""
Fs=1/48000
sample_offset=10000
trackpath="gucci.pcm"
floats=getFloatsfromTrack(trackpath,nan=False)
echo=createEchoWith(trackpath,'convertLoss.pcm',floats,sample_offset)
doPlot(floats,echo,Fs)
"""

"""
Fs=1/48000
trackpath="gucci.pcm"
orignal=getFloatsfromTrack(trackpath,nan=False)
test=doConversionLossTest(trackpath,'convertLoss.pcm',orignal)
doPlot(orignal,test,Fs)
"""

"""
Fs=1/48000
trackpath="gucci.pcm"
track=getFloatsfromTrack(trackpath,nan=False)
shift=np.array(track)+100
doPlot(track,shift,Fs)
"""

"""
trackpath="gucci.pcm"
floats=getFloatsfromTrack(trackpath,nan=False)
shiftandWrite(trackpath,"shifted_track.pcm",48000,floats)
"""

"""
filepath="convertLoss.pcm"
generateSamplePCM(filepath)
"""


