import os
import sys
from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtWidgets import QGraphicsScene, QLabel, QGraphicsView
from PySide6.QtUiTools import QUiLoader
from PySide6.QtGui import QDrag
from PySide6.QtCore import QFile, QMimeData, QResource
from PySide6.QtGui import QPixmap
import gui.res.resources




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


        label_3 = self.window.findChild(QLabel, "label_3")
        pixmap = QPixmap(":/img/test.png")  # Use the resource path here
        label_3.setPixmap(pixmap) 

        
        res = QResource(":/src/gui/res/img/test.png")
        print("Resource exists:", res.isValid())

        print(QResource(":/src/gui/res/img/test.png").isValid())
        print(QResource(":/src/gui/res/img/test.png").isValid())
        print(QResource(":/src/gui/res/img/test.png").isValid())
        print(QResource(":/src/gui/res/img/test.png").isValid())

        print("Pixmap is null?", pixmap.isNull())

        f = QFile("src/gui/res/img/test.png")
        print("Resource file exists?", f.exists())

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
