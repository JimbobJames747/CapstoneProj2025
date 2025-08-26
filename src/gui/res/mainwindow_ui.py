# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainwindow.ui'
##
## Created by: Qt User Interface Compiler version 6.9.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QFrame, QGridLayout, QHBoxLayout,
    QHeaderView, QLabel, QLayout, QMainWindow,
    QMenu, QMenuBar, QPushButton, QSizePolicy,
    QSpacerItem, QStatusBar, QTabWidget, QTableWidget,
    QTableWidgetItem, QTreeWidget, QTreeWidgetItem, QVBoxLayout,
    QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1920, 1080)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMinimumSize(QSize(960, 540))
        font = QFont()
        font.setFamilies([u"Neue Haas Grotesk Text Pro Ligh"])
        MainWindow.setFont(font)
        MainWindow.setCursor(QCursor(Qt.CursorShape.ArrowCursor))
        MainWindow.setMouseTracking(False)
        MainWindow.setAutoFillBackground(False)
        MainWindow.setStyleSheet(u"QLabel {\n"
"	color: black\n"
"}\n"
"QMenuBar {\n"
"	background-color: black;\n"
"	color: white\n"
"}\n"
"QStatusBar {\n"
"	background-color: black\n"
"}\n"
"")
        MainWindow.setTabShape(QTabWidget.TabShape.Rounded)
        self.actionNew = QAction(MainWindow)
        self.actionNew.setObjectName(u"actionNew")
        self.actionNew.setCheckable(False)
        self.actionNew.setEnabled(True)
        icon = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.DocumentNew))
        self.actionNew.setIcon(icon)
        self.actionSave = QAction(MainWindow)
        self.actionSave.setObjectName(u"actionSave")
        icon1 = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.DocumentSave))
        self.actionSave.setIcon(icon1)
        self.actionetc = QAction(MainWindow)
        self.actionetc.setObjectName(u"actionetc")
        self.actionExit = QAction(MainWindow)
        self.actionExit.setObjectName(u"actionExit")
        self.actionExit.setEnabled(True)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.centralwidget.setStyleSheet(u"QWidget {\n"
"	background-color: rgb(240, 255, 228)\n"
"}")
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setSizeConstraint(QLayout.SizeConstraint.SetDefaultConstraint)
        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.paramSelect = QWidget(self.centralwidget)
        self.paramSelect.setObjectName(u"paramSelect")
        self.paramSelect.setMinimumSize(QSize(600, 0))
        self.paramSelect.setMaximumSize(QSize(300, 16777215))
        self.paramSelect.setCursor(QCursor(Qt.CursorShape.ArrowCursor))
        self.paramSelect.setStyleSheet(u"QWidget#paramSelect {\n"
"	border: 2px solid black;\n"
"	background-color: #f0ffe4\n"
"}\n"
"QWidget {\n"
"	background-color: \"#f0ffe4\"\n"
"}")
        self.verticalLayout_4 = QVBoxLayout(self.paramSelect)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.label = QLabel(self.paramSelect)
        self.label.setObjectName(u"label")
        font1 = QFont()
        font1.setFamilies([u"Roboto Medium"])
        font1.setPointSize(14)
        self.label.setFont(font1)
        self.label.setStyleSheet(u"")

        self.verticalLayout_4.addWidget(self.label)

        self.componentTree = QTreeWidget(self.paramSelect)
        self.componentTree.setObjectName(u"componentTree")
        font2 = QFont()
        font2.setFamilies([u"Roboto Medium"])
        font2.setPointSize(12)
        self.componentTree.setFont(font2)
        self.componentTree.viewport().setProperty(u"cursor", QCursor(Qt.CursorShape.PointingHandCursor))
        self.componentTree.setStyleSheet(u"QTreeWidget {\n"
"	color: white;\n"
"	border: 2px solid black;\n"
"	background-color: rgb(36, 88, 104)\n"
"}")

        self.verticalLayout_4.addWidget(self.componentTree)

        self.selectedComponentLabel = QLabel(self.paramSelect)
        self.selectedComponentLabel.setObjectName(u"selectedComponentLabel")
        self.selectedComponentLabel.setFont(font1)

        self.verticalLayout_4.addWidget(self.selectedComponentLabel)

        self.paramTable = QTableWidget(self.paramSelect)
        if (self.paramTable.columnCount() < 2):
            self.paramTable.setColumnCount(2)
        __qtablewidgetitem = QTableWidgetItem()
        self.paramTable.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.paramTable.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        self.paramTable.setObjectName(u"paramTable")
        self.paramTable.setMinimumSize(QSize(500, 0))
        self.paramTable.setFont(font2)
        self.paramTable.setStyleSheet(u"QTableWidget {\n"
"	color: white;\n"
"	background-color: rgb(36, 88, 104);\n"
"	border: 2px solid black\n"
"}\n"
"")

        self.verticalLayout_4.addWidget(self.paramTable)


        self.horizontalLayout.addWidget(self.paramSelect)

        self.drawingArea = QFrame(self.centralwidget)
        self.drawingArea.setObjectName(u"drawingArea")
        self.drawingArea.setStyleSheet(u"QFrame#drawingArea {\n"
"	border: 2px solid black;\n"
"	background-color: white\n"
"}")
        self.drawingArea.setFrameShape(QFrame.Shape.NoFrame)
        self.gridLayout_2 = QGridLayout(self.drawingArea)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.diagramLabel = QLabel(self.drawingArea)
        self.diagramLabel.setObjectName(u"diagramLabel")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Maximum)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.diagramLabel.sizePolicy().hasHeightForWidth())
        self.diagramLabel.setSizePolicy(sizePolicy1)

        self.gridLayout_2.addWidget(self.diagramLabel, 0, 0, 1, 1)


        self.horizontalLayout.addWidget(self.drawingArea)


        self.verticalLayout_3.addLayout(self.horizontalLayout)

        self.componentSelect = QWidget(self.centralwidget)
        self.componentSelect.setObjectName(u"componentSelect")
        self.componentSelect.setMinimumSize(QSize(0, 200))
        self.componentSelect.setMaximumSize(QSize(16777215, 200))
        self.componentSelect.setStyleSheet(u"QWidget#componentSelect {\n"
"	border: 2px solid black;\n"
"	background-color: \"#f0ffe4\"\n"
"}")
        self.gridLayout_3 = QGridLayout(self.componentSelect)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.widget = QWidget(self.componentSelect)
        self.widget.setObjectName(u"widget")
        self.widget.setStyleSheet(u"QWidget {\n"
"	color: white;\n"
"	background-color: rgb(36, 88, 104)\n"
"}")
        self.horizontalLayoutWidget = QWidget(self.widget)
        self.horizontalLayoutWidget.setObjectName(u"horizontalLayoutWidget")
        self.horizontalLayoutWidget.setGeometry(QRect(20, 10, 1238, 161))
        self.horizontalLayout_4 = QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.addSingleLinkBtn = QPushButton(self.horizontalLayoutWidget)
        self.addSingleLinkBtn.setObjectName(u"addSingleLinkBtn")
        self.addSingleLinkBtn.setMinimumSize(QSize(200, 150))
        self.addSingleLinkBtn.setFont(font2)
        self.addSingleLinkBtn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.addSingleLinkBtn.setStyleSheet(u"QPushButton {\n"
"	background-color: white;\n"
"	color: black;\n"
"	border-radius: 1px;\n"
"	border: 4px solid rgb(121, 121, 121);	\n"
"}\n"
"QPushButton:hover {\n"
"	background-color: rgb(207, 207, 207)\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"	background-color: rgb(121, 121, 121)\n"
"}")

        self.horizontalLayout_4.addWidget(self.addSingleLinkBtn)

        self.pushButton = QPushButton(self.horizontalLayoutWidget)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setMinimumSize(QSize(200, 150))
        self.pushButton.setMaximumSize(QSize(50, 16777215))
        self.pushButton.setFont(font2)
        self.pushButton.setStyleSheet(u"QPushButton {\n"
"	background-color: white;\n"
"	color: black;\n"
"	border-radius: 1px;\n"
"	border: 4px solid rgb(121, 121, 121);	\n"
"}\n"
"QPushButton:hover {\n"
"	background-color: rgb(207, 207, 207)\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"	background-color: rgb(121, 121, 121)\n"
"}")

        self.horizontalLayout_4.addWidget(self.pushButton)

        self.addRepChainBtn = QPushButton(self.horizontalLayoutWidget)
        self.addRepChainBtn.setObjectName(u"addRepChainBtn")
        self.addRepChainBtn.setMinimumSize(QSize(200, 150))
        self.addRepChainBtn.setFont(font2)
        self.addRepChainBtn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.addRepChainBtn.setStyleSheet(u"QPushButton {\n"
"	background-color: white;\n"
"	color: black;\n"
"	border-radius: 1px;\n"
"	border: 4px solid rgb(121, 121, 121);	\n"
"}\n"
"QPushButton:hover {\n"
"	background-color: rgb(207, 207, 207)\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"	background-color: rgb(121, 121, 121)\n"
"}")

        self.horizontalLayout_4.addWidget(self.addRepChainBtn)

        self.addTrustNodeBtn = QPushButton(self.horizontalLayoutWidget)
        self.addTrustNodeBtn.setObjectName(u"addTrustNodeBtn")
        self.addTrustNodeBtn.setMinimumSize(QSize(200, 150))
        self.addTrustNodeBtn.setFont(font2)
        self.addTrustNodeBtn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.addTrustNodeBtn.setStyleSheet(u"QPushButton {\n"
"	background-color: white;\n"
"	color: black;\n"
"	border-radius: 1px;\n"
"	border: 4px solid rgb(121, 121, 121);	\n"
"}\n"
"QPushButton:hover {\n"
"	background-color: rgb(207, 207, 207)\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"	background-color: rgb(121, 121, 121)\n"
"}")

        self.horizontalLayout_4.addWidget(self.addTrustNodeBtn)

        self.pushButton_2 = QPushButton(self.horizontalLayoutWidget)
        self.pushButton_2.setObjectName(u"pushButton_2")
        self.pushButton_2.setMinimumSize(QSize(200, 150))
        self.pushButton_2.setFont(font2)
        self.pushButton_2.setStyleSheet(u"QPushButton {\n"
"	background-color: white;\n"
"	color: black;\n"
"	border-radius: 1px;\n"
"	border: 4px solid rgb(121, 121, 121);	\n"
"}\n"
"QPushButton:hover {\n"
"	background-color: rgb(207, 207, 207)\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"	background-color: rgb(121, 121, 121)\n"
"}")

        self.horizontalLayout_4.addWidget(self.pushButton_2)

        self.pushButton_3 = QPushButton(self.horizontalLayoutWidget)
        self.pushButton_3.setObjectName(u"pushButton_3")
        self.pushButton_3.setMinimumSize(QSize(200, 150))
        self.pushButton_3.setFont(font2)
        self.pushButton_3.setStyleSheet(u"QPushButton {\n"
"	background-color: white;\n"
"	color: black;\n"
"	border-radius: 1px;\n"
"	border: 4px solid rgb(121, 121, 121);	\n"
"}\n"
"QPushButton:hover {\n"
"	background-color: rgb(207, 207, 207)\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"	background-color: rgb(121, 121, 121)\n"
"}")

        self.horizontalLayout_4.addWidget(self.pushButton_3)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_3)


        self.gridLayout_3.addWidget(self.widget, 0, 0, 1, 1)


        self.verticalLayout_3.addWidget(self.componentSelect)


        self.gridLayout.addLayout(self.verticalLayout_3, 1, 0, 1, 1)

        self.toolbar = QHBoxLayout()
        self.toolbar.setSpacing(6)
        self.toolbar.setObjectName(u"toolbar")
        self.toolbar.setSizeConstraint(QLayout.SizeConstraint.SetDefaultConstraint)
        self.toolbar.setContentsMargins(-1, -1, -1, 0)
        self.toolBar = QWidget(self.centralwidget)
        self.toolBar.setObjectName(u"toolBar")
        self.toolBar.setMaximumSize(QSize(16777215, 70))
        self.toolBar.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.toolBar.setStyleSheet(u".QPushButton {\n"
"	background-color: rgb(255, 255, 255);\n"
"	border-color: \"#000000\";\n"
"	color: \"#000000\"\n"
"}\n"
"QWidget{\n"
"	background-color: rgb(36, 88, 104)\n"
"}")
        self.horizontalLayout_3 = QHBoxLayout(self.toolBar)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.newBtn = QPushButton(self.toolBar)
        self.newBtn.setObjectName(u"newBtn")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.newBtn.sizePolicy().hasHeightForWidth())
        self.newBtn.setSizePolicy(sizePolicy2)
        self.newBtn.setMinimumSize(QSize(50, 50))
        self.newBtn.setMaximumSize(QSize(50, 50))
        font3 = QFont()
        font3.setFamilies([u"Roboto Medium"])
        self.newBtn.setFont(font3)
        self.newBtn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.newBtn.setStyleSheet(u"QPushButton {\n"
"	background-color: white;\n"
"	color: black;\n"
"	border-radius: 1px;\n"
"	border: 2px solid rgb(121, 121, 121);	\n"
"}\n"
"QPushButton:hover {\n"
"	background-color: rgb(207, 207, 207)\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"	background-color: rgb(121, 121, 121)\n"
"}")

        self.horizontalLayout_3.addWidget(self.newBtn)

        self.saveBtn = QPushButton(self.toolBar)
        self.saveBtn.setObjectName(u"saveBtn")
        self.saveBtn.setMinimumSize(QSize(50, 50))
        self.saveBtn.setMaximumSize(QSize(50, 50))
        self.saveBtn.setFont(font3)
        self.saveBtn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.saveBtn.setStyleSheet(u"QPushButton {\n"
"	background-color: white;\n"
"	color: black;\n"
"	border-radius: 1px;\n"
"	border: 2px solid rgb(121, 121, 121);	\n"
"}\n"
"QPushButton:hover {\n"
"	background-color: rgb(207, 207, 207)\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"	background-color: rgb(121, 121, 121)\n"
"}")

        self.horizontalLayout_3.addWidget(self.saveBtn)

        self.runBtn = QPushButton(self.toolBar)
        self.runBtn.setObjectName(u"runBtn")
        self.runBtn.setMinimumSize(QSize(50, 50))
        self.runBtn.setMaximumSize(QSize(50, 50))
        self.runBtn.setFont(font3)
        self.runBtn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.runBtn.setStyleSheet(u"QPushButton {\n"
"	background-color: white;\n"
"	color: black;\n"
"	border-radius: 1px;\n"
"	border: 2px solid rgb(121, 121, 121);	\n"
"}\n"
"QPushButton:hover {\n"
"	background-color: rgb(207, 207, 207)\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"	background-color: rgb(121, 121, 121)\n"
"}")

        self.horizontalLayout_3.addWidget(self.runBtn)

        self.stopBtn = QPushButton(self.toolBar)
        self.stopBtn.setObjectName(u"stopBtn")
        self.stopBtn.setMinimumSize(QSize(50, 50))
        self.stopBtn.setMaximumSize(QSize(50, 50))
        self.stopBtn.setFont(font3)
        self.stopBtn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.stopBtn.setStyleSheet(u"QPushButton {\n"
"	background-color: white;\n"
"	color: black;\n"
"	border-radius: 1px;\n"
"	border: 2px solid rgb(121, 121, 121);	\n"
"}\n"
"QPushButton:hover {\n"
"	background-color: rgb(207, 207, 207)\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"	background-color: rgb(121, 121, 121)\n"
"}")

        self.horizontalLayout_3.addWidget(self.stopBtn)

        self.closeBtn = QPushButton(self.toolBar)
        self.closeBtn.setObjectName(u"closeBtn")
        self.closeBtn.setMinimumSize(QSize(50, 50))
        self.closeBtn.setMaximumSize(QSize(50, 50))
        self.closeBtn.setFont(font3)
        self.closeBtn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.closeBtn.setStyleSheet(u"QPushButton {\n"
"	background-color: white;\n"
"	color: black;\n"
"	border-radius: 1px;\n"
"	border: 2px solid rgb(121, 121, 121);	\n"
"}\n"
"QPushButton:hover {\n"
"	background-color: rgb(207, 207, 207)\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"	background-color: rgb(121, 121, 121)\n"
"}")

        self.horizontalLayout_3.addWidget(self.closeBtn)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_2)

        self.exitBtn = QPushButton(self.toolBar)
        self.exitBtn.setObjectName(u"exitBtn")
        self.exitBtn.setMinimumSize(QSize(50, 50))
        self.exitBtn.setMaximumSize(QSize(50, 50))
        self.exitBtn.setFont(font3)
        self.exitBtn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.exitBtn.setStyleSheet(u"QPushButton {\n"
"	background-color: white;\n"
"	color: black;\n"
"	border-radius: 1px;\n"
"	border: 2px solid rgb(121, 121, 121);	\n"
"}\n"
"QPushButton:hover {\n"
"	background-color: rgb(207, 207, 207)\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"	background-color: rgb(121, 121, 121)\n"
"}")

        self.horizontalLayout_3.addWidget(self.exitBtn)


        self.toolbar.addWidget(self.toolBar)


        self.gridLayout.addLayout(self.toolbar, 0, 0, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1920, 21))
        font4 = QFont()
        font4.setFamilies([u"Segoe UI"])
        font4.setBold(False)
        self.menubar.setFont(font4)
        self.menubar.setCursor(QCursor(Qt.CursorShape.ArrowCursor))
        self.menubar.setDefaultUp(False)
        self.menuFile = QMenu(self.menubar)
        self.menuFile.setObjectName(u"menuFile")
        self.menuEdit = QMenu(self.menubar)
        self.menuEdit.setObjectName(u"menuEdit")
        self.menuPresets = QMenu(self.menubar)
        self.menuPresets.setObjectName(u"menuPresets")
        self.menuHelp = QMenu(self.menubar)
        self.menuHelp.setObjectName(u"menuHelp")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuEdit.menuAction())
        self.menubar.addAction(self.menuPresets.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())
        self.menuFile.addAction(self.actionNew)
        self.menuFile.addAction(self.actionSave)
        self.menuFile.addAction(self.actionExit)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"QUANTA", None))
        self.actionNew.setText(QCoreApplication.translate("MainWindow", u"New", None))
        self.actionSave.setText(QCoreApplication.translate("MainWindow", u"Save", None))
        self.actionetc.setText(QCoreApplication.translate("MainWindow", u"etc", None))
        self.actionExit.setText(QCoreApplication.translate("MainWindow", u"Exit", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Component params", None))
        ___qtreewidgetitem = self.componentTree.headerItem()
        ___qtreewidgetitem.setText(0, QCoreApplication.translate("MainWindow", u"Components", None));
        self.selectedComponentLabel.setText("")
        ___qtablewidgetitem = self.paramTable.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("MainWindow", u"Parameter", None));
        ___qtablewidgetitem1 = self.paramTable.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("MainWindow", u"Value", None));
        self.diagramLabel.setText("")
        self.addSingleLinkBtn.setText(QCoreApplication.translate("MainWindow", u"Single Link \n"
"(Midpoint source)", None))
        self.pushButton.setText(QCoreApplication.translate("MainWindow", u"Single Link \n"
"(Source at sender)", None))
        self.addRepChainBtn.setText(QCoreApplication.translate("MainWindow", u"Repeater Chain", None))
        self.addTrustNodeBtn.setText(QCoreApplication.translate("MainWindow", u"Trusted Node Chain", None))
        self.pushButton_2.setText(QCoreApplication.translate("MainWindow", u"Entanglement\n"
"Purification", None))
        self.pushButton_3.setText(QCoreApplication.translate("MainWindow", u"QKD Performance\n"
"Analysis", None))
        self.newBtn.setText(QCoreApplication.translate("MainWindow", u"New", None))
        self.saveBtn.setText(QCoreApplication.translate("MainWindow", u"Save", None))
        self.runBtn.setText(QCoreApplication.translate("MainWindow", u"Run", None))
        self.stopBtn.setText(QCoreApplication.translate("MainWindow", u"Stop", None))
        self.closeBtn.setText(QCoreApplication.translate("MainWindow", u"Close", None))
        self.exitBtn.setText(QCoreApplication.translate("MainWindow", u"Exit", None))
        self.menuFile.setTitle(QCoreApplication.translate("MainWindow", u"File", None))
        self.menuEdit.setTitle(QCoreApplication.translate("MainWindow", u"Edit", None))
        self.menuPresets.setTitle(QCoreApplication.translate("MainWindow", u"Presets", None))
        self.menuHelp.setTitle(QCoreApplication.translate("MainWindow", u"Help", None))
    # retranslateUi

