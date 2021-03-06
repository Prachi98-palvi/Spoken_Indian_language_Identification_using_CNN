# -*- coding: utf-8 -*-
"""Spectrogram_SLID.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1aZuw45sAFPSCEMYq3ftVZCxepYb1ToSr

# Mounting Drive
"""

from google.colab import drive
drive.mount('/content/drive/')

"""# Importing Packages"""

import os
import librosa


import matplotlib.pyplot as plt
from scipy import signal
from scipy.io import wavfile

import pandas as pd
from glob import glob
import numpy as np

import librosa
import librosa.display
import pylab
import matplotlib.pyplot as plt
from matplotlib import figure
import gc
from pathlib import Path
import matplotlib.pyplot as plot
from scipy.io import wavfile
import wave

"""# Defining a function for audio_paths and Making necessary directories"""

def get_audio_paths(path):
    
    audio_paths = []
    
    ls = os.listdir(path) #extracts list of folders in directory 
    for l in ls:
        iss = os.listdir(os.path.join(path,l)) #extracts filenames 
        for i in iss:
            audio_paths.append(os.path.join(path,l,i))

    return audio_paths

path = "/content/drive/My Drive/audio_files"
audio_paths = get_audio_paths(path)

"""To check how many files have been loaded"""

len(audio_paths)

!mkdir "/content/drive/My Drive/project/"
!mkdir "/content/drive/My Drive/project/train/"
!mkdir "/content/drive/My Drive/project/test/
!mkdir "/content/drive/My Drive/project/newdata/"
!mkdir "/content/drive/My Drive/project/newdata/kan/" #kannada
!mkdir "/content/drive/My Drive/project/newdata/hin/" #Hindi
!mkdir "/content/drive/My Drive/project/newdata/mar/" #Marathi
!mkdir "/content/drive/My Drive/project/newdata/tam/" #Tamil
!mkdir "/content/drive/My Drive/project/newdata/ben/" #Bengali
!mkdir "/content/drive/My Drive/project/newdata/mal/" #Malayalam
!mkdir "/content/drive/My Drive/project/newdata/tel/" #Telugu

# since the files are already loaded once they cannot be reloaded as they already exist

filename = audio_paths[4003]
print(filename)

"""# **EDA**"""

import wave 
print(filename,'\n')
clip, sample_rate = librosa.load(filename, sr=None) 
test = wave.open(filename)
print(test.getparams() )
duration = len(clip)/sample_rate
print('Duration : ',duration)

"""*   No of channels is 1 i.e Single channel Mono Sound
*   Framerate/Sample rate of our audio files is 16000
"""

print('Librosa.load uses default sampling rate as : ',sr,'Hz')
print('To use original sampling rate specify sr as None : ',sample_rate,'Hz')

y, sr = librosa.load(filename) 
clip, sample_rate = librosa.load(filename, sr=None) 
# trim silent edges
test_audio, _ = librosa.effects.trim(clip)
librosa.display.waveplot(test_audio, sr=sample_rate)
plot.title('Time-Domain Representation')
plot.xlabel('Time')
plot.ylabel('Amplitude')
plot.show()

"""This visualization is called the time-domain representation of a given signal. This shows us the loudness (amplitude) of sound wave changing with time. Here amplitude = 0 represents silence. (From the definition of sound waves — This amplitude is actually the amplitude of air particles which are oscillating because of the pressure change in the atmosphere due to sound).
These amplitudes are not very informative, as they only talk about the loudness of audio recording. To better understand the audio signal, it is necessary to transform it into the frequency-domain. The frequency-domain representation of a signal tells us what different frequencies are present in the signal.
"""

S = librosa.feature.melspectrogram(y=clip, sr=sample_rate)

librosa.display.specshow(S,sr=sr, x_axis='time', y_axis='linear')
plot.title(os.path.basename(filename))
plot.xlabel('Time')
plot.ylabel('Frequency')
plt.colorbar()
plot.show()

"""Transform both, y-axis (frequency) to log scale, and the “color” axis (amplitude) to Decibels, which is kinda the log scale of amplitudes.

The Mel Scale, mathematically speaking, is the result of some non-linear transformation of the frequency scale. This Mel Scale is constructed such that sounds of equal distance from each other on the Mel Scale, also “sound” to humans as they are equal in distance from one another.
In contrast to Hz scale, where the difference between 500 and 1000 Hz is obvious, whereas the difference between 7500 and 8000 Hz is barely noticeable.
Luckily, someone computed this non-linear transformation for us, and all we need to do to apply it is use the appropriate command from librosa.
"""

librosa.display.specshow(librosa.power_to_db(S, ref=np.max),sr = sr,x_axis='time', y_axis='mel')
plot.title(os.path.basename(filename))
plot.xlabel('Time')
plot.ylabel('Frequency')
plt.colorbar(format='%+2.0f dB')
plot.show()

"""Defining a function to create spectrograms and saving them with their names intact"""

def create_spectrogram(filename,name):
    plt.interactive(False)
    clip, sample_rate = librosa.load(filename, sr=None)
    fig = plt.figure(figsize=[0.72,0.72])
    ax = fig.add_subplot(111)
    ax.axes.get_xaxis().set_visible(False)
    ax.axes.get_yaxis().set_visible(False)
    ax.set_frame_on(False)
    S = librosa.feature.melspectrogram(y=clip, sr=sample_rate)
    librosa.display.specshow(librosa.power_to_db(S, ref=np.max))
    folder = name.split('_')[0]
    filename  = '/content/drive/My Drive/project/newdata/'+folder+'/' + name + '.jpg'
    fig.savefig(filename, dpi=400, bbox_inches='tight',pad_inches=0)
    plt.close()    
    fig.clf()
    plt.close(fig)
    plt.close('all')
    del filename,name,clip,sample_rate,fig,ax,S

def create_spectrogram_test(filename,name):
    plt.interactive(False)
    clip, sample_rate = librosa.load(filename, sr=None)
    fig = plt.figure(figsize=[0.72,0.72])
    ax = fig.add_subplot(111)
    ax.axes.get_xaxis().set_visible(False)
    ax.axes.get_yaxis().set_visible(False)
    ax.set_frame_on(False)
    S = librosa.feature.melspectrogram(y=clip, sr=sample_rate)
    librosa.display.specshow(librosa.power_to_db(S, ref=np.max))
    filename  = Path('/content/drive/My Drive/project/test/' + name + '.jpg')
    fig.savefig(filename, dpi=400, bbox_inches='tight',pad_inches=0)
    plt.close()    
    fig.clf()
    plt.close(fig)
    plt.close('all')
    del filename,name,clip,sample_rate,fig,ax,S

test_paths = audio_paths
for i in range(0,len(test_paths)):
  file = audio_paths[i]
  filename,name = file,file.split('/')[-1].split('.')[0]
  #lang = name.split('_')[0]
  #if lang == 'tel':
  create_spectrogram(filename,name) #(path,name) #rename kan to kannada in drive folder after saving 

#create_spectrogram(audio_paths[0],'test1')

#audio_paths[6999].split('/')[-1].split('.')[0].split('_')[0]

"""## Example"""

path = "/content/drive/My Drive/project/test/EDA/eda_main"
audio_paths = get_audio_paths(path)
audio_paths

for filename in audio_paths:
  y, sr = librosa.load(filename) 
  clip, sample_rate = librosa.load(filename, sr=None) 
  # trim silent edges
  test_audio, _ = librosa.effects.trim(clip)
  librosa.display.waveplot(test_audio, sr=sample_rate)
  name = filename.split('/')[-1].split('.')[0]
  print(name)
  duration = len(clip)/sample_rate
  print('Duration : ',duration)

  test = wave.open(filename)
  print(test.getparams() )
  
  plot.title('Time-Domain Representation ')
  plot.xlabel('Time')
  plot.ylabel('Amplitude')
  plot.show()

  S = librosa.feature.melspectrogram(y=clip, sr=sample_rate)
  librosa.display.specshow(S,sr=sr, x_axis='time', y_axis='linear')
  plot.title(os.path.basename(filename))
  plot.xlabel('Time')
  plot.ylabel('Frequency')
  plt.colorbar()
  plot.show()

  librosa.display.specshow(librosa.power_to_db(S, ref=np.max),sr = sr,x_axis='time', y_axis='mel')
  plot.title(os.path.basename(filename))
  plot.xlabel('Time')
  plot.ylabel('Frequency')
  plt.colorbar(format='%+2.0f dB')
  plot.show()