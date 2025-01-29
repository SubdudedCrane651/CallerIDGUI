# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'callerid.ui'
##
## Created by: Qt User Interface Compiler version 6.8.1
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
from PySide6.QtWidgets import (QApplication, QPlainTextEdit, QPushButton, QSizePolicy,
    QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(770, 622)
        icon = QIcon()
        icon.addFile(u"icon.ico", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        Form.setWindowIcon(icon)
        self.plainTextEdit = QPlainTextEdit(Form)
        self.plainTextEdit.setObjectName(u"plainTextEdit")
        self.plainTextEdit.setGeometry(QRect(0, 30, 781, 601))
        font = QFont()
        font.setFamilies([u"Arial"])
        font.setPointSize(16)
        font.setBold(True)
        self.plainTextEdit.setFont(font)
        self.Help_Button = QPushButton(Form)
        self.Help_Button.setObjectName(u"Help_Button")
        self.Help_Button.setGeometry(QRect(0, 0, 93, 31))
        self.LastCall_Button = QPushButton(Form)
        self.LastCall_Button.setObjectName(u"LastCall_Button")
        self.LastCall_Button.setGeometry(QRect(90, 0, 93, 31))
        self.Speak_Button = QPushButton(Form)
        self.Speak_Button.setObjectName(u"Speak_Button")
        self.Speak_Button.setGeometry(QRect(180, 0, 93, 31))
        self.Report_Button = QPushButton(Form)
        self.Report_Button.setObjectName(u"Report_Button")
        self.Report_Button.setGeometry(QRect(270, 0, 93, 31))
        self.Init_Button = QPushButton(Form)
        self.Init_Button.setObjectName(u"Init_Button")
        self.Init_Button.setGeometry(QRect(360, 0, 93, 31))

        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"CallerID", None))
        self.Help_Button.setText(QCoreApplication.translate("Form", u"Help", None))
        self.LastCall_Button.setText(QCoreApplication.translate("Form", u"LastCall", None))
        self.Speak_Button.setText(QCoreApplication.translate("Form", u"Speak", None))
        self.Report_Button.setText(QCoreApplication.translate("Form", u"Report", None))
        self.Init_Button.setText(QCoreApplication.translate("Form", u"Init", None))
    # retranslateUi

