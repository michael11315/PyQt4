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
		self.createBarForGrid()
		self.createbtnAndConnection()
		
		left_vl = QVBoxLayout()
		for i in range(4):
			left_vl.addLayout(self.bar_hl[i])
			left_vl.addLayout(self.grid_gl[i])
		
		left_vl.addLayout(self.btn_hl)
		
		self.setLayout(left_vl)
	
	def createGridLayout(self):
		# global data
		self.grid_qlabelList = []
		self.grid_gl = []
		
		# grid layout
		for i in range(4):
			tmp = []
			self.grid_gl.append(QGridLayout())
			self.grid_gl[i].setSpacing(1)
			self.grid_gl[i].setMargin(1)
			
			# initial each grid and put in layout
			for y in range(6):
				for x in range(30):
					tmp.append(QLabel())
					pixmap = QPixmap(imgCell)
					tmp[len(tmp)-1].setPixmap(pixmap)
					tmp[len(tmp)-1].setScaledContents(True)
					self.grid_gl[i].addWidget(tmp[len(tmp)-1], y, x)
			
			self.grid_qlabelList.append(tmp)
	
	def createBarForGrid(self):
		# global data
		self.bar_hl = []
		self.bar_qlabel = []
		self.bar_btn = []
		self.bar_qlineedit = []
		
		for i in range(4):
			self.bar_hl.append(QHBoxLayout())
			#self.bar_hl[i].setSpacing(1)
			#self.bar_hl[i].setMargin(1)
			self.bar_qlabel.append(QLabel())
			self.bar_btn.append(QPushButton())
			self.bar_qlineedit.append(QLineEdit())
			
			self.bar_hl[i].addWidget(self.bar_qlabel[i])
			self.bar_hl[i].addWidget(self.bar_btn[i])
			self.bar_hl[i].addWidget(self.bar_qlineedit[i])
	
	# horizontal layout for button
	def createbtnAndConnection(self):
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
		if self.count < len(self.grid_qlabelList[0]):
			pixmap = QPixmap(imgBlack)
			self.grid_qlabelList[0][self.count].setPixmap(pixmap)
			self.count += 1
	
	def btn2_changeGrid(self, text):
		if self.count < len(self.grid_qlabelList[0]):
			pixmap = QPixmap(imgRed)
			self.grid_qlabelList[0][self.count].setPixmap(pixmap)
			self.count += 1
		
if __name__ == "__main__":
	app = QApplication(sys.argv)
	GridWindow = GridWindow()
	GridWindow.show()
	
	app.exec_()