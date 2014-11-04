import goslate

from speech_translator.speech.language import Language
from speech_translator.speech.recognizer import SpeechRecognizer
from speech_translator.speech.text_to_speech import TextToSpeech


__author__ = 'Iurii Sergiichuk <i.sergiichuk@samsung.com>'


# TEST HERE ###
gs = goslate.Goslate()
tts = TextToSpeech()
speech = SpeechRecognizer()
speech.record(5)
phrase, complete_response = speech.recognize('english')
print phrase
tts.say(phrase, language='english')

translated_phase = gs.translate(text=phrase, target_language=Language.get_language('russian'),
                                source_language=Language.get_language('english'))
print translated_phase
tts.say(translated_phase, language='russian')