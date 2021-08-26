from struct import unpack, pack
import numpy as np

def get_bytes(file_path):
    bytes=b''
    with open(file_path,'rb') as f:
        bytes=f.read()
    return bytes[44:]

def get_shorts(bytes):
    count = len(bytes)//2
    return unpack('h'*count,bytes)

def mix(s1,s2):
    s1,s2=fit(s1,s2)
    mixed=[]
    for i in range(len(s1)):
        s=(s1[i]+s2[i])
        mixed.append(s)
    return np.array(mixed).tobytes()  

def fit(s1,s2):
    if len(s1)>len(s2):
        s1=s1[:len(s2)]
    elif len(s1)<len(s2):
        s2=s2[:len(s1)]
    return s1,s2

def writeWav(pcm):

    sampleRate=48000
    num_channels=1
    samples=len(pcm)
    subchunk2size=samples*num_channels*(16//8)+36
    byterate=sampleRate*1*(16//8)
    blockalign=1*(16//8)

    with open("sumSignal.wav",'wb') as f:
        f.write(pack('>I',0x52494646)) #RIFF
        f.write(pack('<i',samples+36))  
        f.write(pack('>I',0x57415645)) #WAVE
        f.write(pack('>I',0x666d7420)) #FMT
        f.write(pack('<L',16))
        f.write(pack('<H',1))  
        f.write(pack('<H',1))    
        f.write(pack('<L',sampleRate))
        f.write(pack('<L',byterate))
        f.write(pack('<H',blockalign))
        f.write(pack('<H',16))
        f.write(pack('>I',0x64617461)) #data
        f.write(pack('<i',samples))
        f.write(pcm)

    from playsound import playsound
    playsound('sumSignal.wav')

bytes_1=get_bytes('your wav file here')
bytes_2=get_bytes('your other wav file here')

shorts_1=get_shorts(bytes_1)
shorts_2=get_shorts(bytes_2)

writeWav(mix(shorts_1,shorts_2))
