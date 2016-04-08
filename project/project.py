import sys
from PyQt4.QtGui import *
from PyQt4.QtCore import *

# image path
imgDir = '../img/'
imgCell = imgDir + 'cell.jpg'
imgBlack = imgDir + 'black.jpg'
imgRed = imgDir + 'red.jpg'

QTextCodec.setCodecForTr(QTextCodec.codecForName("utf8"))

class GridWindow(QWidget):
	
	def __init__(self, parent = None):
		super(GridWindow, self).__init__(parent)
		self.count = 0
		self.createWindows()
	
	def createWindows(self):
		self.createGridLayout()
		self.createBarForGrid()
		
		left_vl = QVBoxLayout()
		for i in range(4):
			left_vl.addLayout(self.bar_hl[i])
			left_vl.addWidget(self.grid_qframe[i])
		
		self.setLayout(left_vl)
	
	def createGridLayout(self):
		# global data
		self.grid_qframe = []
		self.grid_gl = []
		self.grid_qlabelList = []
		
		# grid layout
		for i in range(4):
			# initial grid form
			self.grid_qframe.append(QFrame())
			self.grid_gl.append(QGridLayout())
			
			# initial each grid and set in gridlayout
			tmp = []
			for y in range(6):
				for x in range(30):
					tmp.append(QLabel())
					pixmap = QPixmap(imgCell)
					tmp[len(tmp)-1].setPixmap(pixmap)
					tmp[len(tmp)-1].setScaledContents(True)
					self.grid_gl[i].addWidget(tmp[len(tmp)-1], y, x)
			
			self.grid_qlabelList.append(tmp)
			
			# set relationship
			self.grid_qframe[i].setLayout(self.grid_gl[i])
			
			# set attribute
			self.grid_gl[i].setSpacing(1)
			self.grid_gl[i].setMargin(1)
			self.grid_qframe[i].setStyleSheet('background-color: gray;')
	
	def createBarForGrid(self):
		# full bar global data
		self.bar_hl = []
		for i in range(4):
			self.bar_hl.append(QHBoxLayout())
		
		# bar's title
		#----------------------------------------------------
		self.tbar_qframe = []
		self.tbar_hl = []
		self.tbar_qlabel = []
		
		for i in range(4):
			# initial title bar
			self.tbar_qframe.append(QFrame())
			self.tbar_hl.append(QHBoxLayout())
			self.tbar_qlabel.append(QLabel())
			
			# set relationship
			self.tbar_hl[i].addWidget(self.tbar_qlabel[i])
			self.tbar_qframe[i].setLayout(self.tbar_hl[i])
			self.bar_hl[i].addWidget(self.tbar_qframe[i])
			self.bar_hl[i].addWidget(QFrame())
			
			# set attribute
			#self.tbar_qframe[i].setStyleSheet('''.QFrame {border: 1px solid gray;}''')
			self.tbar_hl[i].setSpacing(1)
			self.tbar_hl[i].setMargin(1)
			#self.tbar_qlabel[i].setAlignment(Qt.AlignCenter)
		
		self.tbar_qlabel[0].setText(self.tr('下局預測  大路'))
		self.tbar_qlabel[1].setText(self.tr('下局預測  眼路'))
		self.tbar_qlabel[2].setText(self.tr('下局預測  小路'))
		self.tbar_qlabel[3].setText(self.tr('下局預測  筆路'))
		
		# left bar's global data
		#----------------------------------------------------
		self.lbar_qframe = []
		self.lbar_hl = []
		self.lbar_qlabel = []
		self.lbar_btn = []
		self.lbar_qspinbox = []
		
		for i in range(4):
			# initial left bar
			self.lbar_qframe.append(QFrame())
			self.lbar_hl.append(QHBoxLayout())
			self.lbar_qlabel.append(QLabel(self.tr('莊')))
			self.lbar_btn.append(QPushButton(self.tr('手動')))
			self.lbar_qspinbox.append(QSpinBox())
			
			# set relationship
			self.lbar_hl[i].addWidget(self.lbar_qlabel[i])
			self.lbar_hl[i].addWidget(self.lbar_btn[i])
			self.lbar_hl[i].addWidget(self.lbar_qspinbox[i])
			self.lbar_qframe[i].setLayout(self.lbar_hl[i])
			self.bar_hl[i].addWidget(self.lbar_qframe[i])
			
			# set attribute
			self.lbar_qframe[i].setStyleSheet('''.QFrame {background-color: rgb(255, 0, 0); border: 1px solid gray;}''')
			self.lbar_hl[i].setSpacing(1)
			self.lbar_hl[i].setMargin(1)
			self.lbar_qlabel[i].setStyleSheet('color: rgb(255, 255, 255);')
			self.lbar_qlabel[i].setAlignment(Qt.AlignCenter)
		
		# right bar's global data
		#----------------------------------------------------
		self.rbar_qframe = []
		self.rbar_hl = []
		self.rbar_qlabel1 = []
		self.rbar_btn = []
		self.rbar_qlabel2 = []
		
		for i in range(4):
			# initial right bar
			self.rbar_qframe.append(QFrame())
			self.rbar_hl.append(QHBoxLayout())
			self.rbar_qlabel1.append(QLabel(self.tr('小計 : ')))
			self.rbar_btn.append(QPushButton(self.tr('切停')))
			self.rbar_qlabel2.append(QLabel(self.tr('合計 : ')))
			
			# set relationship
			self.rbar_hl[i].addWidget(self.rbar_qlabel1[i])
			self.rbar_hl[i].addWidget(self.rbar_btn[i])
			self.rbar_hl[i].addWidget(self.rbar_qlabel2[i])
			self.rbar_qframe[i].setLayout(self.rbar_hl[i])
			self.bar_hl[i].addWidget(self.rbar_qframe[i])
			
			# set attribute
			self.rbar_qframe[i].setStyleSheet('''.QFrame {border: 1px solid gray;}''')
			self.rbar_hl[i].setSpacing(1)
			self.rbar_hl[i].setMargin(1)
			self.rbar_qlabel1[i].setAlignment(Qt.AlignCenter)
			self.rbar_qlabel2[i].setAlignment(Qt.AlignCenter)
		
if __name__ == "__main__":
	app = QApplication(sys.argv)
	GridWindow = GridWindow()
	GridWindow.show()
	
	app.exec_()