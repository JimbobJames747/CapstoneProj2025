import os
import sys
from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtWidgets import QGraphicsScene, QLabel, QGraphicsView, QGraphicsItem,QGraphicsRectItem, QListWidget, QDialog, QVBoxLayout, QLineEdit, QTreeWidget, QTreeWidgetItem, QTableWidget
from PySide6.QtUiTools import QUiLoader 
from PySide6.QtGui import QDrag, QColor
from PySide6.QtCore import QFile, QMimeData, QResource
from PySide6.QtGui import QPixmap
import gui.res.resources
import numpy as np





from .slots import SlotHandler

# class DrawingArea(QtWidgets.QFrame):
#     def __init__(self, parent=None):
#         super().__init__(parent)
#         self.setAcceptDrops(True)
#         self.setStyleSheet("background-color: #f0f0f0; border: 2px dashed gray;")

#     def dragEnterEvent(self, event):
#         print("dragEnterEvent")
#         if event.mimeData().hasText():
#             event.acceptProposedAction()
#         else:
#             event.ignore()

#     def dropEvent(self, event):
#         print("dropEvent:", event.mimeData().text())
#         event.acceptProposedAction()





class MainApp:
    def __init__(self):
        QtGui.QGuiApplication.setApplicationName("QUANTA")
        QtGui.QGuiApplication.setApplicationVersion("alpha 0.1")

        # get path of mainwindow.ui and load
        loader = QUiLoader()
        self.app = QtWidgets.QApplication(sys.argv)
        script_dir = os.path.dirname(__file__)
        ui_file_path = os.path.join(script_dir, "res/mainwindow.ui")
        self.window = loader.load(ui_file_path, None)

        



        # set up basic logic handling
        self.logic = SlotHandler(self.window, self)
        #self.window.pushButton.clicked.connect(lambda: self.logic.change_label("test"))
        # menu bar file-->exit
        self.window.actionExit.triggered.connect(self.logic.exit_app)

        # exit button clicked
        self.window.exitBtn.clicked.connect(self.logic.exit_app)

        # new network button clicked
        #self.window.newBtn.clicked.connect(self.logic.new_button_clicked)

        # run button clicked
        self.window.runBtn.clicked.connect(self.logic.run_button_clicked)

        # stop button clicked
        self.window.stopBtn.clicked.connect(self.logic.stop_button_clicked)

        #save button clicked
        #self.window.saveBtn.clicked.connect(lambda: self.logic.save_button_clicked("test"))
        self.window.saveBtn.clicked.connect(lambda: self.logic.save_button_clicked(self.logic.network))

        #close button clicked
        self.window.closeBtn.clicked.connect(self.logic.close_button_clicked)

        ##############################################
        ### ADDING COMPONENTS TO DRAWING AREA BTNS ###
        ##############################################

        # # add source button clicked
        # self.window.addSourceBtn.clicked.connect(self.logic.add_source_button_clicked)

        # # add detector button clicked
        # self.window.addDetectorBtn.clicked.connect(self.logic.add_detector_button_clicked)

        # # add fibre button clicked
        # self.window.addFibreBtn.clicked.connect(self.logic.add_fibre_button_clicked)




        ### presets ###
 


    #########################################
    ############# single link ###############
    #########################################

       # add single link preset button clicked

        self.window.addSingleLinkBtn.clicked.connect(self.logic.add_single_link_button_clicked)

    ####################################################
    ############# single link src sender ###############
    ####################################################

        self.window.addSingleLinkSenderBtn.clicked.connect(self.logic.add_single_link_button_src_at_sender_clicked)
        
        self.window.addRepChainBtn.clicked.connect(self.logic.add_repeater_chain_button_clicked)

        self.window.componentTree.itemClicked.connect(self.logic.component_tree_item_clicked_handler)

        self.window.paramTable.cellChanged.connect(self.logic.param_table_cell_changed_handler)


    #########################################
    ############ dialog boxes ###############
    #########################################

    def show_single_link_dialog(self):
        dialog = SingleLinkDialog()
        dialog.exec()  # modal popup



    # def show_repeater_chain_dialog(self):
    #     dialog = RepeaterChainDialog()
    #     dialog.exec()  # modal popup
    
    # start gui
    def run(self):
        self.window.showMaximized()
        self.app.exec()



class SingleLinkDialog(QDialog):
    def __init__(self):
        super().__init__()
        loader = QUiLoader()
        script_dir = os.path.dirname(__file__)
        ui_file_path = os.path.join(script_dir, "res/single_link_dialog.ui")
        loader.load(ui_file_path, self)
        self.ui = loader.load(ui_file_path)
        layout = QVBoxLayout(self)
        layout.addWidget(self.ui)
        self.setWindowTitle("Single Link Parameters")
        self.setMinimumSize(700, 500)
        self.setMaximumSize(700, 500)

        self.SL_indVar = None
        self.SL_depVar = None

        self.logic = SlotHandler(self.ui, self)

        self.ui.okBtn.clicked.connect(self.logic.single_link_dialog_handler)
        self.ui.cancelBtn.clicked.connect(self.close_single_link_dialog)

        self.ui.srcRepRateRBtn.pressed.connect(self.logic.SL_srcRepRateRBtn_selected)
        self.ui.dcProbPerBinRBtn.pressed.connect(self.logic.SL_dcProbPerBinRBtn_selected)
        self.ui.detEffRBtn.pressed.connect(self.logic.SL_detEffRBtn_selected)
        self.ui.linkLengthRBtn.pressed.connect(self.logic.SL_linkLengthRBtn_selected)

        self.ui.entProbRBtn.pressed.connect(self.logic.SL_entProbRBtn_selected)
        self.ui.entRateRBtn.pressed.connect(self.logic.SL_entRateRBtn_selected)
        self.ui.entFidRBtn.pressed.connect(self.logic.SL_entFidRBtn_selected)

    def get_len_range(self):
        start = float(self.ui.linkLenStart.text())
        end = float(self.ui.linkLenEnd.text())
        return [start, end]
    
    def get_def_eff_range(self):
        start = float(self.ui.detEffStart.text())
        end = float(self.ui.detEffEnd.text())
        return [start, end]

    def get_dc_prob_range(self):
        start = float(self.ui.dcProbStart.text())
        end = float(self.ui.dcProbEnd.text())
        return [start, end]

    def get_src_rep_rate_range(self):
        start = float(self.ui.srcRepStart.text())
        end = float(self.ui.srcRepEnd.text())
        return [start, end]
    
    def get_atten(self):
        return float(self.ui.fibreAtten.text())
    
    def get_iterations(self):
        return int(self.ui.nDataPoints.text())

    def close_single_link_dialog(self):
        self.close()





if __name__ == "__main__":
    app = MainApp()
    app.run()
