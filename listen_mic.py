# can install pyaudio using anaconda
# need to install portaudio first
# do conda install -c anaconda portaudio
# then install the pyaudio 
# pip install pyaudio should work now
import pyaudio
import sounddevice as sd
import soundfile as sf
from scipy.io.wavfile import write

fs = 44100  # Sample rate
seconds = 3  # Duration of recording

myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
sd.wait()  # Wait until recording is finished
write('output.wav', fs, myrecording)  # Save as WAV file 