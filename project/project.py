import sys
from PyQt4.QtGui import *
from PyQt4.QtCore import *

# image path
imgDir = '../img/'
imgCell = imgDir + 'cell.jpg'
imgBlack = imgDir + 'black.jpg'
imgRed = imgDir + 'red.jpg'

class GridWindow(QWidget):
	
	def __init__(self, parent = None):
		super(GridWindow, self).__init__(parent)
		self.count = 0
		self.createWindows()
	
	def createWindows(self):
		self.createGridLayout()
		self.btnWidgetAndConnection()
		
		left_vl = QVBoxLayout()
		left_vl.addLayout(self.form_gl[0])
		left_vl.addLayout(self.form_gl[1])
		left_vl.addLayout(self.form_gl[2])
		left_vl.addLayout(self.form_gl[3])
		left_vl.addLayout(self.btn_hl)
		
		self.setLayout(left_vl)
	
	def createGridLayout(self):
		# global data
		self.QLabelList = []
		self.form_gl = []
		
		# grid layout for image
		for i in range(4):
			tmp = []
			self.form_gl.append(QGridLayout())
			self.form_gl[i].setSpacing(1)
			self.form_gl[i].setMargin(1)
			
			for y in range(6):
				for x in range(30):
					tmp.append(QLabel())
					pixmap = QPixmap(imgCell)
					tmp[len(tmp)-1].setPixmap(pixmap)
					tmp[len(tmp)-1].setScaledContents(True)
					self.form_gl[i].addWidget(tmp[len(tmp)-1], y, x)
			
			self.QLabelList.append(tmp)
	
	# horizontal layout for button
	def btnWidgetAndConnection(self):
		# global data
		self.btn_hl = QHBoxLayout()
		self.btn1 = QPushButton('black')
		self.btn2 = QPushButton('red')
		self.btn_hl.addWidget(self.btn1)
		self.btn_hl.addWidget(self.btn2)
		
		# button connection
		self.btn1.clicked.connect(self.btn1_changeGrid)
		self.btn2.clicked.connect(self.btn2_changeGrid)
	
	def btn1_changeGrid(self, text):
		if self.count < len(self.QLabelList[0]):
			pixmap = QPixmap(imgBlack)
			self.QLabelList[0][self.count].setPixmap(pixmap)
			self.count += 1
	
	def btn2_changeGrid(self, text):
		if self.count < len(self.QLabelList[0]):
			pixmap = QPixmap(imgRed)
			self.QLabelList[0][self.count].setPixmap(pixmap)
			self.count += 1
		
if __name__ == "__main__":
	app = QApplication(sys.argv)
	GridWindow = GridWindow()
	GridWindow.show()
	
	app.exec_()