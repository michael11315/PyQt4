import sys, os
from PyQt4.QtGui import *
from PyQt4.QtCore import *

class QWindow(QWidget):
    def __init__(self):
        super(QWindow, self).__init__()
        self.setWindowTitle('title')
        self.setGeometry(400,100,500,400)
        self.show()

class QLab(QLabel):
    def __init__(self, parent, text=''):
        QLabel.__init__(self, parent)
        self.setText(text)
        self.setFont(QFont('Arial', 16, 30, False))
        self.setStyleSheet(
           'background-color:black;' +
           'color:white;' +
           'border:brown;'+
           'text-align: right;')
        self.show()

class QBtn(QPushButton):
    def __init__(
        self, parent, text='click', enable=True):
        QPushButton.__init__(self, parent)
        self.setText(text)
        self.setFont(QFont('Arial', 16, 30, False))
        self.setEnabled(enable)
        self.setCursor(
            QCursor(Qt.PointingHandCursor))
        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)

    widget = QWindow()
    labelr = QLab(widget,'Hello world!')
    butn_1 = QBtn(widget,'enable')
    butn_2 = QBtn(widget,'enable')
    butn_3 = QBtn(widget,'disable',False)

    grid = QGridLayout()
    grid.setSpacing(1)
    grid.addWidget(butn_1,0,0)
    grid.addWidget(butn_2,1,0)
    grid.addWidget(butn_3,2,0)
    grid.addWidget(labelr,0,1,3,3)
    widget.setLayout(grid)

    sys.exit(app.exec_())