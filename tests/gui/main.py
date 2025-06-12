import os
import sys
from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile

loader = QUiLoader()
app = QtWidgets.QApplication(sys.argv)

# get path of mainwindow.ui
script_dir = os.path.dirname(__file__)
ui_file_path = os.path.join(script_dir, "mainwindow.ui")


window = loader.load(ui_file_path, None)
window.showMaximized()
app.exec()