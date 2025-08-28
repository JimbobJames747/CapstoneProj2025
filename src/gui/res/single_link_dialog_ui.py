# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'single_link_dialog.ui'
##
## Created by: Qt User Interface Compiler version 6.9.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QButtonGroup, QDialog, QGridLayout,
    QHBoxLayout, QLabel, QLineEdit, QPushButton,
    QRadioButton, QSizePolicy, QSpacerItem, QWidget)

class Ui_singleLinkDialog(object):
    def setupUi(self, singleLinkDialog):
        if not singleLinkDialog.objectName():
            singleLinkDialog.setObjectName(u"singleLinkDialog")
        singleLinkDialog.resize(766, 476)
        self.gridLayoutWidget = QWidget(singleLinkDialog)
        self.gridLayoutWidget.setObjectName(u"gridLayoutWidget")
        self.gridLayoutWidget.setGeometry(QRect(19, 19, 631, 326))
        self.gridLayout = QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.label_2 = QLabel(self.gridLayoutWidget)
        self.label_2.setObjectName(u"label_2")
        font = QFont()
        font.setPointSize(11)
        font.setBold(True)
        self.label_2.setFont(font)

        self.gridLayout.addWidget(self.label_2, 5, 0, 1, 1)

        self.srcRepRateRBtn = QRadioButton(self.gridLayoutWidget)
        self.buttonGroup = QButtonGroup(singleLinkDialog)
        self.buttonGroup.setObjectName(u"buttonGroup")
        self.buttonGroup.addButton(self.srcRepRateRBtn)
        self.srcRepRateRBtn.setObjectName(u"srcRepRateRBtn")

        self.gridLayout.addWidget(self.srcRepRateRBtn, 1, 0, 1, 1)

        self.linkLengthRBtn = QRadioButton(self.gridLayoutWidget)
        self.buttonGroup.addButton(self.linkLengthRBtn)
        self.linkLengthRBtn.setObjectName(u"linkLengthRBtn")

        self.gridLayout.addWidget(self.linkLengthRBtn, 4, 0, 1, 1)

        self.entFidRBtn = QRadioButton(self.gridLayoutWidget)
        self.buttonGroup_2 = QButtonGroup(singleLinkDialog)
        self.buttonGroup_2.setObjectName(u"buttonGroup_2")
        self.buttonGroup_2.addButton(self.entFidRBtn)
        self.entFidRBtn.setObjectName(u"entFidRBtn")

        self.gridLayout.addWidget(self.entFidRBtn, 8, 0, 1, 1)

        self.label = QLabel(self.gridLayoutWidget)
        self.label.setObjectName(u"label")
        self.label.setFont(font)

        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)

        self.entRateRBtn = QRadioButton(self.gridLayoutWidget)
        self.buttonGroup_2.addButton(self.entRateRBtn)
        self.entRateRBtn.setObjectName(u"entRateRBtn")

        self.gridLayout.addWidget(self.entRateRBtn, 7, 0, 1, 1)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.verticalSpacer, 10, 0, 1, 1)

        self.dcProbPerBinRBtn = QRadioButton(self.gridLayoutWidget)
        self.buttonGroup.addButton(self.dcProbPerBinRBtn)
        self.dcProbPerBinRBtn.setObjectName(u"dcProbPerBinRBtn")

        self.gridLayout.addWidget(self.dcProbPerBinRBtn, 2, 0, 1, 1)

        self.label_6 = QLabel(self.gridLayoutWidget)
        self.label_6.setObjectName(u"label_6")

        self.gridLayout.addWidget(self.label_6, 0, 2, 1, 1)

        self.label_5 = QLabel(self.gridLayoutWidget)
        self.label_5.setObjectName(u"label_5")

        self.gridLayout.addWidget(self.label_5, 0, 1, 1, 1)

        self.label_7 = QLabel(self.gridLayoutWidget)
        self.label_7.setObjectName(u"label_7")

        self.gridLayout.addWidget(self.label_7, 9, 0, 1, 1)

        self.detEffRBtn = QRadioButton(self.gridLayoutWidget)
        self.buttonGroup.addButton(self.detEffRBtn)
        self.detEffRBtn.setObjectName(u"detEffRBtn")

        self.gridLayout.addWidget(self.detEffRBtn, 3, 0, 1, 1)

        self.radioButton_9 = QRadioButton(self.gridLayoutWidget)
        self.buttonGroup_2.addButton(self.radioButton_9)
        self.radioButton_9.setObjectName(u"radioButton_9")

        self.gridLayout.addWidget(self.radioButton_9, 6, 0, 1, 1)

        self.nDataPoints = QLineEdit(self.gridLayoutWidget)
        self.nDataPoints.setObjectName(u"nDataPoints")

        self.gridLayout.addWidget(self.nDataPoints, 9, 1, 1, 1)

        self.srcRepStart = QLineEdit(self.gridLayoutWidget)
        self.srcRepStart.setObjectName(u"srcRepStart")

        self.gridLayout.addWidget(self.srcRepStart, 1, 1, 1, 1)

        self.dcProbStart = QLineEdit(self.gridLayoutWidget)
        self.dcProbStart.setObjectName(u"dcProbStart")

        self.gridLayout.addWidget(self.dcProbStart, 2, 1, 1, 1)

        self.detEffStart = QLineEdit(self.gridLayoutWidget)
        self.detEffStart.setObjectName(u"detEffStart")

        self.gridLayout.addWidget(self.detEffStart, 3, 1, 1, 1)

        self.linkLenStart = QLineEdit(self.gridLayoutWidget)
        self.linkLenStart.setObjectName(u"linkLenStart")

        self.gridLayout.addWidget(self.linkLenStart, 4, 1, 1, 1)

        self.srcRepEnd = QLineEdit(self.gridLayoutWidget)
        self.srcRepEnd.setObjectName(u"srcRepEnd")

        self.gridLayout.addWidget(self.srcRepEnd, 1, 2, 1, 1)

        self.dcProbEnd = QLineEdit(self.gridLayoutWidget)
        self.dcProbEnd.setObjectName(u"dcProbEnd")

        self.gridLayout.addWidget(self.dcProbEnd, 2, 2, 1, 1)

        self.detEffEnd = QLineEdit(self.gridLayoutWidget)
        self.detEffEnd.setObjectName(u"detEffEnd")

        self.gridLayout.addWidget(self.detEffEnd, 3, 2, 1, 1)

        self.linkLenEnd = QLineEdit(self.gridLayoutWidget)
        self.linkLenEnd.setObjectName(u"linkLenEnd")

        self.gridLayout.addWidget(self.linkLenEnd, 4, 2, 1, 1)

        self.horizontalLayoutWidget = QWidget(singleLinkDialog)
        self.horizontalLayoutWidget.setObjectName(u"horizontalLayoutWidget")
        self.horizontalLayoutWidget.setGeometry(QRect(390, 360, 291, 80))
        self.horizontalLayout = QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.okBtn = QPushButton(self.horizontalLayoutWidget)
        self.okBtn.setObjectName(u"okBtn")

        self.horizontalLayout.addWidget(self.okBtn)

        self.cancelBtn = QPushButton(self.horizontalLayoutWidget)
        self.cancelBtn.setObjectName(u"cancelBtn")

        self.horizontalLayout.addWidget(self.cancelBtn)


        self.retranslateUi(singleLinkDialog)

        QMetaObject.connectSlotsByName(singleLinkDialog)
    # setupUi

    def retranslateUi(self, singleLinkDialog):
        singleLinkDialog.setWindowTitle(QCoreApplication.translate("singleLinkDialog", u"Dialog", None))
        self.label_2.setText(QCoreApplication.translate("singleLinkDialog", u"Dependent Variables", None))
        self.srcRepRateRBtn.setText(QCoreApplication.translate("singleLinkDialog", u"Source repetition rate", None))
        self.linkLengthRBtn.setText(QCoreApplication.translate("singleLinkDialog", u"Link Length", None))
        self.entFidRBtn.setText(QCoreApplication.translate("singleLinkDialog", u"Entanglement fidelity", None))
        self.label.setText(QCoreApplication.translate("singleLinkDialog", u"Independent Variables", None))
        self.entRateRBtn.setText(QCoreApplication.translate("singleLinkDialog", u"Rate of entanglement distribution", None))
        self.dcProbPerBinRBtn.setText(QCoreApplication.translate("singleLinkDialog", u"Dark count probability/freq bin", None))
        self.label_6.setText(QCoreApplication.translate("singleLinkDialog", u"to", None))
        self.label_5.setText(QCoreApplication.translate("singleLinkDialog", u"From", None))
        self.label_7.setText(QCoreApplication.translate("singleLinkDialog", u"Number of data points", None))
        self.detEffRBtn.setText(QCoreApplication.translate("singleLinkDialog", u"Detector efficiency", None))
        self.radioButton_9.setText(QCoreApplication.translate("singleLinkDialog", u"Entanglement probability", None))
        self.okBtn.setText(QCoreApplication.translate("singleLinkDialog", u"OK", None))
        self.cancelBtn.setText(QCoreApplication.translate("singleLinkDialog", u"Cancel", None))
    # retranslateUi

