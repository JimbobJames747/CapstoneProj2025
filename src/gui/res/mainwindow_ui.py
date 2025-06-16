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
        font1.setFamilies([u"Verdana"])
        font1.setPointSize(12)
        self.label.setFont(font1)
        self.label.setStyleSheet(u"")

        self.verticalLayout_4.addWidget(self.label)

        self.treeWidget = QTreeWidget(self.paramSelect)
        __qtreewidgetitem = QTreeWidgetItem()
        __qtreewidgetitem.setFont(0, font1);
        __qtreewidgetitem.setBackground(0, QColor(36, 88, 104));
        self.treeWidget.setHeaderItem(__qtreewidgetitem)
        __qtreewidgetitem1 = QTreeWidgetItem(self.treeWidget)
        QTreeWidgetItem(__qtreewidgetitem1)
        __qtreewidgetitem2 = QTreeWidgetItem(self.treeWidget)
        QTreeWidgetItem(__qtreewidgetitem2)
        __qtreewidgetitem3 = QTreeWidgetItem(self.treeWidget)
        __qtreewidgetitem4 = QTreeWidgetItem(__qtreewidgetitem3)
        QTreeWidgetItem(__qtreewidgetitem4)
        self.treeWidget.setObjectName(u"treeWidget")
        font2 = QFont()
        font2.setFamilies([u"Verdana"])
        font2.setPointSize(10)
        self.treeWidget.setFont(font2)
        self.treeWidget.viewport().setProperty(u"cursor", QCursor(Qt.CursorShape.PointingHandCursor))
        self.treeWidget.setStyleSheet(u"QTreeWidget {\n"
"	color: white;\n"
"	border: 2px solid black;\n"
"	background-color: rgb(36, 88, 104)\n"
"}")

        self.verticalLayout_4.addWidget(self.treeWidget)

        self.label_5 = QLabel(self.paramSelect)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setFont(font1)

        self.verticalLayout_4.addWidget(self.label_5)

        self.tableWidget = QTableWidget(self.paramSelect)
        if (self.tableWidget.columnCount() < 2):
            self.tableWidget.setColumnCount(2)
        __qtablewidgetitem = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        self.tableWidget.setObjectName(u"tableWidget")
        self.tableWidget.setStyleSheet(u"QTableWidget {\n"
"	color: black;\n"
"	background-color: rgb(36, 88, 104)\n"
"}\n"
"QWidget#tableWidget {\n"
"	border: 2px solid black\n"
"}")

        self.verticalLayout_4.addWidget(self.tableWidget)


        self.horizontalLayout.addWidget(self.paramSelect)

        self.drawingArea = QFrame(self.centralwidget)
        self.drawingArea.setObjectName(u"drawingArea")
        self.drawingArea.setStyleSheet(u"QFrame#drawingArea {\n"
"	border: 2px solid black\n"
"}")
        self.drawingArea.setFrameShape(QFrame.Shape.StyledPanel)
        self.drawingArea.setFrameShadow(QFrame.Shadow.Raised)
        self.label_2 = QLabel(self.drawingArea)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(120, 40, 71, 31))

        self.horizontalLayout.addWidget(self.drawingArea)

        self.resultsArea = QWidget(self.centralwidget)
        self.resultsArea.setObjectName(u"resultsArea")
        self.resultsArea.setMaximumSize(QSize(400, 16777215))
        self.resultsArea.setCursor(QCursor(Qt.CursorShape.ArrowCursor))
        self.resultsArea.setStyleSheet(u"QWidget#resultsArea {\n"
"	border: 2px solid black;\n"
"	background-color: \"#f0ffe4\"\n"
"}")
        self.verticalLayout = QVBoxLayout(self.resultsArea)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.tabWidget_2 = QTabWidget(self.resultsArea)
        self.tabWidget_2.setObjectName(u"tabWidget_2")
        self.tabWidget_2.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.tabWidget_2.setStyleSheet(u"QWidget {\n"
"	background-color: rgb(36, 88, 104);\n"
"	color: white\n"
"}")
        self.tabWidget_2.setTabShape(QTabWidget.TabShape.Rounded)
        self.tab_3 = QWidget()
        self.tab_3.setObjectName(u"tab_3")
        self.tab_3.setCursor(QCursor(Qt.CursorShape.ArrowCursor))
        self.tabWidget_2.addTab(self.tab_3, "")
        self.tab_4 = QWidget()
        self.tab_4.setObjectName(u"tab_4")
        self.tab_4.setCursor(QCursor(Qt.CursorShape.ArrowCursor))
        self.tabWidget_2.addTab(self.tab_4, "")

        self.verticalLayout.addWidget(self.tabWidget_2)


        self.horizontalLayout.addWidget(self.resultsArea)


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
        self.tabWidget = QTabWidget(self.componentSelect)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tabWidget.setMinimumSize(QSize(0, 160))
        self.tabWidget.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.tabWidget.setStyleSheet(u"QWidget {\n"
"	background-color: rgb(36, 88, 104);\n"
"	color: white\n"
"}")
        self.tabWidget.setTabShape(QTabWidget.TabShape.Rounded)
        self.tab = QWidget()
        self.tab.setObjectName(u"tab")
        self.tab.setCursor(QCursor(Qt.CursorShape.ArrowCursor))
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QWidget()
        self.tab_2.setObjectName(u"tab_2")
        self.tabWidget.addTab(self.tab_2, "")

        self.gridLayout_3.addWidget(self.tabWidget, 0, 0, 1, 1)


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
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.newBtn.sizePolicy().hasHeightForWidth())
        self.newBtn.setSizePolicy(sizePolicy1)
        self.newBtn.setMinimumSize(QSize(50, 50))
        self.newBtn.setMaximumSize(QSize(50, 16777215))
        self.newBtn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.horizontalLayout_3.addWidget(self.newBtn)

        self.saveBtn = QPushButton(self.toolBar)
        self.saveBtn.setObjectName(u"saveBtn")
        self.saveBtn.setMinimumSize(QSize(50, 50))
        self.saveBtn.setMaximumSize(QSize(50, 50))
        self.saveBtn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.horizontalLayout_3.addWidget(self.saveBtn)

        self.runBtn = QPushButton(self.toolBar)
        self.runBtn.setObjectName(u"runBtn")
        self.runBtn.setMaximumSize(QSize(50, 50))
        self.runBtn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.horizontalLayout_3.addWidget(self.runBtn)

        self.stopBtn = QPushButton(self.toolBar)
        self.stopBtn.setObjectName(u"stopBtn")
        self.stopBtn.setMinimumSize(QSize(50, 50))
        self.stopBtn.setMaximumSize(QSize(50, 50))
        self.stopBtn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.horizontalLayout_3.addWidget(self.stopBtn)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer)

        self.exitBtn = QPushButton(self.toolBar)
        self.exitBtn.setObjectName(u"exitBtn")
        self.exitBtn.setMaximumSize(QSize(50, 50))
        self.exitBtn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.horizontalLayout_3.addWidget(self.exitBtn)


        self.toolbar.addWidget(self.toolBar)


        self.gridLayout.addLayout(self.toolbar, 0, 0, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1920, 21))
        font3 = QFont()
        font3.setFamilies([u"Segoe UI"])
        font3.setBold(False)
        self.menubar.setFont(font3)
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

        self.tabWidget_2.setCurrentIndex(1)
        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Simulaysh", None))
        self.actionNew.setText(QCoreApplication.translate("MainWindow", u"New", None))
        self.actionSave.setText(QCoreApplication.translate("MainWindow", u"Save", None))
        self.actionetc.setText(QCoreApplication.translate("MainWindow", u"etc", None))
        self.actionExit.setText(QCoreApplication.translate("MainWindow", u"Exit", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Component params", None))
        ___qtreewidgetitem = self.treeWidget.headerItem()
        ___qtreewidgetitem.setText(0, QCoreApplication.translate("MainWindow", u"Network", None));

        __sortingEnabled = self.treeWidget.isSortingEnabled()
        self.treeWidget.setSortingEnabled(False)
        ___qtreewidgetitem1 = self.treeWidget.topLevelItem(0)
        ___qtreewidgetitem1.setText(0, QCoreApplication.translate("MainWindow", u"test", None));
        ___qtreewidgetitem2 = ___qtreewidgetitem1.child(0)
        ___qtreewidgetitem2.setText(0, QCoreApplication.translate("MainWindow", u"sub", None));
        ___qtreewidgetitem3 = self.treeWidget.topLevelItem(1)
        ___qtreewidgetitem3.setText(0, QCoreApplication.translate("MainWindow", u"test2", None));
        ___qtreewidgetitem4 = ___qtreewidgetitem3.child(0)
        ___qtreewidgetitem4.setText(0, QCoreApplication.translate("MainWindow", u"sub2", None));
        ___qtreewidgetitem5 = self.treeWidget.topLevelItem(2)
        ___qtreewidgetitem5.setText(0, QCoreApplication.translate("MainWindow", u"test3", None));
        ___qtreewidgetitem6 = ___qtreewidgetitem5.child(0)
        ___qtreewidgetitem6.setText(0, QCoreApplication.translate("MainWindow", u"sub3", None));
        ___qtreewidgetitem7 = ___qtreewidgetitem6.child(0)
        ___qtreewidgetitem7.setText(0, QCoreApplication.translate("MainWindow", u"subsub3", None));
        self.treeWidget.setSortingEnabled(__sortingEnabled)

        self.label_5.setText(QCoreApplication.translate("MainWindow", u"(Selected component)", None))
        ___qtablewidgetitem = self.tableWidget.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("MainWindow", u"param", None));
        ___qtablewidgetitem1 = self.tableWidget.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("MainWindow", u"value", None));
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Drawing area", None))
        self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.tab_3), QCoreApplication.translate("MainWindow", u"Results", None))
        self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.tab_4), QCoreApplication.translate("MainWindow", u"Sweeps", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QCoreApplication.translate("MainWindow", u"Components", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), QCoreApplication.translate("MainWindow", u"Presets", None))
        self.newBtn.setText(QCoreApplication.translate("MainWindow", u"New", None))
        self.saveBtn.setText(QCoreApplication.translate("MainWindow", u"Save", None))
        self.runBtn.setText(QCoreApplication.translate("MainWindow", u"Run", None))
        self.stopBtn.setText(QCoreApplication.translate("MainWindow", u"Stop", None))
        self.exitBtn.setText(QCoreApplication.translate("MainWindow", u"Exit", None))
        self.menuFile.setTitle(QCoreApplication.translate("MainWindow", u"File", None))
        self.menuEdit.setTitle(QCoreApplication.translate("MainWindow", u"Edit", None))
        self.menuPresets.setTitle(QCoreApplication.translate("MainWindow", u"Presets", None))
        self.menuHelp.setTitle(QCoreApplication.translate("MainWindow", u"Help", None))
    # retranslateUi

