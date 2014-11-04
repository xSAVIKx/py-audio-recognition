from speech_translator.gui import MainDialog

__author__ = 'Iurii Sergiichuk <i.sergiichuk@samsung.com>'

import sys

from PyQt5.QtWidgets import QApplication


if __name__ == "__main__":
    app = QApplication(["Translator"])
    ui = MainDialog()
    ui.show()
    sys.exit(app.exec_())