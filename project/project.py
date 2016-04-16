import sys
from PyQt4.QtGui import *
from PyQt4.QtCore import *

# image path
imgDir = 'img/'
imgCell = imgDir + 'cell.jpg'
imgBlack = imgDir + 'black.jpg'
imgRed = imgDir + 'red.jpg'
imgRedBtn = imgDir + 'red_btn.jpg'
imgGreenBtn = imgDir + 'green_btn.jpg'
imgBlueBtn = imgDir + 'blue_btn.jpg'

QTextCodec.setCodecForTr(QTextCodec.codecForName("utf8"))

def clickable(widget):
	class Filter(QObject):
		
		clicked = pyqtSignal()
		
		def eventFilter(self, obj, event):
			if obj  == widget:
				if event.type()  == QEvent.MouseButtonRelease:
					if obj.rect().contains(event.pos()):
						self.clicked.emit()
						# The developer can opt for .emit(obj) to get the object within the slot.
						return True
			
			return False
	
	filter = Filter(widget)
	widget.installEventFilter(filter)
	return filter.clicked
	
def pressed(widget):
	class Filter(QObject):
		
		clicked = pyqtSignal()
		
		def eventFilter(self, obj, event):
			if obj == widget:
				if event.type()  == QEvent.MouseButtonPress:
					if obj.rect().contains(event.pos()):
						self.clicked.emit()
						# The developer can opt for .emit(obj) to get the object within the slot.
						return True
			
			return False
	
	filter = Filter(widget)
	widget.installEventFilter(filter)
	return filter.clicked

class GridWindow(QWidget):
	def __init__(self, parent = None):
		super(GridWindow, self).__init__(parent)
		
		self.UI_hl = QHBoxLayout(self)
		self.left_qframe = QFrame(self)
		self.left_vl = QVBoxLayout(self.left_qframe)
		self.bet_qframe = QFrame(self)
		self.bet_vl = QVBoxLayout(self.bet_qframe)
		
		self.count = 0
		self.sizeWidth = 60
		self.sizeHeight = 25
		self.sizeWidth_btn = 70
		self.sizeHeight_btn = 22
		self.sizeWidth_qlineedit = 60
		self.sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
		
		self.UIcreate()
		self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
		self.setFixedSize(self.sizeHint())
		#print self.sizeHint()
		self.updateGeometry()
		self.vline.setFixedHeight(self.sizeHint().height()-50)
		
		self.lbar_btn[0].clicked.connect(self.btn_test)
	
	def initialGlobalAttribute(self):
		# initail global values of UIcreate
		#----------------------------------------------------
		self.UI_hl.setSpacing(15)
		
		# initail global values of UIcreate_GridLayout
		#----------------------------------------------------
		for i in range(4):
			self.grid_qframe[i].setStyleSheet('''.QFrame {background-color: gray;}''')
			
			self.grid_gl[i].setSpacing(1)
			self.grid_gl[i].setMargin(1)
		
		# initail global values of UIcreate_BarForGrid
		#----------------------------------------------------
		# bar's title
		#--------------------------
		for i in range(4):
			self.tbar_hl[i].setSpacing(1)
			self.tbar_hl[i].setMargin(1)
		
		self.tbar_qlabel[0].setText(self.tr('下局預測  大路'))
		self.tbar_qlabel[1].setText(self.tr('下局預測  眼路'))
		self.tbar_qlabel[2].setText(self.tr('下局預測  小路'))
		self.tbar_qlabel[3].setText(self.tr('下局預測  筆路'))
		
		# left bar
		#--------------------------
		for i in range(4):
			self.lbar_qframe[i].setStyleSheet('''.QFrame {background-color: red; border: 1px solid gray;}''')
			self.lbar_qframe[i].setSizePolicy(self.sizePolicy)
			
			self.lbar_hl[i].setSpacing(1)
			self.lbar_hl[i].setMargin(1)
			
			self.lbar_qlabel[i].setText(self.tr('莊'))
			self.lbar_qlabel[i].setStyleSheet('color: rgb(255, 255, 255);')
			self.lbar_qlabel[i].setAlignment(Qt.AlignCenter)
			self.lbar_qlabel[i].setSizePolicy(self.sizePolicy)
			self.lbar_qlabel[i].setFixedWidth(self.sizeWidth)
			
			self.lbar_btn[i].setText(self.tr('手動'))
			self.lbar_btn[i].setSizePolicy(self.sizePolicy)
			self.lbar_btn[i].setFixedWidth(self.sizeWidth_btn)
			self.lbar_btn[i].setFixedHeight(self.sizeHeight_btn)
			
			self.lbar_qlineedit[i].setFixedWidth(self.sizeWidth)
			self.lbar_qlineedit[i].setSizePolicy(self.sizePolicy)
		
		# right bar
		#--------------------------
		for i in range(4):
			self.rbar_qframe[i].setStyleSheet('''.QFrame {border: 1px solid gray;}''')
			self.rbar_qframe[i].setSizePolicy(self.sizePolicy)
			
			self.rbar_hl[i].setSpacing(1)
			self.rbar_hl[i].setMargin(1)
			
			self.rbar_qlabel1[i].setText(self.tr('小計 : '))
			self.rbar_qlabel1[i].setAlignment(Qt.AlignCenter)
			self.rbar_qlabel1[i].setSizePolicy(self.sizePolicy)
			self.rbar_qlabel1[i].setFixedWidth(self.sizeWidth)
			
			self.rbar_btn[i].setText(self.tr('切停'))
			self.rbar_btn[i].setSizePolicy(self.sizePolicy)
			self.rbar_btn[i].setFixedWidth(self.sizeWidth_btn)
			self.rbar_btn[i].setFixedHeight(self.sizeHeight_btn)
			
			self.rbar_qlabel2[i].setText(self.tr('合計 : '))
			self.rbar_qlabel2[i].setAlignment(Qt.AlignCenter)
			self.rbar_qlabel2[i].setSizePolicy(self.sizePolicy)
			self.rbar_qlabel2[i].setFixedWidth(self.sizeWidth)
		
		# initail global values of UIcreate_BetStatus
		#----------------------------------------------------
		self.bet_vl.setSpacing(25)
		
		# bet and print area
		#--------------------------
		self.bbet_qframe.setStyleSheet('''.QFrame {border: 1px solid gray;}''')
		self.bbet_qframe.setSizePolicy(self.sizePolicy)
		self.bbet_qframe.setFixedWidth(215)
		self.bbet_qframe.setFixedHeight(80)
		
		self.bbet_gl.setSpacing(1)
		self.bbet_gl.setMargin(1)
		
		self.bbet_btn1.setText(self.tr('本金'))
		self.bbet_btn1.setSizePolicy(self.sizePolicy)
		
		self.bbet_qlineedit.setFixedWidth(self.sizeWidth_qlineedit)
		
		self.bbet_btn2.setText(self.tr('列印'))
		self.bbet_btn2.setSizePolicy(self.sizePolicy)
		
		self.bbet_qlabel1.setText(self.tr('檯面數 : '))
		self.bbet_qlabel1.setSizePolicy(self.sizePolicy)
		
		self.bbet_qlabel2.setText(self.tr('轉碼 : '))
		self.bbet_qlabel2.setSizePolicy(self.sizePolicy)
		
		# next bet area
		#--------------------------
		self.nbet_qframe.setStyleSheet('''.QFrame {background-color: gray;} .QLabel {background-color: white;}''')
		#self.nbet_qframe.setStyleSheet('''.QLabel {border: 1px solid gray;}''')
		self.nbet_qframe.setSizePolicy(self.sizePolicy)
		self.nbet_qframe.setFixedWidth(215)
		self.nbet_qframe.setFixedHeight(55)
		
		self.nbet_gl.setSpacing(1)
		self.nbet_gl.setMargin(1)
		
		self.nbet_qlabel1.setText(self.tr('下局注碼'))
		self.nbet_qlabel1.setAlignment(Qt.AlignCenter)
		
		self.nbet_qlabel2.setText(self.tr('總計'))
		self.nbet_qlabel2.setAlignment(Qt.AlignCenter)
		
		self.nbet_qlabel3.setText(self.tr('莊'))
		self.nbet_qlabel3.setAlignment(Qt.AlignCenter)
		self.nbet_qlabel3.setStyleSheet('''.QLabel {color: red;}''')
		
		self.nbet_qlabel4.setText('99')
		self.nbet_qlabel4.setAlignment(Qt.AlignCenter)
		
		self.nbet_qlabel5.setText('108')
		self.nbet_qlabel5.setAlignment(Qt.AlignCenter)
		
		# bet inning count area
		#--------------------------
		self.ibet_qframe.setStyleSheet('''.QFrame {background-color: gray;} .QLabel {background-color: white;}''')
		self.ibet_qframe.setSizePolicy(self.sizePolicy)
		self.ibet_qframe.setFixedWidth(215)
		self.ibet_qframe.setFixedHeight(80)
		
		self.ibet_gl.setSpacing(1)
		self.ibet_gl.setMargin(1)
		
		self.ibet_qlabel2.setAlignment(Qt.AlignCenter)
		
		self.ibet_qlabel3.setText(self.tr('\n局'))
		self.ibet_qlabel3.setAlignment(Qt.AlignCenter)
		
		self.ibet_qlabel4.setAlignment(Qt.AlignCenter)
		
		self.ibet_qlabel5.setAlignment(Qt.AlignCenter)
		
		# bet push button area
		#--------------------------
		#self.pbet_qframe.setStyleSheet('''.QFrame {background-color: gray;} .QLabel {background-color: white;}''')
		self.pbet_qframe.setStyleSheet('''.QFrame {border: 1px solid gray;}''')
		self.pbet_qframe.setSizePolicy(self.sizePolicy)
		self.pbet_qframe.setFixedWidth(215)
		self.pbet_qframe.setFixedHeight(135)
		
		self.pbet_gl.setSpacing(1)
		self.pbet_gl.setMargin(1)
		
		pixmap = QPixmap(imgRedBtn)
		self.pbet_qlabel1.setPixmap(pixmap)
		self.pbet_qlabel1.setScaledContents(True)
		pixmap = QPixmap(imgGreenBtn)
		self.pbet_qlabel2.setPixmap(pixmap)
		self.pbet_qlabel2.setScaledContents(True)
		pixmap = QPixmap(imgBlueBtn)
		self.pbet_qlabel3.setPixmap(pixmap)
		self.pbet_qlabel3.setScaledContents(True)
		
		self.pbet_btn.setText(self.tr('返回'))
		#self.pbet_btn.setAlignment(Qt.AlignCenter)
		#self.pbet_btn.setSizePolicy(self.sizePolicy)
		self.pbet_btn.setFixedWidth(90)
		self.pbet_btn.setFixedHeight(30)
		
		
		# bet record area
		#--------------------------
		self.rbet_qframe.setStyleSheet('''.QLabel {background-color: white; border-top: 1px solid gray;
											border-left: 1px solid gray; border-right: 1px solid gray;}''')
		self.rbet_qframe.setSizePolicy(self.sizePolicy)
		
		self.rbet_vl.setSpacing(0)
		self.rbet_vl.setMargin(1)
		
		self.rbet_qlabel.setText(self.tr('投注紀錄'))
		self.rbet_qlabel.setAlignment(Qt.AlignCenter)
		self.rbet_qlabel.setFixedWidth(215)
		self.rbet_qlabel.setFixedHeight(30)
		
		#for i in range(30):
			#self.rbet_qlistwidget.addItem(str(i))
			
		self.rbet_qlistwidget.setFixedWidth(215)
		self.rbet_qlistwidget.setFixedHeight(330)
		
		# initail global values of UIcreate_numberInput
		#----------------------------------------------------
		self.binp_qframe.setStyleSheet('''.QFrame {background-color: rgb(218, 218, 218); border: 1px solid gray;}
											.QPushButton {background-color: white;}''')
		self.binp_qframe.setGeometry(QRect(565, 55, 147, 110))
		self.binp_qframe.setFrameShape(QFrame.StyledPanel)
		self.binp_qframe.setFrameShadow(QFrame.Raised)
		
		self.binp_gl.setSpacing(2)
		self.binp_gl.setMargin(2)
		
		self.binp_btn0.setText('0')
		self.binp_btn1.setText('1')
		self.binp_btn2.setText('2')
		self.binp_btn3.setText('3')
		self.binp_btn4.setText('4')
		self.binp_btn5.setText('5')
		self.binp_btn6.setText('6')
		self.binp_btn7.setText('7')
		self.binp_btn8.setText('8')
		self.binp_btn9.setText('9')
		self.binp_btn10.setText(self.tr('莊'))
		self.binp_btn11.setText(self.tr('閒'))
		
		self.binp_btn10.setStyleSheet('''.QPushButton {background-color: rgb(255, 47, 61); color: white;}''')
		self.binp_btn11.setStyleSheet('''.QPushButton {background-color: rgb(116, 106, 255); color: white;}''')
		
		self.binp_btnWidth = 40
		self.binp_btnHeight = 25
		self.binp_btn0.setFixedWidth(self.binp_btnWidth)
		self.binp_btn0.setFixedHeight(self.binp_btnHeight)
		self.binp_btn1.setFixedWidth(self.binp_btnWidth)
		self.binp_btn1.setFixedHeight(self.binp_btnHeight)
		self.binp_btn2.setFixedWidth(self.binp_btnWidth)
		self.binp_btn2.setFixedHeight(self.binp_btnHeight)
		self.binp_btn3.setFixedWidth(self.binp_btnWidth)
		self.binp_btn3.setFixedHeight(self.binp_btnHeight)
		self.binp_btn4.setFixedWidth(self.binp_btnWidth)
		self.binp_btn4.setFixedHeight(self.binp_btnHeight)
		self.binp_btn5.setFixedWidth(self.binp_btnWidth)
		self.binp_btn5.setFixedHeight(self.binp_btnHeight)
		self.binp_btn6.setFixedWidth(self.binp_btnWidth)
		self.binp_btn6.setFixedHeight(self.binp_btnHeight)
		self.binp_btn7.setFixedWidth(self.binp_btnWidth)
		self.binp_btn7.setFixedHeight(self.binp_btnHeight)
		self.binp_btn8.setFixedWidth(self.binp_btnWidth)
		self.binp_btn8.setFixedHeight(self.binp_btnHeight)
		self.binp_btn9.setFixedWidth(self.binp_btnWidth)
		self.binp_btn9.setFixedHeight(self.binp_btnHeight)
		self.binp_btn10.setFixedWidth(self.binp_btnWidth)
		self.binp_btn10.setFixedHeight(self.binp_btnHeight)
		self.binp_btn11.setFixedWidth(self.binp_btnWidth)
		self.binp_btn11.setFixedHeight(self.binp_btnHeight)
	
	def UIcreate(self):
		self.UIcreate_Grid()
		self.UI_create_Vline()
		self.UIcreate_BetStatus()
		self.UIcreate_numberInput()
		
		self.UI_hl.addWidget(self.left_qframe)
		self.UI_hl.addWidget(self.vline)
		self.UI_hl.addWidget(self.bet_qframe)
		
		self.initialGlobalAttribute()
		
		self.setLayout(self.UI_hl)
	
	def UI_create_Vline(self):
		self.vline = QFrame(self)
		self.vline.setFrameShape(QFrame.VLine)
		self.vline.setFrameShadow(QFrame.Sunken)
	
	def UIcreate_Grid(self):
		self.UIcreate_GridLayout()
		self.UIcreate_GridBar()
		
		for i in range(4):
			self.left_vl.addWidget(self.bar_qframe[i])
			self.left_vl.addWidget(self.grid_qframe[i])
		self.left_qframe.setLayout(self.left_vl)
	
	def UIcreate_GridBar(self):
		# full bar global data
		self.bar_qframe = []
		self.bar_hl = []
		for i in range(4):
			self.bar_qframe.append(QFrame(self.left_qframe))
			self.bar_hl.append(QHBoxLayout(self.bar_qframe[i]))
		
		# bar's title
		#----------------------------------------------------
		self.tbar_qframe = []
		self.tbar_hl = []
		self.tbar_qlabel = []
		
		for i in range(4):
			# initial title bar
			self.tbar_qframe.append(QFrame(self.bar_qframe[i]))
			self.tbar_hl.append(QHBoxLayout(self.tbar_qframe[i]))
			self.tbar_qlabel.append(QLabel(self.tbar_qframe[i]))
			
			# set relationship
			self.tbar_hl[i].addWidget(self.tbar_qlabel[i])
			self.tbar_qframe[i].setLayout(self.tbar_hl[i])
			self.bar_hl[i].addWidget(self.tbar_qframe[i])
			self.bar_hl[i].addWidget(QFrame())
		
		# left bar's global data
		#----------------------------------------------------
		self.lbar_qframe = []
		self.lbar_hl = []
		self.lbar_qlabel = []
		self.lbar_btn = []
		self.lbar_qlineedit = []
		
		for i in range(4):
     			# initial left bar
			self.lbar_qframe.append(QFrame(self.bar_qframe[i]))
			self.lbar_hl.append(QHBoxLayout(self.lbar_qframe[i]))
			self.lbar_qlabel.append(QLabel(self.lbar_qframe[i]))
			self.lbar_btn.append(QPushButton(self.lbar_qframe[i]))
			self.lbar_qlineedit.append(QLineEdit(self.lbar_qframe[i]))
			
			# set relationship
			self.lbar_hl[i].addWidget(self.lbar_qlabel[i])
			self.lbar_hl[i].addWidget(self.lbar_btn[i])
			self.lbar_hl[i].addWidget(self.lbar_qlineedit[i])
			self.lbar_qframe[i].setLayout(self.lbar_hl[i])
			self.bar_hl[i].addWidget(self.lbar_qframe[i])
		
		# right bar's global data
		#----------------------------------------------------
		self.rbar_qframe = []
		self.rbar_hl = []
		self.rbar_qlabel1 = []
		self.rbar_btn = []
		self.rbar_qlabel2 = []
		
		for i in range(4):
			# initial right bar
			self.rbar_qframe.append(QFrame(self.bar_qframe[i]))
			self.rbar_hl.append(QHBoxLayout(self.rbar_qframe[i]))
			self.rbar_qlabel1.append(QLabel(self.rbar_qframe[i]))
			self.rbar_btn.append(QPushButton(self.rbar_qframe[i]))
			self.rbar_qlabel2.append(QLabel(self.rbar_qframe[i]))
			
			# set relationship
			self.rbar_hl[i].addWidget(self.rbar_qlabel1[i])
			self.rbar_hl[i].addWidget(self.rbar_btn[i])
			self.rbar_hl[i].addWidget(self.rbar_qlabel2[i])
			self.rbar_qframe[i].setLayout(self.rbar_hl[i])
			self.bar_hl[i].addWidget(self.rbar_qframe[i])
	
	def UIcreate_GridLayout(self):
		# global data
		self.grid_qframe = []
		self.grid_gl = []
		self.grid_qlabelList = []
		
		# grid layout
		for i in range(4):
			# initial grid form
			self.grid_qframe.append(QFrame(self.left_qframe))
			self.grid_gl.append(QGridLayout(self.grid_qframe[i]))
			
			# initial each grid and set in gridlayout
			tmp = []
			for y in range(6):
				for x in range(30):
					tmp.append(QLabel(self.grid_qframe[i]))
					pixmap = QPixmap(imgCell)
					tmp[len(tmp)-1].setPixmap(pixmap)
					tmp[len(tmp)-1].setScaledContents(True)
					self.grid_gl[i].addWidget(tmp[len(tmp)-1], y, x)
			
			self.grid_qlabelList.append(tmp)
			
			# set relationship
			self.grid_qframe[i].setLayout(self.grid_gl[i])
	
	def UIcreate_BetStatus(self):
		self.bet_qframe.setLayout(self.bet_vl)
		
		# bet and print area
		#----------------------------------------------------
		# initial
		self.bbet_qframe = QFrame(self.bet_qframe)
		self.bbet_gl = QGridLayout(self.bbet_qframe)
		self.bbet_btn1 = QPushButton(self.bbet_qframe)
		self.bbet_qlineedit = QLineEdit(self.bbet_qframe)
		self.bbet_btn2 = QPushButton(self.bbet_qframe)
		self.bbet_qlabel1 = QLabel(self.bbet_qframe)
		self.bbet_qlabel2 = QLabel(self.bbet_qframe)
		
		# set relationship
		self.bbet_qframe.setLayout(self.bbet_gl)
		self.bbet_gl.addWidget(self.bbet_btn1, 0, 0)
		self.bbet_gl.addWidget(self.bbet_qlineedit, 0, 1)
		self.bbet_gl.addWidget(self.bbet_btn2, 0, 2)
		self.bbet_gl.addWidget(self.bbet_qlabel1, 1, 0, 1, 2)
		self.bbet_gl.addWidget(self.bbet_qlabel2, 1, 2)
		self.bet_vl.addWidget(self.bbet_qframe)
		
		# next bet area
		#----------------------------------------------------
		# initial
		self.nbet_qframe = QFrame(self.bet_qframe)
		self.nbet_gl = QGridLayout(self.nbet_qframe)
		self.nbet_qlabel1 = QLabel(self.nbet_qframe)
		self.nbet_qlabel2 = QLabel(self.nbet_qframe)
		self.nbet_qlabel3 = QLabel(self.nbet_qframe)
		self.nbet_qlabel4 = QLabel(self.nbet_qframe)
		self.nbet_qlabel5 = QLabel(self.nbet_qframe)
		
		# set relationship
		self.nbet_qframe.setLayout(self.nbet_gl)
		self.nbet_gl.addWidget(self.nbet_qlabel1, 0, 0, 1, 3)
		self.nbet_gl.addWidget(self.nbet_qlabel2, 0, 3)
		self.nbet_gl.addWidget(self.nbet_qlabel3, 1, 0, 1, 2)
		self.nbet_gl.addWidget(self.nbet_qlabel4, 1, 2)
		self.nbet_gl.addWidget(self.nbet_qlabel5, 1, 3)
		self.bet_vl.addWidget(self.nbet_qframe)
		
		# bet inning count area
		#----------------------------------------------------
		# initial
		self.ibet_qframe = QFrame(self.bet_qframe)
		self.ibet_gl = QGridLayout(self.ibet_qframe)
		self.ibet_qlabel1 = QLabel(self.ibet_qframe)
		self.ibet_qlabel2 = QLabel(self.ibet_qframe)
		self.ibet_qlabel3 = QLabel(self.ibet_qframe)
		self.ibet_qlabel4 = QLabel(self.ibet_qframe)
		self.ibet_qlabel5 = QLabel(self.ibet_qframe)
		
		# set relationship
		self.ibet_qframe.setLayout(self.ibet_gl)
		self.ibet_gl.addWidget(self.ibet_qlabel1, 0, 0, 3, 2)
		self.ibet_gl.addWidget(self.ibet_qlabel2, 0, 2)
		self.ibet_gl.addWidget(self.ibet_qlabel3, 0, 3, 3, 1)
		self.ibet_gl.addWidget(self.ibet_qlabel4, 1, 2)
		self.ibet_gl.addWidget(self.ibet_qlabel5, 2, 2)
		self.bet_vl.addWidget(self.ibet_qframe)
		
		# bet push button area
		#----------------------------------------------------
		# initial
		self.pbet_qframe = QFrame(self.bet_qframe)
		self.pbet_gl = QGridLayout(self.pbet_qframe)
		self.pbet_qlabel1 = QLabel(self.pbet_qframe)
		self.pbet_qlabel2 = QLabel(self.pbet_qframe)
		self.pbet_qlabel3 = QLabel(self.pbet_qframe)
		self.pbet_btn = QPushButton(self.pbet_qframe)
		
		# set relationship
		self.pbet_qframe.setLayout(self.pbet_gl)
		self.pbet_gl.addWidget(self.pbet_qlabel1, 0, 0, 2, 1)
		self.pbet_gl.addWidget(self.pbet_qlabel2, 0, 1, 2, 1)
		self.pbet_gl.addWidget(self.pbet_qlabel3, 0, 2, 2, 1)
		self.pbet_gl.addWidget(self.pbet_btn, 2, 0, 1, 3, Qt.AlignCenter)
		self.bet_vl.addWidget(self.pbet_qframe)
		
		# bet record area
		#----------------------------------------------------
		# initial
		self.rbet_qframe = QFrame(self.bet_qframe)
		self.rbet_vl = QVBoxLayout(self.rbet_qframe)
		self.rbet_qlabel = QLabel(self.rbet_qframe)
		self.rbet_qlistwidget = QListWidget(self.rbet_qframe)
		
		# set relationship
		self.rbet_qframe.setLayout(self.rbet_vl)
		self.rbet_vl.addWidget(self.rbet_qlabel)
		self.rbet_vl.addWidget(self.rbet_qlistwidget)
		self.bet_vl.addWidget(self.rbet_qframe)
	
	def UIcreate_numberInput(self):
		# initial
		self.binp_qframe = QFrame(self)
		self.binp_gl = QGridLayout(self.binp_qframe)
		self.binp_btn0 = QPushButton(self.binp_qframe)
		self.binp_btn1 = QPushButton(self.binp_qframe)
		self.binp_btn2 = QPushButton(self.binp_qframe)
		self.binp_btn3 = QPushButton(self.binp_qframe)
		self.binp_btn4 = QPushButton(self.binp_qframe)
		self.binp_btn5 = QPushButton(self.binp_qframe)
		self.binp_btn6 = QPushButton(self.binp_qframe)
		self.binp_btn7 = QPushButton(self.binp_qframe)
		self.binp_btn8 = QPushButton(self.binp_qframe)
		self.binp_btn9 = QPushButton(self.binp_qframe)
		self.binp_btn10 = QPushButton(self.binp_qframe)
		self.binp_btn11 = QPushButton(self.binp_qframe)
		
		# set relationship
		self.binp_qframe.setLayout(self.binp_gl)
		self.binp_gl.addWidget(self.binp_btn1, 0, 0)
		self.binp_gl.addWidget(self.binp_btn2, 0, 1)
		self.binp_gl.addWidget(self.binp_btn3, 0, 2)
		self.binp_gl.addWidget(self.binp_btn4, 1, 0)
		self.binp_gl.addWidget(self.binp_btn5, 1, 1)
		self.binp_gl.addWidget(self.binp_btn6, 1, 2)
		self.binp_gl.addWidget(self.binp_btn7, 2, 0)
		self.binp_gl.addWidget(self.binp_btn8, 2, 1)
		self.binp_gl.addWidget(self.binp_btn9, 2, 2)
		self.binp_gl.addWidget(self.binp_btn0, 3, 0)
		self.binp_gl.addWidget(self.binp_btn10, 3, 1)
		self.binp_gl.addWidget(self.binp_btn11, 3, 2)
	
	def btn_test(self):
		self.binp_qframe.show()
		#self.binp_qframe.close()
		
		#QObject.connect(self.lbar_btn[0], SIGNAL("clicked()"), self.test_frame.show)
		#QObject.connect(self.lbar_btn[1], SIGNAL("clicked()"), self.binp_qframe.close)
	
	def mousePressEvent(self, QMouseEvent):
		print QMouseEvent.pos()
	
	def mouseReleaseEvent(self, QMouseEvent):
		cursor = QCursor()
		print cursor.pos()

if __name__ == "__main__":
	app = QApplication(sys.argv)
	GridWindow = GridWindow()
	GridWindow.show()
	
	app.exec_()