from fileinput import filename
import cv2
import numpy as np
import pandas as pd   # https://pypi.org/project/pandas/
import matplotlib.pylab as plt  # https://pypi.org/project/matplotlib/

from audiolazy import str2midi # https://pypi.org/project/audiolazy/
from midiutil import MIDIFile # https://midiutil.readthedocs.io/en/1.2.1/
from scipy import signal
from midi_numbers import instrument_to_program

##############################################################################
duration_beats = 52.8 #desired duration in beats (1 beat = 1 second if bpm=60)
bpm = 60 #tempo (beats per minute)

y_scale = 0.5  #scaling parameter for y-axis data (1 = linear)

#note set for mapping (or use a few octaves of a specific scale)
# note_names = ['C1','C2','G2',
#              'C3','E3','G3','A3','B3',
#              'D4','E4','G4','A4','B4',
#              'D5','E5','G5','A5','B5',
#              'D6','E6','F#6','G6','A6']

note_names = ['C2','D2','E2','G2','A2',
             'C3','D3','E3','G3','A3',
             'C4','D4','E4','G4','A4']

# blue_notes = ['C3', 'E3', 'G3', 'B3']
blue_notes  = ['D4', 'F#4', 'A4', 'C5']
green_notes= ['E5', 'G5', 'B5', 'D6']
red_notes = ['C6', 'E6', 'G6', 'B6']

vel_min,vel_max = 35,127   #minimum and maximum note velocity

##############################################################################
def map_value(value,min_value,max_value,min_result,max_result):
    '''maps value (or array of values) from one range to another'''
    result = min_result + (value - min_value)/(max_value-min_value)*(max_result - min_result)
    return result
##############################################################################


def strideConv(arr, arr2, s):
    return signal.convolve2d(arr, arr2[::-1, ::-1], mode='valid')[::s, ::s]


def main():
    # Load an image
    filename = "NGC_2336.jpg"
    image = cv2.imread(f'./data/{filename}')
    image = cv2.resize(image, dsize=(100, 100))

    # Define a 5x5 kernel with equal weights
    kernel = np.ones((5, 5), dtype=np.float32) / 25.0

    # Apply the kernel to the image using convolution
    # result = cv2.filter2D(image, -1, kernel)
    blue = strideConv(image[:, :, 0], kernel, 5).astype(np.uint8).flatten()
    green = strideConv(image[:, :, 1], kernel, 5).astype(np.uint8).flatten()
    red = strideConv(image[:, :, 2], kernel, 5).astype(np.uint8).flatten()
    
    # Fix hardcoding
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.resize(gray, dsize=(20, 20))
    gray = gray.flatten()

    # Display the original and filtered images
    # cv2.imshow('Original Image', image)
    # cv2.imshow('Filtered Image', result)
    # print(image.shape, result.shape)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    ## Compress Time
    t_data = map_value(gray, min(gray), max(gray), duration_beats, 0) #compress time from Myrs to beats

    ## Calculate duration in seconds
    duration_sec = max(t_data)*60/bpm #duration in seconds (actually, onset of last note)
    print('Duration:',duration_sec,'seconds')

    ## Normalize and scale y-axis data
    y1_data = map_value(blue, min(blue), max(blue), 0, 1) #normalize data, so it runs from 0 to 1 (makes scaling easier)
    y1_data = y1_data**y_scale
    y2_data = map_value(green, min(green), max(green), 0, 1) 
    y2_data = y2_data**y_scale
    y3_data = map_value(red, min(red), max(red), 0, 1) 
    y3_data = y3_data**y_scale

    print(min(blue), max(blue))

    ## Make list of MIDI numbers of chosen notes for mapping
    note_midis = [str2midi(n) for n in note_names] # make a list of midi note numbers
    blue_note_midis = [str2midi(n) for n in blue_notes]
    red_note_midis = [str2midi(n) for n in red_notes]
    green_note_midis = [str2midi(n) for n in green_notes]
    n_notes = len(note_midis)
    print('Resolution:',n_notes,'notes')

    ## Save MIDI file
    my_midi_file = MIDIFile(3) #one track
    my_midi_file.addTempo(track=0, time=0, tempo=bpm)
    my_midi_file.addProgramChange(0, 0, 0, 0)
    my_midi_file.addProgramChange(0, 1, 0, instrument_to_program('Electric Guitar (clean)'))
    # my_midi_file.addProgramChange(0, 1, 0, instrument_to_program('Violin'))
    my_midi_file.addProgramChange(0, 2, 0, instrument_to_program('Steel Drums'))
    # my_midi_file.addProgramChange(0, 2, 0, instrument_to_program('Harmonica'))

    for i in range(len(gray)):
        note_index = round(map_value(y1_data[i], 0, 1, len(blue_notes)-1, 0))
        note_velocity = round(map_value(y1_data[i], 0, 1, vel_min, vel_max))
        my_midi_file.addNote(track=0, channel=0, pitch=blue_note_midis[note_index], time=t_data[i] , duration=2, volume=note_velocity)

        note_index = round(map_value(y2_data[i], 0, 1, len(green_notes)-1, 0))
        note_velocity = round(map_value(y2_data[i], 0, 1, vel_min, vel_max))
        my_midi_file.addNote(track=1, channel=1, pitch=green_note_midis[note_index], time=t_data[i] , duration=2, volume=note_velocity)

        note_index = round(map_value(y3_data[i], 0, 1, len(red_notes)-1, 0))
        note_velocity = round(map_value(y3_data[i], 0, 1, vel_min, vel_max))
        my_midi_file.addNote(track=2, channel=2, pitch=red_note_midis[note_index], time=t_data[i] , duration=2, volume=note_velocity)


    with open(f'{filename}.mid', "wb") as f:
        my_midi_file.writeFile(f)
    print('Saved' + '.mid')

if __name__ == "__main__":
    main()