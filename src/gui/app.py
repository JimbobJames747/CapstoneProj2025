import os
import sys
from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile
from .logic import LogicHandler



class MainApp:
    def __init__(self):
        QtGui.QGuiApplication.setApplicationName("Simulaysh")
        QtGui.QGuiApplication.setApplicationVersion("alpha 0.1")

        # get path of mainwindow.ui and load
        loader = QUiLoader()
        self.app = QtWidgets.QApplication(sys.argv)
        script_dir = os.path.dirname(__file__)
        ui_file_path = os.path.join(script_dir, "res/mainwindow.ui")
        self.window = loader.load(ui_file_path, None)

        self.logic = LogicHandler()
        self.window.pushButton.clicked.connect(self.logic.start_simulation)
        
        # menu bar file-->exit
        self.window.actionExit.triggered.connect(self.logic.exit_app)


    def run(self):
        self.window.showMaximized()
        self.app.exec()

if __name__ == "__main__":
    app = MainApp()
    app.run()
