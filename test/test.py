import wave

import pyaudio

__author__ = 'Iurii Sergiichuk <i.sergiichuk@samsung.com>'

import speech_recognition as sr

r = sr.Recognizer()
p = pyaudio.PyAudio()
CHUNK = 1024
frames = []
stream = p.open(format=pyaudio.paInt16,
                channels=1,
                rate=44100,
                input=True,
                frames_per_buffer=1024,
                output_device_index=1)

for i in range(0, 100):
    data = stream.read(CHUNK)
    frames.append(data)

stream.stop_stream()
stream.close()
p.terminate()
wf = wave.open('out.wav', 'wb')
wf.setnchannels(1)
wf.setsampwidth(p.get_sample_size(pyaudio.paInt16))
wf.setframerate(44100)
wf.writeframes(b''.join(frames))
wf.close()
with sr.WavFile("out.wav") as source:  # use the default microphone as the audio source
    audio = r.listen(source, timeout=10)  # listen for the first phrase and extract it into audio data

try:
    print("You said " + r.recognize(audio))  # recognize speech using Google Speech Recognition
except LookupError:  # speech is unintelligible
    print("Could not understand audio")