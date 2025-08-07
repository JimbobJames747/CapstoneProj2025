import os
import sys
from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtWidgets import QGraphicsScene, QLabel, QGraphicsView, QGraphicsItem, QGraphicsRectItem, QListWidget
from PySide6.QtUiTools import QUiLoader 
from PySide6.QtGui import QDrag, QColor
from PySide6.QtCore import QFile, QMimeData, QResource
from PySide6.QtGui import QPixmap
import gui.res.resources




from .slots import SlotHandler

class DrawingArea(QtWidgets.QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAcceptDrops(True)
        self.setStyleSheet("background-color: #f0f0f0; border: 2px dashed gray;")

    def dragEnterEvent(self, event):
        print("dragEnterEvent")
        if event.mimeData().hasText():
            event.acceptProposedAction()
        else:
            event.ignore()

    def dropEvent(self, event):
        print("dropEvent:", event.mimeData().text())
        event.acceptProposedAction()


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

        # exit button clicked
        self.window.exitBtn.clicked.connect(self.logic.exit_app)

        # new network button clicked
        self.window.newBtn.clicked.connect(self.logic.new_button_clicked)

        # run button clicked
        self.window.runBtn.clicked.connect(self.logic.run_button_clicked)

        # stop button clicked
        self.window.stopBtn.clicked.connect(self.logic.stop_button_clicked)

        #save button clicked
        self.window.saveBtn.clicked.connect(lambda: self.logic.save_button_clicked("test"))

        ##############################################
        ### ADDING COMPONENTS TO DRAWING AREA BTNS ###
        ##############################################

        # add source button clicked
        self.window.addSourceBtn.clicked.connect(self.logic.add_source_button_clicked)

        # add detector button clicked
        self.window.addDetectorBtn.clicked.connect(self.logic.add_detector_button_clicked)

        # add fibre button clicked
        self.window.addFibreBtn.clicked.connect(self.logic.add_fibre_button_clicked)

        ### presets ###

        # add single link preset button clicked

        self.window.addSingleLinkBtn.clicked.connect(self.logic.add_single_link_button_clicked)
        
        ####################################
        ### SELECTING COMPONENTS IN TREE ###
        ####################################

       # self.window.


        ########################
        ### BTNS FOR TESTING ###
        ########################

        self.window.printNetBtn.clicked.connect(self.logic.print_network_button_clicked)

        self.window.showBtn.clicked.connect(self.logic.show_button_clicked)


    # start gui
    def run(self):
        self.window.showMaximized()
        self.app.exec()

if __name__ == "__main__":
    app = MainApp()
    app.run()
