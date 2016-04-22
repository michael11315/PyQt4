import sys
from PyQt4.QtGui import *
from PyQt4.QtCore import *

QTextCodec.setCodecForTr(QTextCodec.codecForName("utf8"))

# image path
imgDir = 'img/'
imgCell = imgDir + 'cell.jpg'
imgBlack = imgDir + 'black.jpg'
imgRed = imgDir + 'red.jpg'
imgRedBtn = imgDir + 'red_btn.png'
imgGreenBtn = imgDir + 'green_btn.png'
imgBlueBtn = imgDir + 'blue_btn.png'
imgBigRedCir = imgDir + 'big_red_cir.png'
imgBigBlueCir = imgDir + 'big_blue_cir.png'
imgBigRedCirGreen = imgDir + 'big_red_cir_green.png'
imgBigBlueCirGreen = imgDir + 'big_blue_cir_green.png'
imgEyeRedCir = imgDir + 'eye_red_cir.png'
imgEyeBlueCir = imgDir + 'eye_blue_cir.png'
imgSmaRedCir = imgDir + 'sma_red_cir.png'
imgSmaBlueCir = imgDir + 'sma_blue_cir.png'
imgPenRedCir = imgDir + 'pen_red_cir.png'
imgPenBlueCir = imgDir + 'pen_blue_cir.png'

# value for bet button
Banker = 0
Player = 1
Tie = 2

Red = 0
Blue = 1

class betRecord():
	def __init__(self):
		self.recordAll = []
		self.recordBig = []
		self.recordEye = []
		self.recordSma = []
		self.recordPen = []
		
		# count continuous times for Eye, Sma, Pen
		self.countBig = [0, 0, 0, 0]
		
		self.mapBig = []
		self.mapEye = []
		self.mapSma = []
		self.mapPen = []
		for row in range(6):
			tmp = []
			for col in range(30):
				tmp.append(-1)
			tmp2 = []
			for col in range(30):
				tmp2.append(-1)
			tmp3 = []
			for col in range(30):
				tmp3.append(-1)
			tmp4 = []
			for col in range(30):
				tmp4.append(-1)
				
			self.mapBig.append(tmp)
			self.mapEye.append(tmp2)
			self.mapSma.append(tmp3)
			self.mapPen.append(tmp4)
		
		self.imgPath = []
		# imgPath[0] -> imgBig
		self.imgPath.append([imgBigRedCir, imgBigBlueCir, (imgBigRedCirGreen, imgBigBlueCirGreen)])
		# imgPath[1] -> imgEye
		self.imgPath.append([imgEyeRedCir, imgEyeBlueCir])
		# imgPath[2] -> imgSma
		self.imgPath.append([imgSmaRedCir, imgSmaBlueCir])
		# imgPath[3] -> imgPen
		self.imgPath.append([imgPenRedCir, imgPenBlueCir])
	
	def bet(self, winner):
		if winner != Tie:
			ret = self.findPos(winner)
			if ret.get('status') == 0:
				Big = ret.get('Big')
				Eye = ret.get('Eye')
				Sma = ret.get('Sma')
				Pen = ret.get('Pen')
				self.recordBig.append(Big)
				self.recordEye.append(Eye)
				self.recordSma.append(Sma)
				self.recordPen.append(Pen)
				self.mapBig[Big[0]][Big[1]] = Big[2]
				self.mapEye[Eye[0]][Eye[1]] = Eye[2]
				self.mapSma[Sma[0]][Sma[1]] = Sma[2]
				self.mapPen[Pen[0]][Pen[1]] = Pen[2]
			
			self.recordAll.append(winner)
			#print 'record', self.recordAll
			#print self.countBig
			
			return {'status': 0, 'Big': Big, 'Eye': Eye, 'Sma': Sma, 'Pen': Pen}
		else:
			self.countBig[0] -= 1
			pass
		
		return {'status': -1}
	
	def findPos(self, winner):
		Big, Eye, Sma, Pen = (-1, -1, -1), (-1, -1, -1), (-1, -1, -1), (-1, -1, -1)
		
		if len(self.recordAll) == 0:
			Big = (0, 0, winner)
			self.countBig[0] += 1
			return {'status': 0, 'Big': Big, 'Eye': Eye, 'Sma': Sma, 'Pen': Pen}
		
		lastBet = self.recordBig[len(self.recordBig)-1]
		jump = False
		if lastBet[2] == winner:
			Big = self.PosNext(self.mapBig, lastBet[0], lastBet[1], lastBet[2])
			self.countBig[0] += 1
		else:
			Big = self.PosChangeCol(self.mapBig, lastBet[2])
			jump = True
		
		lastBet = self.recordEye[len(self.recordEye)-1]
		if lastBet[0] != -1 or lastBet[1] != -1 or self.countBig[1] != 0:
			if lastBet[0] != -1 or lastBet[1] != -1 or (self.countBig[0] != 1 or jump):
				imgColor = self.findColor(jump, self.countBig[0], self.countBig[1])
				
				if lastBet[2] == -1:
					Eye = self.PosNext(self.mapEye, lastBet[0], lastBet[1], imgColor)
				elif lastBet[2] == imgColor:
					Eye = self.PosNext(self.mapEye, lastBet[0], lastBet[1], lastBet[2])
				else:
					Eye = self.PosChangeCol(self.mapEye, lastBet[2])
		
		lastBet = self.recordSma[len(self.recordSma)-1]
		if lastBet[0] != -1 or lastBet[1] != -1 or self.countBig[2] != 0:
			if lastBet[0] != -1 or lastBet[1] != -1 or (self.countBig[0] != 1 or jump):
				imgColor = self.findColor(jump, self.countBig[0], self.countBig[2])
				
				if lastBet[2] == -1:
					Sma = self.PosNext(self.mapSma, lastBet[0], lastBet[1], imgColor)
				elif lastBet[2] == imgColor:
					Sma = self.PosNext(self.mapSma, lastBet[0], lastBet[1], lastBet[2])
				else:
					Sma = self.PosChangeCol(self.mapSma, lastBet[2])
		
		lastBet = self.recordPen[len(self.recordPen)-1]
		if lastBet[0] != -1 or lastBet[1] != -1 or self.countBig[3] != 0:
			if lastBet[0] != -1 or lastBet[1] != -1 or (self.countBig[0] != 1 or jump):
				imgColor = self.findColor(jump, self.countBig[0], self.countBig[3])
				
				if lastBet[2] == -1:
					Pen = self.PosNext(self.mapPen, lastBet[0], lastBet[1], imgColor)
				elif lastBet[2] == imgColor:
					Pen = self.PosNext(self.mapPen, lastBet[0], lastBet[1], lastBet[2])
				else:
					Pen = self.PosChangeCol(self.mapPen, lastBet[2])
		
		if jump:
			self.countBig[3] = self.countBig[2]
			self.countBig[2] = self.countBig[1]
			self.countBig[1] = self.countBig[0]
			self.countBig[0] = 1
		
		#print Big, Eye, Sma, Pen
		return {'status': 0, 'Big': Big, 'Eye': Eye, 'Sma': Sma, 'Pen': Pen}
	
	def findColor(self, jump, countBig_now, countBig_old):
		if jump:
			if countBig_now == countBig_old:
				return Red
			else:
				return Blue
		else:
			if countBig_now <= countBig_old:
				return Red
			elif countBig_now == countBig_old+1:
				return Blue
			else:
				return Red
	
	def findPosOther(self, map, lastBet_row, lastBet_col, lastBet_img, countBig_now, countBig_old):
		if lastBet_row == -1 and lastBet_col == -1 and countBig_now < 2:
			return (-1, -1, -1)
		
		if countBig_old == 0:
			return (-1, -1, -1)
		
		img = -1
		if countBig_now == countBig_old+1:
			img = 1
		else:
			img = 0
		
		if lastBet_row == -1 and lastBet_col == -1:
			return (0, 0, 0)
		
		pos = (-1, -1, -1)
		if img == lastBet_img:
			pos = self.PosNext(map, lastBet_row, lastBet_col, lastBet_img)
		else:
			pos = self.PosChangeCol(map, lastBet_img)
		
		return pos
	
	def PosNext(self, map, lastBet_row, lastBet_col, lastBet_img):
		if lastBet_row == -1 and lastBet_col == -1:
			return (0, 0, lastBet_img)
		elif lastBet_row == 5:
			return (lastBet_row, lastBet_col+1, lastBet_img)
		elif map[lastBet_row+1][lastBet_col-1] == lastBet_img:
			return (lastBet_row, lastBet_col+1, lastBet_img)
		elif lastBet_row < 4 and map[lastBet_row+2][lastBet_col] == lastBet_img:
			return (lastBet_row, lastBet_col+1, lastBet_img)
		elif map[lastBet_row+1][lastBet_col] != -1:
			return (lastBet_row, lastBet_col+1, lastBet_img)
		else:
			return (lastBet_row+1, lastBet_col, lastBet_img)
	
	def PosChangeCol(self, map, lastBet_img):
		img = 0
		if lastBet_img == 0:
			img = 1
		else:
			img = 0
		
		for col in range(30):
			if map[0][col] == -1:
				return (0, col, img)

class GridWindow(QWidget):
	def __init__(self, parent = None):
		super(GridWindow, self).__init__(parent)
		
		self.UI_hl = QHBoxLayout(self)
		self.left_qframe = QFrame(self)
		self.left_vl = QVBoxLayout(self.left_qframe)
		self.bet_qframe = QFrame(self)
		self.bet_vl = QVBoxLayout(self.bet_qframe)
		
		self.sizeDefine()
		self.UIcreate()
		
		self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
		self.setFixedSize(1251, 917)
		print self.sizeHint()
		self.vline.setFixedHeight(self.sizeHint().height()-50)
		
		self.betRecord = betRecord()
		self.testFunc()
	
	def sizeDefine(self):
		self.count = 0
		self.sizeWidth = 60
		self.sizeHeight = 25
		self.sizeWidth_btn = 70
		self.sizeHeight_btn = 22
		self.sizeWidth_qlineedit = 60
		self.sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
		
		self.binp_btnWidth = 37
		self.binp_btnHeight = 30
	
	def UIcreate(self):
		self.UIcreate_Grid()
		self.UI_create_Vline()
		self.UIcreate_BetStatus()
		self.UIcreate_numberInput()
		
		self.UI_hl.addWidget(self.left_qframe)
		self.UI_hl.addWidget(self.vline)
		self.UI_hl.addWidget(self.bet_qframe)
		
		self.initialGlobalAttribute()
		self.initialBtnConnect()
		
		self.setLayout(self.UI_hl)
	
	def UIcreate_Grid(self):
		self.UIcreate_GridLayout()
		self.UIcreate_GridBar()
		
		for i in range(4):
			self.left_vl.addWidget(self.bar_qframe[i])
			self.left_vl.addWidget(self.grid_qframe[i])
		self.left_qframe.setLayout(self.left_vl)
	
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
			for row in range(6):
				tmprow = []
				for col in range(30):
					tmprow.append(QLabel(self.grid_qframe[i]))
					pixmap = QPixmap(imgCell)
					tmprow[len(tmprow)-1].setPixmap(pixmap)
					tmprow[len(tmprow)-1].setScaledContents(True)
					self.grid_gl[i].addWidget(tmprow[len(tmprow)-1], row, col)
				
				tmp.append(tmprow)
			
			self.grid_qlabelList.append(tmp)
			
			# set relationship
			self.grid_qframe[i].setLayout(self.grid_gl[i])
	
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
	
	def UI_create_Vline(self):
		self.vline = QFrame(self)
		self.vline.setFrameShape(QFrame.VLine)
		self.vline.setFrameShadow(QFrame.Sunken)
	
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
		#self.pbet_qlabel1 = QLabel("<html><img src='%s'></html>" %imgRedBtn)
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
		self.rbet_qscrollarea = QScrollArea(self.rbet_qframe)
		
		# set relationship
		self.rbet_qframe.setLayout(self.rbet_vl)
		self.rbet_vl.addWidget(self.rbet_qlabel)
		self.rbet_vl.addWidget(self.rbet_qscrollarea)
		self.bet_vl.addWidget(self.rbet_qframe)
	
	def UIcreate_numberInput(self):
		self.binp_qframe = []
		self.binp_gl = []
		self.binp_btn0 = []
		self.binp_btn1 = []
		self.binp_btn2 = []
		self.binp_btn3 = []
		self.binp_btn4 = []
		self.binp_btn5 = []
		self.binp_btn6 = []
		self.binp_btn7 = []
		self.binp_btn8 = []
		self.binp_btn9 = []
		self.binp_btn10 = []
		self.binp_btn11 = []
		
		for i in range(4):
			# initial
			self.binp_qframe.append(QFrame(self))
			self.binp_gl.append(QGridLayout(self.binp_qframe[i]))
			self.binp_btn0.append(QPushButton(self.binp_qframe[i]))
			self.binp_btn1.append(QPushButton(self.binp_qframe[i]))
			self.binp_btn2.append(QPushButton(self.binp_qframe[i]))
			self.binp_btn3.append(QPushButton(self.binp_qframe[i]))
			self.binp_btn4.append(QPushButton(self.binp_qframe[i]))
			self.binp_btn5.append(QPushButton(self.binp_qframe[i]))
			self.binp_btn6.append(QPushButton(self.binp_qframe[i]))
			self.binp_btn7.append(QPushButton(self.binp_qframe[i]))
			self.binp_btn8.append(QPushButton(self.binp_qframe[i]))
			self.binp_btn9.append(QPushButton(self.binp_qframe[i]))
			self.binp_btn10.append(QPushButton(self.binp_qframe[i]))
			self.binp_btn11.append(QPushButton(self.binp_qframe[i]))
			
			# set relationship
			self.binp_qframe[i].setLayout(self.binp_gl[i])
			self.binp_gl[i].addWidget(self.binp_btn1[i], 0, 0)
			self.binp_gl[i].addWidget(self.binp_btn2[i], 0, 1)
			self.binp_gl[i].addWidget(self.binp_btn3[i], 0, 2)
			self.binp_gl[i].addWidget(self.binp_btn4[i], 1, 0)
			self.binp_gl[i].addWidget(self.binp_btn5[i], 1, 1)
			self.binp_gl[i].addWidget(self.binp_btn6[i], 1, 2)
			self.binp_gl[i].addWidget(self.binp_btn7[i], 2, 0)
			self.binp_gl[i].addWidget(self.binp_btn8[i], 2, 1)
			self.binp_gl[i].addWidget(self.binp_btn9[i], 2, 2)
			self.binp_gl[i].addWidget(self.binp_btn0[i], 3, 0)
			self.binp_gl[i].addWidget(self.binp_btn10[i], 3, 1)
			self.binp_gl[i].addWidget(self.binp_btn11[i], 3, 2)
	
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
		self.pbet_qframe.setStyleSheet('''.QFrame {background-color: white; border: 1px solid gray;}''')
		self.pbet_qframe.setSizePolicy(self.sizePolicy)
		self.pbet_qframe.setFixedWidth(215)
		self.pbet_qframe.setFixedHeight(135)
		
		self.pbet_gl.setSpacing(1)
		self.pbet_gl.setMargin(1)
		
		self.pbet_qlabel1.setStyleSheet('''.QLabel {background-color: white; border-bottom: 1px solid gray;}''')
		pixmap = QPixmap(imgRedBtn)
		self.pbet_qlabel1.setPixmap(pixmap)
		self.pbet_qlabel1.setScaledContents(True)
		
		self.pbet_qlabel2.setStyleSheet('''.QLabel {background-color: white; border-bottom: 1px solid gray;}''')
		pixmap = QPixmap(imgGreenBtn)
		self.pbet_qlabel2.setPixmap(pixmap)
		self.pbet_qlabel2.setScaledContents(True)
		
		self.pbet_qlabel3.setStyleSheet('''.QLabel {background-color: white; border-bottom: 1px solid gray;}''')
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
		self.rbet_qframe.setSizePolicy(self.sizePolicy)
		
		self.rbet_vl.setSpacing(0)
		self.rbet_vl.setMargin(1)
		
		self.rbet_qlabel.setStyleSheet('''.QLabel {background-color: white; border-top: 1px solid gray;
											border-left: 1px solid gray; border-right: 1px solid gray;}''')
		self.rbet_qlabel.setText(self.tr('投注紀錄'))
		self.rbet_qlabel.setAlignment(Qt.AlignCenter)
		self.rbet_qlabel.setFixedWidth(215)
		self.rbet_qlabel.setFixedHeight(30)
		
		#for i in range(30):
			#self.rbet_qscrollarea.setWidget(QLabel(str(i)))
		
		self.rbet_qscrollarea.setStyleSheet('''.QScrollArea {background-color: white;}''')
		self.rbet_qscrollarea.setFixedWidth(215)
		self.rbet_qscrollarea.setFixedHeight(380)
		
		# initail global values of UIcreate_numberInput
		#----------------------------------------------------
		self.binp_qframe[0].setGeometry(QRect(565, 60, 140, 150))
		self.binp_qframe[1].setGeometry(QRect(565, 279, 140, 150))
		self.binp_qframe[2].setGeometry(QRect(565, 498, 140, 150))
		self.binp_qframe[3].setGeometry(QRect(565, 717, 140, 150))
		for i in range(4):
			self.binp_qframe[i].setStyleSheet('''.QFrame {background-color: rgb(230, 230, 230); border: 2px solid gray;}
												.QPushButton {background-color: rgb(250, 250, 250); font-family: Arial, Microsoft JhengHei, serif, sans-serif;}''')
			self.binp_qframe[i].setFrameShape(QFrame.StyledPanel)
			self.binp_qframe[i].setFrameShadow(QFrame.Raised)
			self.binp_qframe[i].close()
			
			self.binp_gl[i].setSpacing(1)
			self.binp_gl[i].setMargin(1)
			
			self.binp_btn10[i].setStyleSheet('''.QPushButton {background-color: rgb(255, 47, 61); color: white;}''')
			self.binp_btn11[i].setStyleSheet('''.QPushButton {background-color: rgb(116, 106, 255); color: white;}''')
			
			self.binp_btn0[i].setText('0')
			self.binp_btn1[i].setText('1')
			self.binp_btn2[i].setText('2')
			self.binp_btn3[i].setText('3')
			self.binp_btn4[i].setText('4')
			self.binp_btn5[i].setText('5')
			self.binp_btn6[i].setText('6')
			self.binp_btn7[i].setText('7')
			self.binp_btn8[i].setText('8')
			self.binp_btn9[i].setText('9')
			self.binp_btn10[i].setText(self.tr('莊'))
			self.binp_btn11[i].setText(self.tr('閒'))
			
			self.binp_btn0[i].setFixedWidth(self.binp_btnWidth)
			self.binp_btn0[i].setFixedHeight(self.binp_btnHeight)
			self.binp_btn1[i].setFixedWidth(self.binp_btnWidth)
			self.binp_btn1[i].setFixedHeight(self.binp_btnHeight)
			self.binp_btn2[i].setFixedWidth(self.binp_btnWidth)
			self.binp_btn2[i].setFixedHeight(self.binp_btnHeight)
			self.binp_btn3[i].setFixedWidth(self.binp_btnWidth)
			self.binp_btn3[i].setFixedHeight(self.binp_btnHeight)
			self.binp_btn4[i].setFixedWidth(self.binp_btnWidth)
			self.binp_btn4[i].setFixedHeight(self.binp_btnHeight)
			self.binp_btn5[i].setFixedWidth(self.binp_btnWidth)
			self.binp_btn5[i].setFixedHeight(self.binp_btnHeight)
			self.binp_btn6[i].setFixedWidth(self.binp_btnWidth)
			self.binp_btn6[i].setFixedHeight(self.binp_btnHeight)
			self.binp_btn7[i].setFixedWidth(self.binp_btnWidth)
			self.binp_btn7[i].setFixedHeight(self.binp_btnHeight)
			self.binp_btn8[i].setFixedWidth(self.binp_btnWidth)
			self.binp_btn8[i].setFixedHeight(self.binp_btnHeight)
			self.binp_btn9[i].setFixedWidth(self.binp_btnWidth)
			self.binp_btn9[i].setFixedHeight(self.binp_btnHeight)
			self.binp_btn10[i].setFixedWidth(self.binp_btnWidth)
			self.binp_btn10[i].setFixedHeight(self.binp_btnHeight)
			self.binp_btn11[i].setFixedWidth(self.binp_btnWidth)
			self.binp_btn11[i].setFixedHeight(self.binp_btnHeight)
	
	def initialBtnConnect(self):
		# initail left bar btn in UIcreate_Grid
		#----------------------------------------------------
		for i in range(4):
			func = getattr(self, 'connect_lbar_btn' + str(i))
			self.lbar_btn[i].clicked.connect(func)
		
		# initail right bar btn in UIcreate_Grid
		#----------------------------------------------------
		for i in range(4):
			func = getattr(self, 'connect_rbar_btn' + str(i))
			self.rbar_btn[i].clicked.connect(func)
		
		# initail bet and print area in UIcreate_BetStatus
		#----------------------------------------------------
		self.bbet_btn1.clicked.connect(self.connect_bbet_btn1)
		self.bbet_btn2.clicked.connect(self.connect_bbet_btn2)
		#clickable(self.bbet_qlabel1).connect(self.connect_bbet_qlabel1)
		
		# initail bet push button area in UIcreate_BetStatus
		#----------------------------------------------------
		clickable(self.pbet_qlabel1).connect(self.connect_pbet_qlabel1)
		clickable(self.pbet_qlabel2).connect(self.connect_pbet_qlabel2)
		clickable(self.pbet_qlabel3).connect(self.connect_pbet_qlabel3)
		self.pbet_btn.clicked.connect(self.connect_pbet_btn)
	
	def connect_lbar_btn0(self):
		self.show_binp(0)
	
	def connect_lbar_btn1(self):
		self.show_binp(1)
	
	def connect_lbar_btn2(self):
		self.show_binp(2)
	
	def connect_lbar_btn3(self):
		self.show_binp(3)
	
	def show_binp(self, i):
		c = self.lbar_btn[i].text()
		#print c.toUtf8()
		if self.lbar_btn[i].text().toUtf8() == '手動':
			self.lbar_btn[i].setText(self.tr('確認'))
			self.binp_qframe[i].show()
		else:
			self.lbar_btn[i].setText(self.tr('手動'))
			self.binp_qframe[i].close()
	
	def connect_rbar_btn0(self):
		self.stop_count(0)
	
	def connect_rbar_btn1(self):
		self.stop_count(1)
	
	def connect_rbar_btn2(self):
		self.stop_count(2)
	
	def connect_rbar_btn3(self):
		self.stop_count(3)
	
	# stop and count
	def stop_count(self, i):
		print self.rbar_btn[i].text().toUtf8()
	
	def connect_bbet_btn1(self):
		print self.bbet_btn1.text().toUtf8()
	
	def connect_bbet_btn2(self):
		print self.bbet_btn2.text().toUtf8()
	
	def connect_pbet_qlabel1(self):
		self.showBet(Banker)
	
	def connect_pbet_qlabel2(self):
		self.showBet(Tie)
	
	def connect_pbet_qlabel3(self):
		self.showBet(Player)
	
	def showBet(self, winner):
		ret = self.betRecord.bet(winner)
		if ret.get('status') == 0:
			showList = [ret.get('Big'), ret.get('Eye'), ret.get('Sma'), ret.get('Pen')]
			#print showList
			
			for i in range(4):
				row = showList[i][0]
				col = showList[i][1]
				img = showList[i][2]
				if row >= 0 and col >= 0:
					if winner != Tie:
						pixmap = QPixmap(self.betRecord.imgPath[i][img])
						self.grid_qlabelList[i][row][col].setPixmap(pixmap)
					else:
						pass
	
	def connect_pbet_btn(self):
		print self.pbet_btn.text().toUtf8()
	
	# pos in the main widget
	def mousePressEvent(self, QMouseEvent):
		#print 'pos in the widget', QMouseEvent.pos()
		pass
	
	# pos in the windows screen
	def mouseReleaseEvent(self, QMouseEvent):
		cursor = QCursor()
		#print 'pos in the windows screen', cursor.pos()
	
	def testFunc(self):
		#self.rbet_qscrollarea
		test_frame = QFrame(self.rbet_qscrollarea)
		test_vl = QVBoxLayout(test_frame)
		test_vl.setSpacing(0)
		
		for i in range(50):
			test_vl.addWidget(QLabel(str(i)))
		
		self.rbet_qscrollarea.setWidget(test_frame)
		
		#pixmap = QPixmap(imgRedCir)
		#self.grid_qlabelList[0][0][0].setPixmap(pixmap)
		#self.grid_qlabelList[0][1][0].setPixmap(pixmap)
		#self.grid_qlabelList[1][5][0].setPixmap(pixmap)
		#print self.pbet_qframe.sizeHint()

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

if __name__ == "__main__":
	app = QApplication(sys.argv)
	GridWindow = GridWindow()
	GridWindow.show()
	
	app.exec_()