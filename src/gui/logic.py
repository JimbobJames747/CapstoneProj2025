import sys

class LogicHandler:
    def __init__(self, ui):
        self.ui = ui

    def start_simulation(self):
        print("Starting simulation...")

    #To do: make it for general label
    def change_label(self, text):
        self.ui.label.setText(text)

    def exit_app(self):
        sys.exit(0)