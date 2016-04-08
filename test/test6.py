import sys
from PyQt4.QtGui import *
from PyQt4.QtCore import *

class GridWindow(QWidget):
	
	def __init__(self, parent = None):
		super(GridWindow, self).__init__(parent)
		self.QLabelList = []
		self.count = 0
		self.createLayout()
		self.btnConnection()
	
	def createLayout(self):
		gl = QGridLayout()
		gl.setSpacing(2)
		gl.setMargin(2)
		
		# grid layout for image
		for y in range(3):
			for x in range(5):
				self.QLabelList.append(QLabel())
				pixmap = QPixmap('../img/grey.jpg')
				self.QLabelList[len(self.QLabelList)-1].setPixmap(pixmap)
				self.QLabelList[len(self.QLabelList)-1].setScaledContents(True)
				gl.addWidget(self.QLabelList[len(self.QLabelList)-1], y, x)
		
		# horizontal layout for button
		hl = QHBoxLayout()
		self.btn1 = QPushButton('black')
		self.btn2 = QPushButton('red')
		hl.addWidget(self.btn1)
		hl.addWidget(self.btn2)
		
		#Frame button linetext
		tb = QFrame()
		tb.setStyleSheet('background-color: blue;')
		btn_tb = QPushButton(tb)
		
		vl = QVBoxLayout()
		#vl.addWidget(tb)
		vl.addLayout(gl)
		vl.addLayout(hl)
		
		#self.setLayout(vl)
		
		hl2 = QHBoxLayout()
		hl2.addLayout(vl)
		
		line = QFrame()
		line.setFrameShape(QFrame.VLine)
		line.setFrameShadow(QFrame.Sunken)
		line.setStyleSheet('background-color: blue;')
		hl2.addWidget(line)
		
		myToolbar = QToolBar()
		hl2.addWidget(myToolbar)
		
		extractAction = QAction(QIcon('../img/photo.jpg'), 'hahahaha', self)
		#extractAction.triggered.connect(exit())
		myToolbar.addAction(extractAction)
		
		extractAction2 = QAction(QIcon('photo.jpg'), 'hahahaha', self)
		#extractAction.triggered.connect(exit())
		myToolbar.addAction(extractAction2)
		
		
		
		self.setLayout(hl2)
		
		#self.addWidget(myToolbar)
		#QMainWindow.addToolBar( Qt.LeftToolBarArea , myToolbar )
	
	def btnConnection(self):
		self.btn1.clicked.connect(self.btn1_changeGrid)
		self.btn2.clicked.connect(self.btn2_changeGrid)
	
	def btn1_changeGrid(self, text):
		if self.count < 15:
			pixmap = QPixmap('../img/black.jpg')
			self.QLabelList[self.count].setPixmap(pixmap)
			#self.QLabelList[self.count].setScaledContents(True)
			#self.QLabelList[self.count].setText('1')
			self.count += 1
	
	def btn2_changeGrid(self, text):
		if self.count < 15:
			pixmap = QPixmap('../img/red.jpg')
			self.QLabelList[self.count].setPixmap(pixmap)
			#self.QLabelList[self.count].setText('2')
			self.count += 1
		
if __name__ == "__main__":
	app = QApplication(sys.argv)
	GridWindow = GridWindow()
	GridWindow.show()
	
	app.exec_()