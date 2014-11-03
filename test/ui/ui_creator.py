from PyQt5.uic import compileUi

__author__ = 'Iurii Sergiichuk <i.sergiichuk@samsung.com>'


with open("main.ui", 'r') as ui:
    with open("gui.py", 'w') as gui:
        compileUi(ui, gui)