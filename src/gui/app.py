import os
import sys
from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtWidgets import QGraphicsScene, QLabel, QGraphicsView
from PySide6.QtUiTools import QUiLoader
from PySide6.QtGui import QDrag
from PySide6.QtCore import QFile, QMimeData



from .slots import SlotHandler



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


        # set up basic logic handling
        self.logic = SlotHandler(self.window)
        #self.window.pushButton.clicked.connect(lambda: self.logic.change_label("test"))
        # menu bar file-->exit
        self.window.actionExit.triggered.connect(self.logic.exit_app)


        # set up drag and drop area (graphics scene)
        self.scene = QGraphicsScene()
        self.view = self.window.findChild(QGraphicsView, "graphicsView")
        self.view.setScene(self.scene)



    # start gui
    def run(self):
        self.window.showMaximized()
        self.app.exec()

if __name__ == "__main__":
    app = MainApp()
    app.run()
