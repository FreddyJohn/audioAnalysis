from struct import *
import pcmExplore
import matplotlib.pyplot as plt

def getWavMetaData(raw_wav,f=False,b=False):
  metadata={}
  print("Canonical Wave raw metadata: ",raw_wav[:44])

  print("NOW PRINTING RIFF CHUNK DESCRIPTOR.........................")
  print("chunk id: ",raw_wav[:4])
  metadata['chunk_id']=raw_wav[:4]
  print("chunk size: ",unpack('<i',raw_wav[4:8])[0])
  print("format: ",raw_wav[8:12])
  metadata['format']=raw_wav[8:12]

  print("NOW PRINTING FMT SUB-CHUNK..................................")
  print("subchunk id: ",raw_wav[12:16])
  metadata['subchunk_id']=raw_wav[12:16]
  print("subchuck size: ",unpack('<L',raw_wav[16:20])[0])
  metadata['subchunk_size']=raw_wav[16:20]
  print("audio format: ",unpack('<H',raw_wav[20:22])[0])
  metadata['audio_format']=raw_wav[20:22]
  print("num channels: ",unpack('<H',raw_wav[22:24])[0])
  metadata['num_channels']=raw_wav[22:24]
  print("sample rate: ",unpack('<L',raw_wav[24:28])[0])
  metadata['sample_rate']=raw_wav[24:28]
  print("byte rate: ",unpack('<L',raw_wav[28:32])[0])
  metadata['byte_rate']=raw_wav[28:32]
  print("block align: ", unpack('<H',raw_wav[32:34])[0])
  metadata['block_align']=raw_wav[32:34]
  print("bits per sample: ",unpack('<H',raw_wav[34:36])[0])
  metadata['bits_per_sample']=raw_wav[34:36]

  print("NOW PRINTING DATA SUB-CHUNK.................................")
  print("subchuck 2 id: ",raw_wav[36:40])
  metadata['subchunk2_id']=raw_wav[36:40]
  print("subchuck 2 size: ",unpack('<i',raw_wav[40:44])[0])
  l=len(raw_wav[44:unpack('i',raw_wav[40:44])[0]])
  d=str(l//4)+'f'
  data=raw_wav[44:unpack('i',raw_wav[40:44])[0]]
  import time
  if f is True:
    time.sleep(2)
    print("raw audio data as float: ",unpack(d,data))
  if b is True:
    time.sleep(2)
    print("raw audio bit stream: ",unpack(str(l)+'b',data))

  return metadata


#bit_depth==bits_per_sample
def doPcmToWavMagic(sample_rate,bit_depth,num_channels,output_file,raw_pcm):

  print("ATEMPTING .PCM TO .WAV CONVERSION")
  new_file=open(output_file)
  with open(test,'wb') as new_file:

    print("NOW WRITING RIFF CHUNK DESCRIPTOR.........................")
    new_file.write(metadata['chunk_id'])
    num_bytes=len(raw_pcm)*num_channels*bit_depth//8
    cks=pack('<L',num_bytes+36)
    new_file.write(cks)
    new_file.write(metadata['format'])

    print("NOW WRITING FMT SUB-CHUNK..................................")
    new_file.write(metadata['subchunk_id'])
    new_file.write(metadata['subchunk_size'])
    new_file.write(metadata['audio_format'])
    new_file.write(metadata['num_channels'])
    metadata['sample_rate']=pack('<L',sample_rate)
    new_file.write(metadata['sample_rate'])
    metadata['byte_rate']=pack('<L',sample_rate*num_channels*bit_depth//8)
    new_file.write(metadata['byte_rate'])
    metadata['block_align']=pack('<H',num_channels*bit_depth//8)
    new_file.write(metadata['block_align'])
    new_file.write(metadata['bits_per_sample'])

    print("NOW WRITING DATA SUB-CHUNK.................................")
    new_file.write(metadata['subchunk2_id'])
    subcks2=pack('<L',num_bytes)
    new_file.write(subcks2)
    new_file.write(raw_pcm)
    new_file.close()

pcm_track="creation_test.pcm"
raw_pcm,pcm_size=pcmExplore.getBytesFromTrack(pcm_track)

wav_track="StarWars3.wav"
raw_wav,wav_size=pcmExplore.getBytesFromTrack(wav_track)

metadata=getWavMetaData(raw_wav)

test='pcmtowav.wav'
doPcmToWavMagic(48000,16,1,test,raw_pcm)
print("METADATA FROM CONVERSION RESULT:")
result=pcmExplore.getBytesFromTrack(test)
getWavMetaData(result[0]) #,b=True)



"""
NOTES

mp4 headers?

Feild	Length	Content		Access

ckID	4	id:"RIFF"	wav[:4]

cksize	4	ck size:4+n	wav[4:8]

WAVEID	4	id:"WAVE"	wav[8:12]


....wav[:44] --> audio data

more on headers,

  block align num channels * bits per sample / 8

  byte rate = sample rate * num channel * bits per sample / 8
    ex:22050*1*16/8=44100

  chunksize=36+subchunk2size

  subchunk2size = num of samples * num channels * bits per sample / 8
    this is the number of bytes in the audio data for .wav
    ex: 132300 = (num samples *1*16)/8
        1058400 = num samples * 16
        66150 = num samples
    recall that there are 8 bits in a byte and the encoding type 16 bit

"""
