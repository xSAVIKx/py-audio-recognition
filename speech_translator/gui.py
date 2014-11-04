# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main.ui'
#
# Created: Mon Nov  3 17:33:00 2014
# by: PyQt5 UI code generator 5.3.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QDialog, QMessageBox
import goslate

from speech_translator.speech.language import Language
from speech_translator.speech.recognizer import SpeechRecognizer
from speech_translator.speech.text_to_speech import TextToSpeech


_translate = QtCore.QCoreApplication.translate


class UiTranslator(QDialog):
    def __init__(self):
        super(UiTranslator, self).__init__()
        self.say_button = QtWidgets.QPushButton(self)
        self.record_button = QtWidgets.QPushButton(self)
        self.to_language = QtWidgets.QComboBox(self)
        self.from_language = QtWidgets.QComboBox(self)
        self.from_language_label = QtWidgets.QLabel(self)
        self.to_language_label = QtWidgets.QLabel(self)
        self.grid_layout = QtWidgets.QGridLayout(self)

    def setup_ui(self):
        self.setObjectName("Translator")
        x_size = 270
        y_size = 100
        self.resize(x_size, y_size)
        self.setMinimumSize(QtCore.QSize(x_size, y_size))
        self.setMaximumSize(QtCore.QSize(x_size, y_size))
        self._setup_ui()
        self.retranslate_ui()

    def _setup_ui(self):
        self._setup_from_language()
        self._setup_to_language()
        self._setup_push_buttons()
        self._setup_layout()

    def _setup_layout(self):
        self.grid_layout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        content_margin = 5
        horizontal_spacing = 15
        vertical_spacing = 5
        self.grid_layout.setContentsMargins(content_margin, content_margin, content_margin, content_margin)
        self.grid_layout.setHorizontalSpacing(horizontal_spacing)
        self.grid_layout.setVerticalSpacing(vertical_spacing)
        self.grid_layout.setObjectName("grid_layout")

        self.grid_layout.addWidget(self.to_language_label, 0, 0, 1, 1)

        self.grid_layout.addWidget(self.from_language_label, 0, 1, 1, 1)

        self.grid_layout.addWidget(self.from_language, 1, 0, 1, 1)

        self.grid_layout.addWidget(self.to_language, 1, 1, 1, 1)

        self.grid_layout.addWidget(self.record_button, 2, 0, 1, 1)

        self.grid_layout.addWidget(self.say_button, 2, 1, 1, 1)

    def _setup_push_buttons(self):
        self.record_button.setObjectName("record_button")
        self.say_button.setObjectName("say_button")

    def _setup_to_language(self):
        self.to_language_label.setObjectName("to_language_label")
        self.to_language.setObjectName("to_language")
        self.to_language.addItems(Language.languages.keys())

    def _setup_from_language(self):
        self.from_language_label.setObjectName("from_language_label")
        self.from_language.setObjectName("from_language")
        self.from_language.addItems(Language.languages.keys())


    def retranslate_ui(self):
        self.setWindowTitle(_translate("Translator", "Translator"))
        self.to_language_label.setText(_translate("Translator", "From language"))
        self.from_language_label.setText(_translate("Translator", "To language"))
        self.record_button.setText(_translate("Translator", "Record"))
        self.say_button.setText(_translate("Translator", "Say"))


class MainDialog(UiTranslator, object):
    def __init__(self):
        super(MainDialog, self).__init__()
        self.setup_ui()
        self.gs = goslate.Goslate()
        self.tts = TextToSpeech()
        self.speech = None
        self.record_button.clicked.connect(self.record_button_action)
        self.say_button.clicked.connect(self.translate_and_say)
        self.error_box = QMessageBox(self)
        self.spoken_text = ""
        self.translated_text = ""

    def record_button_action(self):
        if self.record_button.text() == 'Record':
            self.from_language.setDisabled(True)
            self.say_button.setDisabled(True)
            self.record_button.setText(_translate("Translator", "Stop"))

            self.speech = SpeechRecognizer()
            self.speech.set_mutex(True)
            self.speech.start()
        else:
            self.say_button.setDisabled(False)
            self.record_button.setDisabled(True)
            self.record_button.setText(_translate("Translator", "Record"))
            self.speech.set_mutex(False)
            self.speech.join()
            self.recognize_audio()

    def recognize_audio(self):
        from_language = self.from_language.currentText()
        try:
            self.spoken_text, full_response = self.speech.recognize(language=from_language)
        except LookupError as e:
            self.error_box.warning(self, self.tr("Unintelligible speech"), self.tr(e.message))
            self.unblock_dialog_elements()


    def translate_text(self):
        from_language = self.from_language.currentText()
        to_language = self.to_language.currentText()
        self.translated_text = self.gs.translate(text=self.spoken_text,
                                                 target_language=Language.get_language(to_language),
                                                 source_language=Language.get_language(from_language))

    def unblock_dialog_elements(self):
        self.from_language.setDisabled(False)
        self.to_language.setDisabled(False)
        self.say_button.setDisabled(False)
        self.record_button.setDisabled(False)

    def translate_and_say(self):
        self.translate_text()
        self.say_text()

    def say_text(self):
        self.unblock_dialog_elements()
        to_language = self.to_language.currentText()
        self.tts.say(self.translated_text, to_language)