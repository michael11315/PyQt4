from PyQt4 import QtGui, QtCore

class MyWindow(QtGui.QWidget):
    def __init__(self, parent=None):
        super(MyWindow, self).__init__(parent)

        self.region = QtGui.QRegion(QtCore.QRect(0, 0, 222, 222), QtGui.QRegion.Ellipse)
        self.setMask(self.region)

        self.palette = QtGui.QPalette()
        self.palette.setBrush(QtGui.QPalette.Background, QtGui.QColor('grey').dark(150))
        self.setPalette(self.palette)

        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)

        #self.label = QtGui.QLabel(self)
        #self.label.setText("A round widget!")
        #self.label.setStyleSheet("QLabel { background-color : lightblue; color : white; }")
        #self.label.setAlignment(QtCore.Qt.AlignCenter)
        
        self.label = QtGui.QPushButton(self)
        
        self.layout = QtGui.QHBoxLayout(self)
        self.layout.addWidget(self.label)

if __name__ == "__main__":
    import sys

    app = QtGui.QApplication(sys.argv)
    app.setApplicationName('MyWindow')

    main = MyWindow()
    main.resize(222, 222)
    main.show()

    sys.exit(app.exec_())