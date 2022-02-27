# can install pyaudio using anaconda
# need to install portaudio first
# do conda install -c anaconda portaudio
# then install the pyaudio 
# pip install pyaudio should work now
import pyaudio
import sounddevice as sd
import soundfile as sf
from scipy.io.wavfile import write
import winsound

# how to play sound on windows
# input is the filename
def play_sound(filename):
    winsound.PlaySound(filename, winsound.SND_FILENAME)

# record using the mic 
# the inputs are the name of the file and the length of the file
def recording(filename="output", length=3):

    fs = 44100  # Sample rate
    seconds = length  # Duration of recording

    myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
    sd.wait()  # Wait until recording is finished
    write('{}.wav'.format(filename), fs, myrecording)  # Save as WAV file 