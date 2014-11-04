# coding=utf-8

__author__ = 'Iurii Sergiichuk <i.sergiichuk@samsung.com>'
import subprocess

from speech_translator.speech.language import Language


class TextToSpeech(object):
    def __init__(self, language=Language.get_festival_language('russian')):
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
        choose_voice_command = "(voice_%s)" % Language.get_festival_language(language)
        say_text_command = "(SayText \"%s\")" % text
        command_args = [self._festival_bin, choose_voice_command, say_text_command, '(exit)']
        return command_args