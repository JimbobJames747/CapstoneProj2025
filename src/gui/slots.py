import sys

class SlotHandler:
    def __init__(self, ui):
        self.ui = ui

    #To do: make it for general label
    def change_label(self, text):
        self.ui.label.setText(text)

    def exit_app(self):
        sys.exit(0)