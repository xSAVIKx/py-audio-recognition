# coding=utf-8

__author__ = 'Iurii Sergiichuk <i.sergiichuk@samsung.com>'
import json
from threading import Thread
from wave import open as open_audio
from urllib2 import Request, urlopen
from os import system

from pyaudio import paInt16, PyAudio

from speech_translator.speech.language import Language


class SpeechRecognizer(Thread):
    def __init__(self, audio_file="audio", language=Language.get_language('english'),
                 key="AIzaSyBOti4mM-6x9WDnZIjIeyEU21OpBXqWBgw"):
        super(SpeechRecognizer, self).__init__(name="Speech recognizer thread")
        self.format = paInt16
        self.rate = 8000
        self.channel = 1
        self.chunk = 1024
        self.audio_file = audio_file
        self.language = language
        self.key = key
        self.mutex = None

    def run(self):
        self.record_with_mutex()

    def convert(self):
        print "CONVERTING START"
        system("sox %s -t wav -r 8000 -t flac %s.flac" % (self.audio_file, self.audio_file))
        print "CONVERTING STOP"

    def set_mutex(self, value):
        self.mutex = value

    def record_with_mutex(self):
        audio = PyAudio()
        stream = audio.open(format=self.format, channels=self.channel,
                            rate=self.rate, input=True,
                            frames_per_buffer=self.chunk)
        print "RECORDING START"
        frames = []
        while self.mutex:
            data = stream.read(self.chunk)
            frames.append(data)
        stream.stop_stream()
        stream.close()
        audio.terminate()
        print "RECORDING STOP"
        write_frames = open_audio(self.audio_file, 'wb')
        write_frames.setnchannels(self.channel)
        write_frames.setsampwidth(audio.get_sample_size(self.format))
        write_frames.setframerate(self.rate)
        write_frames.writeframes(''.join(frames))
        write_frames.close()
        self.convert()

    def record(self, time=5):
        audio = PyAudio()
        stream = audio.open(format=self.format, channels=self.channel,
                            rate=self.rate, input=True,
                            frames_per_buffer=self.chunk)
        print "RECORDING START"
        frames = []
        for i in range(0, self.rate / self.chunk * time):
            data = stream.read(self.chunk)
            frames.append(data)
        stream.stop_stream()
        stream.close()
        audio.terminate()
        print "RECORDING STOP"
        write_frames = open_audio(self.audio_file, 'wb')
        write_frames.setnchannels(self.channel)
        write_frames.setsampwidth(audio.get_sample_size(self.format))
        write_frames.setframerate(self.rate)
        write_frames.writeframes(''.join(frames))
        write_frames.close()
        self.convert()

    def recognize(self, language=None, key=None):
        language_to_use = self.language
        if language:
            language_to_use = Language.get_language(language)
        key_to_use = self.key
        if key:
            key_to_use = key
        url = "http://www.google.com/speech-api/v2/recognize?client=chromium&lang=%s&key=%s" % (
            language_to_use, key_to_use)
        file_upload = "%s.flac" % self.audio_file
        audio = open(file_upload, "rb").read()
        header = {"Content-Type": "audio/x-flac; rate=%s" % self.rate}
        data = Request(url, audio, header)
        post = urlopen(data)
        response = post.read().decode("utf-8")

        best_match_phase = self._get_response_text(response)
        return best_match_phase, response

    def _get_response_text(self, response_text, show_all=False):
        # ignore any blank blocks
        actual_result = []
        for line in response_text.split("\n"):
            if not line: continue
            result = json.loads(line)["result"]
            if len(result) != 0:
                actual_result = result[0]

        # make sure we have a list of transcriptions
        if "alternative" not in actual_result:
            raise LookupError("Speech is unintelligible")

        # return the best guess unless told to do otherwise
        if not show_all:
            for prediction in actual_result["alternative"]:
                if "confidence" in prediction:
                    return prediction["transcript"]
            raise LookupError("Speech is unintelligible")

        spoken_text = []

        # check to see if Google thinks it's 100% correct
        default_confidence = 0
        if len(actual_result["alternative"]) == 1: default_confidence = 1

        # return all the possibilities
        for prediction in actual_result["alternative"]:
            if "confidence" in prediction:
                spoken_text.append({"text": prediction["transcript"], "confidence": prediction["confidence"]})
            else:
                spoken_text.append({"text": prediction["transcript"], "confidence": default_confidence})
        return spoken_text