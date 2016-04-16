# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'UI2.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui
import sys

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(800, 600)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.horizontalLayoutWidget = QtGui.QWidget(self.centralwidget)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(190, 110, 461, 80))
        self.horizontalLayoutWidget.setObjectName(_fromUtf8("horizontalLayoutWidget"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.frame = QtGui.QFrame(self.horizontalLayoutWidget)
        self.frame.setStyleSheet(_fromUtf8("background-color: rgb(255, 0, 0);"))
        self.frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtGui.QFrame.Raised)
        self.frame.setObjectName(_fromUtf8("frame"))
        self.horizontalLayoutWidget_2 = QtGui.QWidget(self.frame)
        self.horizontalLayoutWidget_2.setGeometry(QtCore.QRect(79, 20, 321, 80))
        self.horizontalLayoutWidget_2.setObjectName(_fromUtf8("horizontalLayoutWidget_2"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.horizontalLayoutWidget_2)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.label = QtGui.QLabel(self.horizontalLayoutWidget_2)
        self.label.setStyleSheet(_fromUtf8("color: rgb(255, 255, 255);"))
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout_2.addWidget(self.label)
        self.pushButton = QtGui.QPushButton(self.horizontalLayoutWidget_2)
        self.pushButton.setStyleSheet(_fromUtf8("background-color: rgb(255, 255, 255);"))
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.horizontalLayout_2.addWidget(self.pushButton)
        self.spinBox = QtGui.QSpinBox(self.horizontalLayoutWidget_2)
        self.spinBox.setStyleSheet(_fromUtf8("background-color: rgb(255, 255, 255);"))
        self.spinBox.setObjectName(_fromUtf8("spinBox"))
        self.horizontalLayout_2.addWidget(self.spinBox)
        self.horizontalLayout.addWidget(self.frame)
        self.widget = QtGui.QWidget(self.centralwidget)
        self.widget.setGeometry(QtCore.QRect(170, 280, 481, 221))
        self.widget.setObjectName(_fromUtf8("widget"))
        self.frame_2 = QtGui.QFrame(self.widget)
        self.frame_2.setEnabled(True)
        self.frame_2.setGeometry(QtCore.QRect(140, 40, 251, 121))
        self.frame_2.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtGui.QFrame.Raised)
        self.frame_2.setLineWidth(0)
        self.frame_2.setObjectName(_fromUtf8("frame_2"))
        self.gridLayoutWidget = QtGui.QWidget(self.frame_2)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(9, 9, 239, 112))
        self.gridLayoutWidget.setObjectName(_fromUtf8("gridLayoutWidget"))
        self.gridLayout = QtGui.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.pushButton_4 = QtGui.QPushButton(self.gridLayoutWidget)
        self.pushButton_4.setObjectName(_fromUtf8("pushButton_4"))
        self.gridLayout.addWidget(self.pushButton_4, 0, 2, 1, 1)
        self.pushButton_2 = QtGui.QPushButton(self.gridLayoutWidget)
        self.pushButton_2.setObjectName(_fromUtf8("pushButton_2"))
        self.gridLayout.addWidget(self.pushButton_2, 0, 0, 1, 1)
        self.pushButton_9 = QtGui.QPushButton(self.gridLayoutWidget)
        self.pushButton_9.setObjectName(_fromUtf8("pushButton_9"))
        self.gridLayout.addWidget(self.pushButton_9, 2, 1, 1, 1)
        self.pushButton_3 = QtGui.QPushButton(self.gridLayoutWidget)
        self.pushButton_3.setObjectName(_fromUtf8("pushButton_3"))
        self.gridLayout.addWidget(self.pushButton_3, 0, 1, 1, 1)
        self.pushButton_5 = QtGui.QPushButton(self.gridLayoutWidget)
        self.pushButton_5.setObjectName(_fromUtf8("pushButton_5"))
        self.gridLayout.addWidget(self.pushButton_5, 1, 0, 1, 1)
        self.pushButton_6 = QtGui.QPushButton(self.gridLayoutWidget)
        self.pushButton_6.setObjectName(_fromUtf8("pushButton_6"))
        self.gridLayout.addWidget(self.pushButton_6, 1, 1, 1, 1)
        self.pushButton_7 = QtGui.QPushButton(self.gridLayoutWidget)
        self.pushButton_7.setObjectName(_fromUtf8("pushButton_7"))
        self.gridLayout.addWidget(self.pushButton_7, 1, 2, 1, 1)
        self.pushButton_8 = QtGui.QPushButton(self.gridLayoutWidget)
        self.pushButton_8.setObjectName(_fromUtf8("pushButton_8"))
        self.gridLayout.addWidget(self.pushButton_8, 2, 0, 1, 1)
        self.pushButton_10 = QtGui.QPushButton(self.gridLayoutWidget)
        self.pushButton_10.setObjectName(_fromUtf8("pushButton_10"))
        self.gridLayout.addWidget(self.pushButton_10, 2, 2, 1, 1)
        self.pushButton_11 = QtGui.QPushButton(self.gridLayoutWidget)
        self.pushButton_11.setObjectName(_fromUtf8("pushButton_11"))
        self.gridLayout.addWidget(self.pushButton_11, 3, 0, 1, 1)
        self.pushButton_12 = QtGui.QPushButton(self.gridLayoutWidget)
        self.pushButton_12.setObjectName(_fromUtf8("pushButton_12"))
        self.gridLayout.addWidget(self.pushButton_12, 3, 1, 1, 1)
        self.pushButton_13 = QtGui.QPushButton(self.gridLayoutWidget)
        self.pushButton_13.setObjectName(_fromUtf8("pushButton_13"))
        self.gridLayout.addWidget(self.pushButton_13, 3, 2, 1, 1)
        self.pushButton_14 = QtGui.QPushButton(self.widget)
        self.pushButton_14.setGeometry(QtCore.QRect(170, 10, 75, 23))
        self.pushButton_14.setObjectName(_fromUtf8("pushButton_14"))
        self.pushButton_15 = QtGui.QPushButton(self.widget)
        self.pushButton_15.setGeometry(QtCore.QRect(250, 10, 75, 23))
        self.pushButton_15.setObjectName(_fromUtf8("pushButton_15"))
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 22))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QObject.connect(self.pushButton_14, QtCore.SIGNAL(_fromUtf8("clicked()")), self.frame_2.show)
        QtCore.QObject.connect(self.pushButton_15, QtCore.SIGNAL(_fromUtf8("clicked()")), self.frame_2.close)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.label.setText(_translate("MainWindow", "TextLabel", None))
        self.pushButton.setText(_translate("MainWindow", "PushButton", None))
        self.pushButton_4.setText(_translate("MainWindow", "PushButton", None))
        self.pushButton_2.setText(_translate("MainWindow", "PushButton", None))
        self.pushButton_9.setText(_translate("MainWindow", "PushButton", None))
        self.pushButton_3.setText(_translate("MainWindow", "PushButton", None))
        self.pushButton_5.setText(_translate("MainWindow", "PushButton", None))
        self.pushButton_6.setText(_translate("MainWindow", "PushButton", None))
        self.pushButton_7.setText(_translate("MainWindow", "PushButton", None))
        self.pushButton_8.setText(_translate("MainWindow", "PushButton", None))
        self.pushButton_10.setText(_translate("MainWindow", "PushButton", None))
        self.pushButton_11.setText(_translate("MainWindow", "PushButton", None))
        self.pushButton_12.setText(_translate("MainWindow", "PushButton", None))
        self.pushButton_13.setText(_translate("MainWindow", "PushButton", None))
        self.pushButton_14.setText(_translate("MainWindow", "PushButton", None))
        self.pushButton_15.setText(_translate("MainWindow", "PushButton", None))


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    Ui_MainWindow = Ui_MainWindow()
    Ui_MainWindow.show()
    
    app.exec_()