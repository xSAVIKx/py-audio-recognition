# coding=utf-8
import json
import subprocess

import goslate


__author__ = 'Iurii Sergiichuk <i.sergiichuk@samsung.com>'

from wave import open as open_audio
from urllib2 import Request, urlopen
from os import system

from pyaudio import paInt16, PyAudio


class SpeechRecognizer(object):
    def __init__(self, audio_file="audio", language="en-US", key="AIzaSyBOti4mM-6x9WDnZIjIeyEU21OpBXqWBgw"):
        self.format = paInt16
        self.rate = 8000
        self.channel = 1
        self.chunk = 1024
        self.audio_file = audio_file
        self.language = language
        self.key = key

    def convert(self):
        system("sox %s -t wav -r 8000 -t flac %s.flac" % (self.audio_file, self.audio_file))

    def record(self, time=5):
        audio = PyAudio()
        stream = audio.open(format=self.format, channels=self.channel,
                            rate=self.rate, input=True,
                            frames_per_buffer=self.chunk)
        print "RECORDING: "
        frames = []
        for i in range(0, self.rate / self.chunk * time):
            data = stream.read(self.chunk)
            frames.append(data)
        stream.stop_stream()
        stream.close()
        audio.terminate()
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
            language_to_use = language
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


class TextToSpeech(object):
    festival_language_dictionary = {
        'ru-RU': 'msu_ru_nsh_clunits',
        'en-US': 'kal_diphone'
    }

    def __init__(self, language="ru-RU"):
        self._festival_bin = "festival"
        self.language = language

        pass

    def say(self, text, language=None):
        language_to_use = self.language
        if language:
            language_to_use = language
        args = self.get_say_command_with_language(text, language_to_use)
        p = subprocess.Popen(args,
                             stdin=subprocess.PIPE,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE,
                             close_fds=True)
        stdout, stderr = p.communicate()

    def get_say_command_with_language(self, text, language):
        choose_voice_command = "(voice_%s)" % self.festival_language_dictionary.get(language, 'english')
        say_text_command = "(SayText \"%s\")" % text
        command_args = [self._festival_bin, choose_voice_command, say_text_command, '(exit)']
        return command_args

### TEST HERE ###
gs = goslate.Goslate()
tts = TextToSpeech()
speech = SpeechRecognizer()
speech.record(5)  # duration in seconds (3)
phrase, complete_response = speech.recognize('en_US')  # select the language
print phrase
tts.say(phrase, language='en-US')

translated_phase = gs.translate(text=phrase, target_language='ru-RU', source_language='en-US')
print translated_phase
tts.say(translated_phase, language='ru-RU')