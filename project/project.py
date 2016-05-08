import sys
import functools
from PyQt4.QtGui import *
from PyQt4.QtCore import *

QTextCodec.setCodecForTr(QTextCodec.codecForName("utf8"))

# image path
imgDir = 'img/'
imgCell = imgDir + 'cell.png'

imgRedBtn = imgDir + 'red_btn.png'
imgGreenBtn = imgDir + 'green_btn.png'
imgBlueBtn = imgDir + 'blue_btn.png'

imgCirGreen = imgDir + 'cir_green.png'
imgBigRedCirGreen = imgDir + 'big_red_cir_green.png'
imgBigBlueCirGreen = imgDir + 'big_blue_cir_green.png'
imgBigRedCir = imgDir + 'big_red_cir.png'
imgBigBlueCir = imgDir + 'big_blue_cir.png'
imgEyeRedCir = imgDir + 'eye_red_cir.png'
imgEyeBlueCir = imgDir + 'eye_blue_cir.png'
imgSmaRedCir = imgDir + 'sma_red_cir.png'
imgSmaBlueCir = imgDir + 'sma_blue_cir.png'
imgPenRedCir = imgDir + 'pen_red_cir.png'
imgPenBlueCir = imgDir + 'pen_blue_cir.png'

imgSugBigRedCir = imgDir + 'sug_big_red_cir.png'
imgSugBigBlueCir = imgDir + 'sug_big_blue_cir.png'
imgSugEyeRedCir = imgDir + 'sug_eye_red_cir.png'
imgSugEyeBlueCir = imgDir + 'sug_eye_blue_cir.png'
imgSugSmaRedCir = imgDir + 'sug_sma_red_cir.png'
imgSugSmaBlueCir = imgDir + 'sug_sma_blue_cir.png'
imgSugPenRedCir = imgDir + 'sug_pen_red_cir.png'
imgSugPenBlueCir = imgDir + 'sug_pen_blue_cir.png'

imgNextStatusEyeRedCir = imgDir + 'next_eye_red_cir.png'
imgNextStatusEyeBlueCir = imgDir + 'next_eye_blue_cir.png'
imgNextStatusSmaRedCir = imgDir + 'next_sma_red_cir.png'
imgNextStatusSmaBlueCir = imgDir + 'next_sma_blue_cir.png'
imgNextStatusPenRedCir = imgDir + 'next_pen_red_cir.png'
imgNextStatusPenBlueCir = imgDir + 'next_pen_blue_cir.png'

# value for bet button
Banker = 0
Player = 1
Tie = 2

# status value
Back_From_Tie = 1
Still_Tie = 2
No_Back = 5

# TODO : handle first record is Tie
# TODO : handle overflow(when over 6*30)

class betRecord():
	def __init__(self):
		self.recordAll = []
		self.recordBig = []
		self.recordEye = []
		self.recordSma = []
		self.recordPen = []
		
		# self.countResult[0] is the count of Banker
		# self.countResult[1] is the count of Player
		# self.countResult[2] is the count of Tie
		self.countResult = []
		for i in range(3):
			self.countResult.append(0)
		
		# count continuous times for Eye, Sma, Pen
		self.countBig = []
		for i in range(30):
			self.countBig.append(0)
		
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
		
		self.betSugBig = []
		self.betSugBig_sum = []
		self.betSugEye = []
		self.betSugSma = []
		self.betSugPen = []
		self.betCountBig = []
		self.betCountEye = []
		self.betCountSma = []
		self.betCountPen = []
		self.betStatusBig = []
		self.betStatusEye = []
		self.betStatusSma = []
		self.betStatusPen = []
		
		self.imgPath = []
		# imgPath[0] -> imgBig
		self.imgPath.append([imgBigRedCir, imgBigBlueCir, (imgBigRedCirGreen, imgBigBlueCirGreen)])
		# imgPath[1] -> imgEye
		self.imgPath.append([imgEyeRedCir, imgEyeBlueCir])
		# imgPath[2] -> imgSma
		self.imgPath.append([imgSmaRedCir, imgSmaBlueCir])
		# imgPath[3] -> imgPen
		self.imgPath.append([imgPenRedCir, imgPenBlueCir])
		
		self.imgSugPath = []
		self.imgSugPath.append([imgSugBigRedCir, imgSugBigBlueCir])
		self.imgSugPath.append([imgSugEyeRedCir, imgSugEyeBlueCir])
		self.imgSugPath.append([imgSugSmaRedCir, imgSugSmaBlueCir])
		self.imgSugPath.append([imgSugPenRedCir, imgSugPenBlueCir])
		
		self.imgNextStatusPath = []
		self.imgNextStatusPath.append(['', ''])
		self.imgNextStatusPath.append([imgNextStatusEyeRedCir, imgNextStatusEyeBlueCir])
		self.imgNextStatusPath.append([imgNextStatusSmaRedCir, imgNextStatusSmaBlueCir])
		self.imgNextStatusPath.append([imgNextStatusPenRedCir, imgNextStatusPenBlueCir])
	
	def bet(self, winner, isPredict = False):
		self.countResult[winner] += 1
		if winner != Tie:
			retPos = self.findPos(winner)
			if retPos.get('status') == 0:
				Big = retPos.get('Big')
				Eye = retPos.get('Eye')
				Sma = retPos.get('Sma')
				Pen = retPos.get('Pen')
				self.recordBig.append(Big)
				self.recordEye.append(Eye)
				self.recordSma.append(Sma)
				self.recordPen.append(Pen)
				self.mapBig[Big[0]][Big[1]] = Big[2]
				self.mapEye[Eye[0]][Eye[1]] = Eye[2]
				self.mapSma[Sma[0]][Sma[1]] = Sma[2]
				self.mapPen[Pen[0]][Pen[1]] = Pen[2]
				self.recordAll.append(winner)
				
				self.storeBetStatus(Big, Eye, Sma, Pen)
				retSug = self.suggestNextBet(Big, Eye, Sma, Pen)
				SugBig = retSug.get('SugBig')
				SugEye = retSug.get('SugEye')
				SugSma = retSug.get('SugSma')
				SugPen = retSug.get('SugPen')
				self.betSugBig.append(SugBig)
				self.betSugEye.append(SugEye)
				self.betSugSma.append(SugSma)
				self.betSugPen.append(SugPen)
				
				if not isPredict:
					# if SugBig want to show sum, edit SugBig_sum to SugBig
					# or just return SugBig_sum replace SugBig
					SugBig_sum = self.sumBetInSugBig(Big, SugBig, SugEye, SugSma, SugPen)
					self.betSugBig_sum.append(SugBig_sum)
				else:
					self.betSugBig_sum.append(SugBig)
				
				lastSug = self.lastSugBet()
				lastSugBig = lastSug.get('lastSugBig')
				lastSugBig_sum = lastSug.get('lastSugBig_sum')
				lastSugEye = lastSug.get('lastSugEye')
				lastSugSma = lastSug.get('lastSugSma')
				lastSugPen = lastSug.get('lastSugPen')
				
				retResult = self.resultBet(lastSugBig, lastSugEye, lastSugSma, lastSugPen, Big, Eye, Sma, Pen)
				isBet = retResult.get('isBet')
				sameBet = retResult.get('sameBet')
				countBet = retResult.get('countBet')
				
				return {'status': 0, 'Big': Big, 'Eye': Eye, 'Sma': Sma, 'Pen': Pen,
						'SugBig': SugBig, 'SugEye': SugEye, 'SugSma': SugSma, 'SugPen': SugPen,
						'lastSugBig': lastSugBig_sum, 'lastSugEye': lastSugEye, 'lastSugSma': lastSugSma, 'lastSugPen': lastSugPen,
						'isBet': isBet, 'sameBet': sameBet, 'countBet': countBet}
		else:
			# TODO : handle first record is Tie
			
			lastBet = self.recordBig[-1]
			Big = (lastBet[0], lastBet[1], Tie)
			Eye = (-1, -1, -1)
			Sma = (-1, -1, -1)
			Pen = (-1, -1, -1)
			self.recordAll.append(winner)
			
			SugBig, SugEye, SugSma, SugPen = (-1, -1, -1, -1), (-1, -1, -1, -1), (-1, -1, -1, -1), (-1, -1, -1, -1)
			lastSugBig, lastSugEye, lastSugSma, lastSugPen = (-1, -1, -1, -1), (-1, -1, -1, -1), (-1, -1, -1, -1), (-1, -1, -1, -1)
			
			if lastBet[2] == Tie:
				return {'status': Still_Tie}
			
			return {'status': 0, 'Big': lastBet, 'Eye': Eye, 'Sma': Sma, 'Pen': Pen,
					'SugBig': SugBig, 'SugEye': SugEye, 'SugSma': SugSma, 'SugPen': SugPen,
					'lastSugBig': lastSugBig, 'lastSugEye': lastSugEye, 'lastSugSma': lastSugSma, 'lastSugPen': lastSugPen}
	
	def findPos(self, winner):
		Big, Eye, Sma, Pen = (-1, -1, -1), (-1, -1, -1), (-1, -1, -1), (-1, -1, -1)
		
		if len(self.recordAll) == 0:
			Big = (0, 0, winner)
			self.countBig[0] += 1
			return {'status': 0, 'Big': Big, 'Eye': Eye, 'Sma': Sma, 'Pen': Pen}
		
		i = len(self.recordBig)-1
		lastBet = self.recordBig[i]
		while lastBet[2] == Tie:
			i = i-1
			lastBet = self.recordBig[i]
		
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
			for i in range(29, 0, -1):
				self.countBig[i] = self.countBig[i-1]
			self.countBig[0] = 1
		
		#print Big, Eye, Sma, Pen
		return {'status': 0, 'Big': Big, 'Eye': Eye, 'Sma': Sma, 'Pen': Pen}
	
	def findColor(self, jump, countBig_now, countBig_old):
		if jump:
			if countBig_now == countBig_old:
				return Banker
			else:
				return Player
		else:
			if countBig_now <= countBig_old:
				return Banker
			elif countBig_now == countBig_old+1:
				return Player
			else:
				return Banker
	
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
	
	def backOneStep(self):
		if len(self.recordAll) != 0:
			winner = self.recordAll.pop()
			self.countResult[winner] -= 1
			if winner != Tie:
				Big = self.recordBig.pop()
				Eye = self.recordEye.pop()
				Sma = self.recordSma.pop()
				Pen = self.recordPen.pop()
				self.mapBig[Big[0]][Big[1]] = -1
				self.mapEye[Eye[0]][Eye[1]] = -1
				self.mapSma[Sma[0]][Sma[1]] = -1
				self.mapPen[Pen[0]][Pen[1]] = -1
				
				self.countBig[0] -= 1
				if self.countBig[0] == 0:
					for i in range(29):
						self.countBig[i] = self.countBig[i+1]
				
				lastSug = self.lastSugBet()
				lastSugBig = lastSug.get('lastSugBig')
				lastSugBig_sum = lastSug.get('lastSugBig_sum')
				lastSugEye = lastSug.get('lastSugEye')
				lastSugSma = lastSug.get('lastSugSma')
				lastSugPen = lastSug.get('lastSugPen')
				
				SugBig = self.betSugBig.pop()
				SugBig = self.betSugBig_sum.pop()
				SugEye = self.betSugEye.pop()
				SugSma = self.betSugSma.pop()
				SugPen = self.betSugPen.pop()
				self.betCountBig.pop()
				self.betCountEye.pop()
				self.betCountSma.pop()
				self.betCountPen.pop()
				self.betStatusBig.pop()
				self.betStatusEye.pop()
				self.betStatusSma.pop()
				self.betStatusPen.pop()
				
				return {'status': 0, 'Big': Big, 'Eye': Eye, 'Sma': Sma, 'Pen': Pen,
						'SugBig': SugBig, 'SugEye': SugEye, 'SugSma': SugSma, 'SugPen': SugPen,
						'lastSugBig': lastSugBig, 'lastSugEye': lastSugEye, 'lastSugSma': lastSugSma, 'lastSugPen': lastSugPen}
			else:
				if self.recordAll[-1] == Tie:
					return {'status': Still_Tie}
				else:
					Big = self.recordBig[-1]
					return {'status': Back_From_Tie, 'Big': Big}
		else:
			return {'status': No_Back}
	
	def predictNextStatus(self):
		nextStatus = []
		
		for i in range(2):
			ret = self.bet(i, isPredict = True)
			nextStatus.append((ret.get('Eye')[2], ret.get('Sma')[2], ret.get('Pen')[2]))
			self.backOneStep()
		
		return nextStatus
	
	def storeBetStatus(self, Big, Eye, Sma, Pen):
		# bet count Big
		if len(self.betSugBig) == 0:
			self.betStatusBig.append(-1)
			self.betCountBig.append(0)
		elif Big[2] == -1:
			self.betStatusBig.append(-1)
			self.betCountBig.append(self.betCountBig[-1])
		elif self.betSugBig[-1][2] == -1:
			self.betStatusBig.append(-1)
			self.betCountBig.append(self.betCountBig[-1])
		elif Big[2] == self.betSugBig[-1][2] and self.betSugBig[-1][3] != 0:
			self.betStatusBig.append(0)
			self.betCountBig.append(self.betCountBig[-1] + self.betSugBig[-1][3]*2)
		elif Big[2] != self.betSugBig[-1][2] and self.betSugBig[-1][3] != 0:
			self.betStatusBig.append(1)
			self.betCountBig.append(self.betCountBig[-1] - self.betSugBig[-1][3])
		else:
			self.betStatusBig.append(-1)
			self.betCountBig.append(self.betCountBig[-1])
		
		# bet count Eye
		if len(self.betSugEye) == 0:
			self.betStatusEye.append(-1)
			self.betCountEye.append(0)
		elif Eye[2] == -1:
			self.betStatusEye.append(-1)
			self.betCountEye.append(self.betCountEye[-1])
		elif self.betSugEye[-1][2] == -1:
			self.betStatusEye.append(-1)
			self.betCountEye.append(self.betCountEye[-1])
		elif Eye[2] == self.betSugEye[-1][2] and self.betSugEye[-1][3] != 0:
			self.betStatusEye.append(0)
			self.betCountEye.append(self.betCountEye[-1] + self.betSugEye[-1][3]*2)
		elif Eye[2] != self.betSugEye[-1][2] and self.betSugEye[-1][3] != 0:
			self.betStatusEye.append(1)
			self.betCountEye.append(self.betCountEye[-1] - self.betSugEye[-1][3])
		else:
			self.betStatusEye.append(-1)
			self.betCountEye.append(self.betCountEye[-1])
		
		# bet count Sma
		if len(self.betSugSma) == 0:
			self.betStatusSma.append(-1)
			self.betCountSma.append(0)
		elif Sma[2] == -1:
			self.betStatusSma.append(-1)
			self.betCountSma.append(self.betCountSma[-1])
		elif self.betSugSma[-1][2] == -1:
			self.betStatusSma.append(-1)
			self.betCountSma.append(self.betCountSma[-1])
		elif Sma[2] == self.betSugSma[-1][2] and self.betSugSma[-1][3] != 0:
			self.betStatusSma.append(0)
			self.betCountSma.append(self.betCountSma[-1] + self.betSugSma[-1][3]*2)
		elif Sma[2] != self.betSugSma[-1][2] and self.betSugSma[-1][3] != 0:
			self.betStatusSma.append(1)
			self.betCountSma.append(self.betCountSma[-1] - self.betSugSma[-1][3])
		else:
			self.betStatusSma.append(-1)
			self.betCountSma.append(self.betCountSma[-1])
		
		# bet count Pen
		if len(self.betSugPen) == 0:
			self.betStatusPen.append(-1)
			self.betCountPen.append(0)
		elif Pen[2] == -1:
			self.betStatusPen.append(-1)
			self.betCountPen.append(self.betCountPen[-1])
		elif self.betSugPen[-1][2] == -1:
			self.betStatusPen.append(-1)
			self.betCountPen.append(self.betCountPen[-1])
		elif Pen[2] == self.betSugPen[-1][2] and self.betSugPen[-1][3] != 0:
			self.betStatusPen.append(0)
			self.betCountPen.append(self.betCountPen[-1] + self.betSugPen[-1][3]*2)
		elif Pen[2] != self.betSugPen[-1][2] and self.betSugPen[-1][3] != 0:
			self.betStatusPen.append(1)
			self.betCountPen.append(self.betCountPen[-1] - self.betSugPen[-1][3])
		else:
			self.betStatusPen.append(-1)
			self.betCountPen.append(self.betCountPen[-1])
	
	def suggestNextBet(self, Big, Eye, Sma, Pen):
		SugBig, SugEye, SugSma, SugPen = (-1, -1, -1, -1), (-1, -1, -1, -1), (-1, -1, -1, -1), (-1, -1, -1, -1)
		if len(self.recordAll) == 0:
			return {'SugBig': SugBig, 'SugEye': SugEye, 'SugSma': SugSma, 'SugPen': SugPen}
		
		# SugBig
		#----------------------------------------------------
		if Big[0] == -1 and Big[1] == -1:
			SugBig = (-1, -1, -1, -1)
		elif self.betStatusBig[-1] == -1:
			lastBet = self.recordBig[-1]
			sugBigBet = 1
			tmpBig = self.PosNext(self.mapBig, lastBet[0], lastBet[1], lastBet[2])
			SugBig = (tmpBig[0], tmpBig[1], tmpBig[2], sugBigBet)
		elif self.betStatusBig[-1] == 0:
			lastBet = self.recordBig[-1]
			sugBigBet = self.betSugBig[-1][3] + 1
			tmpBig = self.PosNext(self.mapBig, lastBet[0], lastBet[1], lastBet[2])
			SugBig = (tmpBig[0], tmpBig[1], tmpBig[2], sugBigBet)
		elif self.betStatusBig[-1] == 1:
			lastBet = self.recordBig[-1]
			'''
			if self.betCountBig[-1] > 0:
				sugBigBet = self.betSugBig[-1][3] - 1
				if sugBigBet <= 0:
					sugBigBet = 1
				tmpBig = self.PosChangeCol(self.mapBig, lastBet[2])
				SugBig = (tmpBig[0], tmpBig[1], tmpBig[2], sugBigBet)
			else:
				sugBigBet = 1
				tmpBig = self.PosNext(self.mapBig, lastBet[0], lastBet[1], lastBet[2])
				SugBig = (tmpBig[0], tmpBig[1], tmpBig[2], sugBigBet)
			'''
			if self.betSugBig[-1][3] >  1:
				sugBigBet = self.betSugBig[-1][3] - 1
				tmpBig = self.PosChangeCol(self.mapBig, lastBet[2])
				SugBig = (tmpBig[0], tmpBig[1], tmpBig[2], sugBigBet)
			else:
				SugBig = (-1, -1, lastBet[1], 0)
		
		# SugEye
		#----------------------------------------------------
		if Eye[0] == -1 and Eye[1] == -1:
			SugEye = (-1, -1, -1, -1)
		elif self.betStatusEye[-1] == -1:
			lastBet = self.recordEye[-1]
			sugEyeBet = 1
			tmpEye = self.PosNext(self.mapEye, lastBet[0], lastBet[1], lastBet[2])
			SugEye = (tmpEye[0], tmpEye[1], tmpEye[2], sugEyeBet)
		elif self.betStatusEye[-1] == 0:
			lastBet = self.recordEye[-1]
			sugEyeBet = self.betSugEye[-1][3] + 1
			tmpEye = self.PosNext(self.mapEye, lastBet[0], lastBet[1], lastBet[2])
			SugEye = (tmpEye[0], tmpEye[1], tmpEye[2], sugEyeBet)
		elif self.betStatusEye[-1] == 1:
			lastBet = self.recordEye[-1]
			'''
			if self.betCountEye[-1] > 0:
				sugEyeBet = self.betSugEye[-1][3] - 1
				if sugEyeBet <= 0:
					sugEyeBet = 1
				tmpEye = self.PosChangeCol(self.mapEye, lastBet[2])
				SugEye = (tmpEye[0], tmpEye[1], tmpEye[2], sugEyeBet)
			else:
				sugEyeBet = 1
				tmpEye = self.PosNext(self.mapEye, lastBet[0], lastBet[1], lastBet[2])
				SugEye = (tmpEye[0], tmpEye[1], tmpEye[2], sugEyeBet)
			'''
			if self.betSugEye[-1][3] >  1:
				sugEyeBet = self.betSugEye[-1][3] - 1
				tmpEye = self.PosChangeCol(self.mapEye, lastBet[2])
				SugEye = (tmpEye[0], tmpEye[1], tmpEye[2], sugEyeBet)
			else:
				SugEye = (-1, -1, lastBet[1], 0)
		
		# SugSma
		#----------------------------------------------------
		if Sma[0] == -1 and Sma[1] == -1:
			SugSma = (-1, -1, -1, -1)
		elif self.betStatusSma[-1] == -1:
			lastBet = self.recordSma[-1]
			sugSmaBet = 1
			tmpSma = self.PosNext(self.mapSma, lastBet[0], lastBet[1], lastBet[2])
			SugSma = (tmpSma[0], tmpSma[1], tmpSma[2], sugSmaBet)
		elif self.betStatusSma[-1] == 0:
			lastBet = self.recordSma[-1]
			sugSmaBet = self.betSugSma[-1][3] + 1
			tmpSma = self.PosNext(self.mapSma, lastBet[0], lastBet[1], lastBet[2])
			SugSma = (tmpSma[0], tmpSma[1], tmpSma[2], sugSmaBet)
		elif self.betStatusSma[-1] == 1:
			lastBet = self.recordSma[-1]
			'''
			if self.betCountSma[-1] > 0:
				sugSmaBet = self.betSugSma[-1][3] - 1
				if sugSmaBet <= 0:
					sugSmaBet = 1
				tmpSma = self.PosChangeCol(self.mapSma, lastBet[2])
				SugSma = (tmpSma[0], tmpSma[1], tmpSma[2], sugSmaBet)
			else:
				sugSmaBet = 1
				tmpSma = self.PosNext(self.mapSma, lastBet[0], lastBet[1], lastBet[2])
				SugSma = (tmpSma[0], tmpSma[1], tmpSma[2], sugSmaBet)
			'''
			if self.betSugSma[-1][3] >  1:
				sugSmaBet = self.betSugSma[-1][3] - 1
				tmpEye = self.PosChangeCol(self.mapEye, lastBet[2])
				SugEye = (tmpEye[0], tmpEye[1], tmpEye[2], sugEyeBet)
			else:
				SugEye = (-1, -1, lastBet[1], 0)
		
		# SugPen
		#----------------------------------------------------
		if Pen[0] == -1 and Pen[1] == -1:
			SugPen = (-1, -1, -1, -1)
		elif self.betStatusPen[-1] == -1:
			lastBet = self.recordPen[-1]
			sugPenBet = 1
			tmpPen = self.PosNext(self.mapPen, lastBet[0], lastBet[1], lastBet[2])
			SugPen = (tmpPen[0], tmpPen[1], tmpPen[2], sugPenBet)
		elif self.betStatusPen[-1] == 0:
			lastBet = self.recordPen[-1]
			sugPenBet = self.betSugPen[-1][3] + 1
			tmpPen = self.PosNext(self.mapPen, lastBet[0], lastBet[1], lastBet[2])
			SugPen = (tmpPen[0], tmpPen[1], tmpPen[2], sugPenBet)
		elif self.betStatusPen[-1] == 1:
			lastBet = self.recordPen[-1]
			'''
			if self.betCountPen[-1] > 0:
				sugPenBet = self.betSugPen[-1][3] - 1
				if sugPenBet <= 0:
					sugPenBet = 1
				tmpPen = self.PosChangeCol(self.mapPen, lastBet[2])
				SugPen = (tmpPen[0], tmpPen[1], tmpPen[2], sugPenBet)
			else:
				sugPenBet = 1
				tmpPen = self.PosNext(self.mapPen, lastBet[0], lastBet[1], lastBet[2])
				SugPen = (tmpPen[0], tmpPen[1], tmpPen[2], sugPenBet)
			'''
			if self.betSugPen[-1][3] >  1:
				sugPenBet = self.betSugPen[-1][3] - 1
				tmpPen = self.PosChangeCol(self.mapPen, lastBet[2])
				SugPen = (tmpPen[0], tmpPen[1], tmpPen[2], sugPenBet)
			else:
				SugEye = (-1, -1, lastBet[1], 0)
		
		return {'SugBig': SugBig, 'SugEye': SugEye, 'SugSma': SugSma, 'SugPen': SugPen}
	
	def lastSugBet(self):
		lastSugBig, lastSugEye, lastSugSma, lastSugPen = (-1, -1, -1, -1), (-1, -1, -1, -1), (-1, -1, -1, -1), (-1, -1, -1, -1)
		lastSugBig_sum = (-1, -1, -1, -1)
		
		if len(self.betSugBig) > 1:
			lastSugBig = self.betSugBig[-2]
		
		if len(self.betSugBig_sum) > 1:
			lastSugBig_sum = self.betSugBig_sum[-2]
		
		if len(self.betSugEye) > 1:
			lastSugEye = self.betSugEye[-2]
		
		if len(self.betSugSma) > 1:
			lastSugSma = self.betSugSma[-2]
		
		if len(self.betSugPen) > 1:
			lastSugPen = self.betSugPen[-2]
		
		return {'lastSugBig': lastSugBig,'lastSugBig_sum': lastSugBig_sum, 'lastSugEye': lastSugEye, 'lastSugSma': lastSugSma, 'lastSugPen': lastSugPen}
	
	def sumBetInSugBig(self, Big, SugBig, SugEye, SugSma, SugPen):
		if Big[0] == 0 and Big[0] == 0:
			return SugBig
		
		nextStatus = self.predictNextStatus()
		sumList = [SugEye, SugSma, SugPen]
		imgBig = SugBig[2]
		betBig = SugBig[3]
		for i in range(3):
			if sumList[i][2] != -1:
				if sumList[i][2] == nextStatus[SugBig[2]][i]:
					betBig += sumList[i][3]
				else:
					betBig -= sumList[i][3]
		
		if betBig < 0:
			betBig = betBig * -1
			if imgBig == Big[2]:
				tmp = self.PosChangeCol(self.mapBig, Big[2])
			else:
				tmp = self.PosNext(self.mapBig, Big[0], Big[1], Big[2])
			
			return (tmp[0], tmp[1], tmp[2], betBig)
		
		return (SugBig[0], SugBig[1], imgBig, betBig)
	
	def resultBet(self, lastSugBig, lastSugEye, lastSugSma, lastSugPen, Big, Eye, Sma, Pen):
		isBet = [False, False, False, False]
		sameBet = [False, False, False, False]
		countBet = [0, 0, 0, 0]
		showList = [Big, Eye, Sma, Pen]
		lastSugList = [lastSugBig, lastSugEye, lastSugSma, lastSugPen]
		
		for i in range(4):
			if lastSugList[i][3] != -1:
				isBet[i] = True
				countBet[i] = lastSugList[i][3]
				
				if showList[i][2] == lastSugList[i][2]:
					sameBet[i] = True
				
				if i != 0:
					if sameBet[0] == sameBet[i]:
						countBet[0] += countBet[i]
					else:
						countBet[0] -= countBet[i]
		
		if countBet[0] < 0:
			countBet[0] = countBet[0] * -1
			sameBet[0] = not sameBet[0]
		
		return {'isBet': isBet, 'sameBet': sameBet, 'countBet': countBet}
	
	def manualChangeSug(self, i, img, bet):
		row, col = -1, -1
		erase_row, rease_col = -1, -1
		if i == 0:
			if len(self.betSugBig) != 0 and self.betSugBig[-1][0] != -1:
				tmp = self.betSugBig.pop()
				lastBet = self.recordBig[-1]
				if img == lastBet[2]:
					sugBig = self.PosNext(self.mapBig, lastBet[0], lastBet[1], lastBet[2])
					row = sugBig[0]
					col = sugBig[1]
					erase_row = tmp[0]
					rease_col = tmp[1]
				else:
					sugBig = self.PosChangeCol(self.mapBig, img)
					row = sugBig[0]
					col = sugBig[1]
					erase_row = tmp[0]
					rease_col = tmp[1]
				
				self.betSugBig.append((row, col, img, bet))
				
				SugBig = self.sumBetInSugBig(self.recordBig[-1], self.betSugBig[-1], self.betSugEye[-1], self.betSugSma[-1], self.betSugPen[-1])
				self.betSugBig_sum.pop()
				self.betSugBig_sum.append(SugBig)
		elif i == 1:
			if len(self.betSugEye) != 0 and self.betSugEye[-1][0] != -1:
				tmp = self.betSugEye.pop()
				lastBet = self.recordEye[-1]
				if img == lastBet[2]:
					sugEye = self.PosNext(self.mapEye, lastBet[0], lastBet[1], lastBet[2])
					row = sugEye[0]
					col = sugEye[1]
					erase_row = tmp[0]
					rease_col = tmp[1]
				else:
					sugEye = self.PosChangeCol(self.mapEye, img)
					row = sugEye[0]
					col = sugEye[1]
					erase_row = tmp[0]
					rease_col = tmp[1]
				
				self.betSugEye.append((row, col, img, bet))
		elif i == 2:
			if len(self.betSugSma) != 0 and self.betSugSma[-1][0] != -1:
				tmp = self.betSugSma.pop()
				lastBet = self.recordSma[-1]
				if img == lastBet[2]:
					sugSma = self.PosNext(self.mapSma, lastBet[0], lastBet[1], lastBet[2])
					row = sugSma[0]
					col = sugSma[1]
					erase_row = tmp[0]
					rease_col = tmp[1]
				else:
					sugSma = self.PosChangeCol(self.mapSma, img)
					row = sugSma[0]
					col = sugSma[1]
					erase_row = tmp[0]
					rease_col = tmp[1]
				
				self.betSugSma.append((row, col, img, bet))
		else:
			if len(self.betSugPen) != 0 and self.betSugPen[-1][0] != -1:
				tmp = self.betSugPen.pop()
				lastBet = self.recordPen[-1]
				if img == lastBet[2]:
					sugPen = self.PosNext(self.mapPen, lastBet[0], lastBet[1], lastBet[2])
					row = sugPen[0]
					col = sugPen[1]
					erase_row = tmp[0]
					rease_col = tmp[1]
				else:
					sugPen = self.PosChangeCol(self.mapPen, img)
					row = sugPen[0]
					col = sugPen[1]
					erase_row = tmp[0]
					rease_col = tmp[1]
				
				self.betSugPen.append((row, col, img, bet))
		
		return (row, col, img, bet), (erase_row, rease_col)
	
	def gameIsBegin(self):
		if len(self.recordBig) == 0:
			return False
		else:
			return True

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
					#pixmap = QPixmap(imgCell)
					#tmprow[len(tmprow)-1].setPixmap(pixmap)
					tmprow[len(tmprow)-1].setStyleSheet('''.QLabel {background-image: url(%s);}'''%imgCell)
					tmprow[len(tmprow)-1].setFixedWidth(30)
					tmprow[len(tmprow)-1].setFixedHeight(25)
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
		
		self.libet_qframe = QFrame(self.ibet_qframe)
		self.libet_gl = QGridLayout(self.libet_qframe)
		self.ibet_qlabel_banker1 = QLabel(self.libet_qframe)
		self.ibet_qlabel_banker2 = QLabel(self.libet_qframe)
		self.ibet_qlabel_banker3 = QLabel(self.libet_qframe)
		self.ibet_qlabel_banker4 = QLabel(self.libet_qframe)
		self.ibet_qlabel_player1 = QLabel(self.libet_qframe)
		self.ibet_qlabel_player2 = QLabel(self.libet_qframe)
		self.ibet_qlabel_player3 = QLabel(self.libet_qframe)
		self.ibet_qlabel_player4 = QLabel(self.libet_qframe)
		self.ibet_qlabel_tie1 = QLabel(self.libet_qframe)
		self.ibet_qlabel_tie2 = QLabel(self.libet_qframe)
		self.ibet_qlabel_tie3 = QLabel(self.libet_qframe)
		self.ibet_qlabel_tie4 = QLabel(self.libet_qframe)
		
		# set relationship
		self.ibet_qframe.setLayout(self.ibet_gl)
		self.ibet_gl.addWidget(self.ibet_qlabel1, 0, 4, 1, 2)
		self.ibet_gl.addWidget(self.ibet_qlabel2, 0, 6, 3, 2)
		self.ibet_gl.addWidget(self.ibet_qlabel3, 1, 4, 1, 2)
		self.ibet_gl.addWidget(self.ibet_qlabel4, 2, 4, 1, 2)
		self.ibet_gl.addWidget(self.libet_qframe, 0, 0, 3, 4)
		
		self.libet_qframe.setLayout(self.libet_gl)
		self.libet_gl.addWidget(self.ibet_qlabel_banker1, 0, 0)
		self.libet_gl.addWidget(self.ibet_qlabel_banker2, 0, 1)
		self.libet_gl.addWidget(self.ibet_qlabel_banker3, 0, 2)
		self.libet_gl.addWidget(self.ibet_qlabel_banker4, 0, 3)
		self.libet_gl.addWidget(self.ibet_qlabel_player1, 1, 0)
		self.libet_gl.addWidget(self.ibet_qlabel_player2, 1, 1)
		self.libet_gl.addWidget(self.ibet_qlabel_player3, 1, 2)
		self.libet_gl.addWidget(self.ibet_qlabel_player4, 1, 3)
		self.libet_gl.addWidget(self.ibet_qlabel_tie1, 2, 0)
		self.libet_gl.addWidget(self.ibet_qlabel_tie2, 2, 1)
		self.libet_gl.addWidget(self.ibet_qlabel_tie3, 2, 2)
		self.libet_gl.addWidget(self.ibet_qlabel_tie4, 2, 3)
		
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
			self.grid_qframe[i].setFixedWidth(931)
			self.grid_qframe[i].setFixedHeight(157)
			
			self.grid_gl[i].setSpacing(1)
			self.grid_gl[i].setMargin(1)
		
		# initail global values of UIcreate_BarForGrid
		#----------------------------------------------------
		# bar's title
		#--------------------------
		for i in range(4):
			self.tbar_hl[i].setSpacing(1)
			self.tbar_hl[i].setMargin(1)
			self.tbar_qlabel[i].setStyleSheet('''.QLabel {font-family: Arial, Microsoft JhengHei, serif, sans-serif;}''')
		
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
			self.lbar_qlabel[i].setStyleSheet('''.QLabel {color: white; font-family: Arial, Microsoft JhengHei, serif, sans-serif;}''')
			self.lbar_qlabel[i].setAlignment(Qt.AlignCenter)
			self.lbar_qlabel[i].setSizePolicy(self.sizePolicy)
			self.lbar_qlabel[i].setFixedWidth(self.sizeWidth)
			
			self.lbar_btn[i].setText(self.tr('手動'))
			self.lbar_btn[i].setStyleSheet('''.QPushButton {font-family: Arial, Microsoft JhengHei, serif, sans-serif;}''')
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
			self.rbar_qlabel1[i].setStyleSheet('''.QLabel {font-family: Arial, Microsoft JhengHei, serif, sans-serif;}''')
			self.rbar_qlabel1[i].setAlignment(Qt.AlignCenter)
			self.rbar_qlabel1[i].setSizePolicy(self.sizePolicy)
			self.rbar_qlabel1[i].setFixedWidth(self.sizeWidth)
			
			self.rbar_btn[i].setText(self.tr('切停'))
			self.rbar_btn[i].setStyleSheet('''.QPushButton {font-family: Arial, Microsoft JhengHei, serif, sans-serif;}''')
			self.rbar_btn[i].setSizePolicy(self.sizePolicy)
			self.rbar_btn[i].setFixedWidth(self.sizeWidth_btn)
			self.rbar_btn[i].setFixedHeight(self.sizeHeight_btn)
			
			self.rbar_qlabel2[i].setText(self.tr('合計 : '))
			self.rbar_qlabel2[i].setStyleSheet('''.QLabel {font-family: Arial, Microsoft JhengHei, serif, sans-serif;}''')
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
		self.bbet_btn1.setStyleSheet('''.QPushButton {font-family: Arial, Microsoft JhengHei, serif, sans-serif;}''')
		self.bbet_btn1.setSizePolicy(self.sizePolicy)
		
		self.bbet_qlineedit.setFixedWidth(self.sizeWidth_qlineedit)
		
		self.bbet_btn2.setText(self.tr('列印'))
		self.bbet_btn2.setStyleSheet('''.QPushButton {font-family: Arial, Microsoft JhengHei, serif, sans-serif;}''')
		self.bbet_btn2.setSizePolicy(self.sizePolicy)
		
		self.bbet_qlabel1.setText(self.tr('檯面數 : '))
		self.bbet_qlabel1.setStyleSheet('''.QLabel {font-family: Arial, Microsoft JhengHei, serif, sans-serif;}''')
		self.bbet_qlabel1.setSizePolicy(self.sizePolicy)
		
		self.bbet_qlabel2.setText(self.tr('轉碼 : '))
		self.bbet_qlabel2.setStyleSheet('''.QLabel {font-family: Arial, Microsoft JhengHei, serif, sans-serif;}''')
		self.bbet_qlabel2.setSizePolicy(self.sizePolicy)
		
		# next bet area
		#--------------------------
		self.nbet_qframe.setStyleSheet('''.QFrame {background-color: gray;} .QLabel {background-color: white;}''')
		self.nbet_qframe.setSizePolicy(self.sizePolicy)
		self.nbet_qframe.setFixedWidth(215)
		self.nbet_qframe.setFixedHeight(55)
		
		self.nbet_gl.setSpacing(1)
		self.nbet_gl.setMargin(1)
		
		self.nbet_qlabel1.setText(self.tr('下局注碼'))
		self.nbet_qlabel1.setStyleSheet('''.QLabel {font-family: Arial, Microsoft JhengHei, serif, sans-serif;}''')
		self.nbet_qlabel1.setAlignment(Qt.AlignCenter)
		
		self.nbet_qlabel2.setText(self.tr('總計'))
		self.nbet_qlabel2.setStyleSheet('''.QLabel {font-family: Arial, Microsoft JhengHei, serif, sans-serif;}''')
		self.nbet_qlabel2.setAlignment(Qt.AlignCenter)
		
		self.nbet_qlabel3.setStyleSheet('''.QLabel {font-family: Arial, Microsoft JhengHei, serif, sans-serif;}''')
		self.nbet_qlabel3.setAlignment(Qt.AlignCenter)
		
		self.nbet_qlabel4.setStyleSheet('''.QLabel {font-family: Arial, Microsoft JhengHei, serif, sans-serif;}''')
		self.nbet_qlabel4.setAlignment(Qt.AlignCenter)
		
		self.nbet_qlabel5.setStyleSheet('''.QLabel {font-family: Arial, Microsoft JhengHei, serif, sans-serif;}''')
		self.nbet_qlabel5.setAlignment(Qt.AlignCenter)
		
		# bet inning count area
		#--------------------------
		self.ibet_qframe.setStyleSheet('''.QFrame {background-color: gray;} .QLabel {background-color: white;}''')
		self.ibet_qframe.setSizePolicy(self.sizePolicy)
		self.ibet_qframe.setFixedWidth(215)
		self.ibet_qframe.setFixedHeight(80)
		
		self.ibet_gl.setSpacing(1)
		self.ibet_gl.setMargin(1)
		
		self.ibet_qlabel1.setText('0')
		self.ibet_qlabel1.setAlignment(Qt.AlignCenter)
		self.ibet_qlabel1.setStyleSheet('''.QLabel {color: red; font-family: Arial, Microsoft JhengHei, serif, sans-serif;}''')
		
		self.ibet_qlabel2.setText(self.tr('0\n局'))
		self.ibet_qlabel2.setStyleSheet('''.QLabel {font-family: Arial, Microsoft JhengHei, serif, sans-serif;}''')
		self.ibet_qlabel2.setAlignment(Qt.AlignCenter)
		
		self.ibet_qlabel3.setText('0')
		self.ibet_qlabel3.setStyleSheet('''.QLabel {color: blue; font-family: Arial, Microsoft JhengHei, serif, sans-serif;}''')
		self.ibet_qlabel3.setAlignment(Qt.AlignCenter)
		
		self.ibet_qlabel4.setText('0')
		self.ibet_qlabel4.setStyleSheet('''.QLabel {color: green; font-family: Arial, Microsoft JhengHei, serif, sans-serif;}''')
		self.ibet_qlabel4.setAlignment(Qt.AlignCenter)
		
		self.libet_qframe.setStyleSheet('''.QFrame {background-color: white;} .QLabel {background-color: white;}''')
		
		self.libet_gl.setSpacing(2)
		self.libet_gl.setMargin(2)
		
		self.ibet_qlabel_banker1.setText(self.tr('莊'))
		self.ibet_qlabel_banker1.setStyleSheet('''.QLabel {color: red; font-family: Arial, Microsoft JhengHei, serif, sans-serif;}''')
		self.ibet_qlabel_banker1.setAlignment(Qt.AlignCenter)
		self.ibet_qlabel_banker2.setAlignment(Qt.AlignCenter)
		self.ibet_qlabel_banker3.setAlignment(Qt.AlignCenter)
		self.ibet_qlabel_banker4.setAlignment(Qt.AlignCenter)
		
		self.ibet_qlabel_player1.setText(self.tr('閒'))
		self.ibet_qlabel_player1.setStyleSheet('''.QLabel {color: blue; font-family: Arial, Microsoft JhengHei, serif, sans-serif;}''')
		self.ibet_qlabel_player1.setAlignment(Qt.AlignCenter)
		
		self.ibet_qlabel_tie1.setText(self.tr('和'))
		self.ibet_qlabel_tie1.setStyleSheet('''.QLabel {color: green; font-family: Arial, Microsoft JhengHei, serif, sans-serif;}''')
		self.ibet_qlabel_tie1.setAlignment(Qt.AlignCenter)
		
		
		# bet push button area
		#--------------------------
		self.pbet_qframe.setStyleSheet('''.QFrame {background-color: white; border: 1px solid gray;}''')
		self.pbet_qframe.setSizePolicy(self.sizePolicy)
		self.pbet_qframe.setFixedWidth(215)
		self.pbet_qframe.setFixedHeight(145)
		
		self.pbet_gl.setSpacing(1)
		#self.pbet_gl.setMargin(1)
		
		self.pbet_qlabel1.setText(self.tr('莊'))
		self.pbet_qlabel1.setAlignment(Qt.AlignCenter)
		self.pbet_qlabel1.setFixedWidth(70)
		self.pbet_qlabel1.setFixedHeight(90)
		self.pbet_qlabel1.setStyleSheet('''.QLabel {font-size: 16pt; font-weight:bold; color: white; font-family: Arial, Microsoft JhengHei, serif, sans-serif;
													border-bottom: 1px solid gray; background-image: url(%s);}'''%imgRedBtn)
		#self.pbet_qlabel1.setScaledContents(True)
		#self.pbet_qlabel1.setText('111')
		
		self.pbet_qlabel2.setText(self.tr('和'))
		self.pbet_qlabel2.setAlignment(Qt.AlignCenter)
		self.pbet_qlabel2.setFixedWidth(70)
		self.pbet_qlabel2.setFixedHeight(90)
		self.pbet_qlabel2.setStyleSheet('''.QLabel {font-size: 16pt; font-weight:bold; color: white; font-family: Arial, Microsoft JhengHei, serif, sans-serif;
													border-bottom: 1px solid gray; background-image: url(%s);}'''%imgGreenBtn)
		#self.pbet_qlabel2.setScaledContents(True)
		
		self.pbet_qlabel3.setText(self.tr('閒'))
		self.pbet_qlabel3.setAlignment(Qt.AlignCenter)
		self.pbet_qlabel3.setFixedWidth(70)
		self.pbet_qlabel3.setFixedHeight(90)
		self.pbet_qlabel3.setStyleSheet('''.QLabel {font-size: 16pt; font-weight:bold; color: white; font-family: Arial, Microsoft JhengHei, serif, sans-serif;
													border-bottom: 1px solid gray; background-image: url(%s);}'''%imgBlueBtn)
		#self.pbet_qlabel3.setScaledContents(True)
		
		self.pbet_btn.setText(self.tr('返回'))
		self.pbet_btn.setStyleSheet('''.QPushButton {font-family: Arial, Microsoft JhengHei, serif, sans-serif;}''')
		#self.pbet_btn.setAlignment(Qt.AlignCenter)
		self.pbet_btn.setSizePolicy(self.sizePolicy)
		self.pbet_btn.setFixedWidth(90)
		self.pbet_btn.setFixedHeight(30)
		
		
		# bet record area
		#--------------------------
		self.rbet_qframe.setSizePolicy(self.sizePolicy)
		
		self.rbet_vl.setSpacing(0)
		self.rbet_vl.setMargin(1)
		
		self.rbet_qlabel.setText(self.tr('投注紀錄'))
		self.rbet_qlabel.setStyleSheet('''.QLabel {background-color: white; border-top: 1px solid gray;
											border-left: 1px solid gray; border-right: 1px solid gray;
											font-family: Arial, Microsoft JhengHei, serif, sans-serif;}''')
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
			self.lbar_btn[i].clicked.connect(functools.partial(self.connect_lbar_btn, i))
		
		# initail right bar btn in UIcreate_Grid
		#----------------------------------------------------
		for i in range(4):
			self.rbar_btn[i].clicked.connect(functools.partial(self.connect_rbar_btn, i))
		
		# initail bet and print area in UIcreate_BetStatus
		#----------------------------------------------------
		self.bbet_btn1.clicked.connect(self.connect_bbet_btn1)
		self.bbet_btn2.clicked.connect(self.connect_bbet_btn2)
		
		# initail bet push button area in UIcreate_BetStatus
		#----------------------------------------------------
		clickable(self.pbet_qlabel1).connect(functools.partial(self.connect_pbet_qlabel, Banker))
		clickable(self.pbet_qlabel2).connect(functools.partial(self.connect_pbet_qlabel, Tie))
		clickable(self.pbet_qlabel3).connect(functools.partial(self.connect_pbet_qlabel, Player))
		self.pbet_btn.clicked.connect(self.connect_pbet_btn)
		
		# initail UIcreate_numberInput
		#----------------------------------------------------
		for i in range(4):
			self.binp_btn0[i].clicked.connect(functools.partial(self.connect_binp_btn, i , 0))
			self.binp_btn1[i].clicked.connect(functools.partial(self.connect_binp_btn, i , 1))
			self.binp_btn2[i].clicked.connect(functools.partial(self.connect_binp_btn, i , 2))
			self.binp_btn3[i].clicked.connect(functools.partial(self.connect_binp_btn, i , 3))
			self.binp_btn4[i].clicked.connect(functools.partial(self.connect_binp_btn, i , 4))
			self.binp_btn5[i].clicked.connect(functools.partial(self.connect_binp_btn, i , 5))
			self.binp_btn6[i].clicked.connect(functools.partial(self.connect_binp_btn, i , 6))
			self.binp_btn7[i].clicked.connect(functools.partial(self.connect_binp_btn, i , 7))
			self.binp_btn8[i].clicked.connect(functools.partial(self.connect_binp_btn, i , 8))
			self.binp_btn9[i].clicked.connect(functools.partial(self.connect_binp_btn, i , 9))
			self.binp_btn10[i].clicked.connect(functools.partial(self.connect_binp_btn, i , 10))
			self.binp_btn11[i].clicked.connect(functools.partial(self.connect_binp_btn, i , 11))
	
	def connect_lbar_btn(self, i):
		if self.lbar_btn[i].text().toUtf8() == '手動':
			self.lbar_btn[i].setText(self.tr('確認'))
			self.lbar_qlineedit[i].setText('')
			self.binp_qframe[i].show()
		else:
			self.lbar_btn[i].setText(self.tr('手動'))
			if self.betRecord.gameIsBegin():
				if len(self.lbar_qlineedit[i].text()) > 0:
					img = 0
					bet = int(self.lbar_qlineedit[i].text())
					if self.lbar_qlabel[i].text().toUtf8() == '莊':
						img = 0
					else:
						img = 1
					
					retSug, eraseSug = self.betRecord.manualChangeSug(i, img, bet)
					
					row = eraseSug[0]
					col = eraseSug[1]
					if row >= 0 and col >= 0:
						self.grid_qlabelList[i][row][col].setText('')
						self.grid_qlabelList[i][row][col].setAlignment(Qt.AlignCenter)
						self.grid_qlabelList[i][row][col].setStyleSheet('''.QLabel { font-family: Arial, Microsoft JhengHei, serif, sans-serif;
																			background-image: url(%s);}'''%imgCell)
					
					row = retSug[0]
					col = retSug[1]
					img = retSug[2]
					bet = retSug[3]
					if row >= 0 and col >= 0:
						if img != Tie:
							self.grid_qlabelList[i][row][col].setText(str(bet))
							self.grid_qlabelList[i][row][col].setAlignment(Qt.AlignCenter)
							self.grid_qlabelList[i][row][col].setStyleSheet('''.QLabel { font-family: Arial, Microsoft JhengHei, serif, sans-serif;
																				background-image: url(%s);}'''%self.betRecord.imgSugPath[i][img])
					if i == 0:
						self.initial_nbet(img, bet)
			
			self.binp_qframe[i].close()
	
	# stop and count
	def connect_rbar_btn(self, i):
		print self.rbar_btn[i].text().toUtf8()
	
	def connect_bbet_btn1(self):
		print self.bbet_btn1.text().toUtf8()
	
	def connect_bbet_btn2(self):
		print self.bbet_btn2.text().toUtf8()
	
	def connect_pbet_qlabel(self, winner):
		ret = self.betRecord.bet(winner)
		#print ret
		if ret.get('status') == 0:
			lastSugList = [ret.get('lastSugBig'), ret.get('lastSugEye'), ret.get('lastSugSma'), ret.get('lastSugPen')]
			for i in range(4):
				row = lastSugList[i][0]
				col = lastSugList[i][1]
				img = lastSugList[i][2]
				bet = lastSugList[i][3]
				if row >= 0 and col >= 0:
					if winner != Tie:
						self.grid_qlabelList[i][row][col].setText('')
						self.grid_qlabelList[i][row][col].setAlignment(Qt.AlignCenter)
						self.grid_qlabelList[i][row][col].setStyleSheet('''.QLabel { font-family: Arial, Microsoft JhengHei, serif, sans-serif;
																			background-image: url(%s);}'''%imgCell)
			
			showSugList = [ret.get('SugBig'), ret.get('SugEye'), ret.get('SugSma'), ret.get('SugPen')]
			for i in range(4):
				row = showSugList[i][0]
				col = showSugList[i][1]
				img = showSugList[i][2]
				bet = showSugList[i][3]
				if row >= 0 and col >= 0:
					if winner != Tie:
						if bet == 0:
							self.grid_qlabelList[i][row][col].setText('')
						else:
							self.grid_qlabelList[i][row][col].setText(str(bet))
						
						self.grid_qlabelList[i][row][col].setAlignment(Qt.AlignCenter)
						self.grid_qlabelList[i][row][col].setStyleSheet('''.QLabel { font-family: Arial, Microsoft JhengHei, serif, sans-serif;
																			background-image: url(%s);}'''%self.betRecord.imgSugPath[i][img])
			
			showList = [ret.get('Big'), ret.get('Eye'), ret.get('Sma'), ret.get('Pen')]
			isBet = ret.get('isBet')
			sameBet = ret.get('sameBet')
			countBet = ret.get('countBet')
			for i in range(4):
				row = showList[i][0]
				col = showList[i][1]
				img = showList[i][2]
				if row >= 0 and col >= 0:
					if winner != Tie:
						if isBet[i]:
							if countBet[i] == 0:
								self.grid_qlabelList[i][row][col].setText('')
							else:
								self.grid_qlabelList[i][row][col].setText(str(countBet[i]))
							
							self.grid_qlabelList[i][row][col].setAlignment(Qt.AlignCenter)
							if sameBet[i]:
								self.grid_qlabelList[i][row][col].setStyleSheet('''.QLabel { font-family: Arial, Microsoft JhengHei, serif, sans-serif;
																					background-image: url(%s); color: black}'''%self.betRecord.imgPath[i][img])
							else:
								self.grid_qlabelList[i][row][col].setStyleSheet('''.QLabel { font-family: Arial, Microsoft JhengHei, serif, sans-serif;
																					background-image: url(%s); color: red}'''%self.betRecord.imgPath[i][img])
						else:
							self.grid_qlabelList[i][row][col].setStyleSheet('''.QLabel { font-family: Arial, Microsoft JhengHei, serif, sans-serif;
																					background-image: url(%s); color: black}'''%self.betRecord.imgPath[i][img])
					else:
						self.grid_qlabelList[i][row][col].setAlignment(Qt.AlignCenter)
						self.grid_qlabelList[i][row][col].setStyleSheet('''.QLabel { font-family: Arial, Microsoft JhengHei, serif, sans-serif;
																			background-image: url(%s);}'''%self.betRecord.imgPath[i][Tie][img])
			
			if len(self.betRecord.betCountBig) > 0:
				betCount = [self.betRecord.betCountBig[-1], self.betRecord.betCountEye[-1], self.betRecord.betCountSma[-1], self.betRecord.betCountPen[-1]]
				for i in range(4):
					self.rbar_qlabel1[i].setText(self.tr('小計 : %s' % str(betCount[i])))
			
			self.initial_nbet(showSugList[0][2], showSugList[0][3])
			
		elif ret.get('status') == Still_Tie:
			pass
		
		self.initial_lbar()
		self.initial_ibet()
	
	def connect_pbet_btn(self):
		ret = self.betRecord.backOneStep()
		if ret.get('status') == 0:
			removeList = [ret.get('Big'), ret.get('Eye'), ret.get('Sma'), ret.get('Pen')]
			
			for i in range(4):
				row = removeList[i][0]
				col = removeList[i][1]
				if row >= 0 and col >= 0:
					self.grid_qlabelList[i][row][col].setText('')
					self.grid_qlabelList[i][row][col].setAlignment(Qt.AlignCenter)
					self.grid_qlabelList[i][row][col].setStyleSheet('''.QLabel { font-family: Arial, Microsoft JhengHei, serif, sans-serif;
																		background-image: url(%s);}'''%imgCell)
			
			removeSugList = [ret.get('SugBig'), ret.get('SugEye'), ret.get('SugSma'), ret.get('SugPen')]
			for i in range(4):
				row = removeSugList[i][0]
				col = removeSugList[i][1]
				img = removeSugList[i][2]
				bet = removeSugList[i][3]
				if row >= 0 and col >= 0:
					self.grid_qlabelList[i][row][col].setText('')
					self.grid_qlabelList[i][row][col].setAlignment(Qt.AlignCenter)
					self.grid_qlabelList[i][row][col].setStyleSheet('''.QLabel { font-family: Arial, Microsoft JhengHei, serif, sans-serif;
																		background-image: url(%s);}'''%imgCell)
			
			ShowLastSugList = [ret.get('lastSugBig'), ret.get('lastSugEye'), ret.get('lastSugSma'), ret.get('lastSugPen')]
			for i in range(4):
				row = ShowLastSugList[i][0]
				col = ShowLastSugList[i][1]
				img = ShowLastSugList[i][2]
				bet = ShowLastSugList[i][3]
				if row >= 0 and col >= 0:
					if bet == 0:
						self.grid_qlabelList[i][row][col].setText('')
					else:
						self.grid_qlabelList[i][row][col].setText(str(bet))
					self.grid_qlabelList[i][row][col].setAlignment(Qt.AlignCenter)
					self.grid_qlabelList[i][row][col].setStyleSheet('''.QLabel { font-family: Arial, Microsoft JhengHei, serif, sans-serif;
																		background-image: url(%s);}'''%self.betRecord.imgSugPath[i][img])
			
			if len(self.betRecord.betCountBig) > 0:
				betCount = [self.betRecord.betCountBig[-1], self.betRecord.betCountEye[-1], self.betRecord.betCountSma[-1], self.betRecord.betCountPen[-1]]
				for i in range(4):
					self.rbar_qlabel1[i].setText(self.tr('小計 : %s' % str(betCount[i])))
			
			if removeList[0][0] == 0 and removeList[0][1] == 0:
				self.initial_nbet(-2, -2)
			else:
				self.initial_nbet(ShowLastSugList[0][2], ShowLastSugList[0][3])
			
		elif ret.get('status') == No_Back:
			pass
		elif ret.get('status') == Still_Tie:
			pass
		elif ret.get('status') == Back_From_Tie:
			BackBig = ret.get('Big')
			self.grid_qlabelList[0][BackBig[0]][BackBig[1]].setAlignment(Qt.AlignCenter)
			self.grid_qlabelList[0][BackBig[0]][BackBig[1]].setStyleSheet('''.QLabel { font-family: Arial, Microsoft JhengHei, serif, sans-serif;
																background-image: url(%s);}'''%self.betRecord.imgPath[0][BackBig[2]])
		
		self.initial_lbar()
		self.initial_ibet()
	
	def connect_binp_btn(self, i, number):
		if number in range(10):
			tmp = self.lbar_qlineedit[i].text() + str(number)
			self.lbar_qlineedit[i].setText(tmp)
		elif number == 10:
			self.lbar_qlabel[i].setText(self.tr('莊'))
			self.lbar_qframe[i].setStyleSheet('''.QFrame {background-color: red; border: 1px solid gray;}''')
		elif number == 11:
			self.lbar_qlabel[i].setText(self.tr('閒'))
			self.lbar_qframe[i].setStyleSheet('''.QFrame {background-color: blue; border: 1px solid gray;}''')
	
	def initial_lbar(self):
		for i in range(4):
			self.lbar_qlabel[i].setText(self.tr('莊'))
			self.lbar_btn[i].setText(self.tr('手動'))
			self.binp_qframe[i].close()
	
	def initial_nbet(self, img, bet):
		if img == 0:
			self.nbet_qlabel3.setText(self.tr('莊'))
			self.nbet_qlabel3.setStyleSheet('''.QLabel {color: red; font-family: Arial, Microsoft JhengHei, serif, sans-serif;}''')
			self.nbet_qlabel4.setText(str(bet))
		elif img == 1:
			self.nbet_qlabel3.setText(self.tr('賢'))
			self.nbet_qlabel3.setStyleSheet('''.QLabel {color: blue; font-family: Arial, Microsoft JhengHei, serif, sans-serif;}''')
			self.nbet_qlabel4.setText(str(bet))
		elif img == -1:
			pass
		elif img == -2:
			self.nbet_qlabel3.setText('')
			self.nbet_qlabel4.setText('')
		
		#self.nbet_qlabel5.setText('108')
	
	def initial_ibet(self):
		# predict next status
		nextStatus = self.betRecord.predictNextStatus()
		if nextStatus[0][0] != -1:
			self.ibet_qlabel_banker2.setStyleSheet('''.QLabel {background-image: url(%s)}'''%self.betRecord.imgNextStatusPath[1][nextStatus[0][0]])
		else:
			self.ibet_qlabel_banker2.setStyleSheet('''.QLabel {}''')
		if nextStatus[0][1] != -1:
			self.ibet_qlabel_banker3.setStyleSheet('''.QLabel {background-image: url(%s)}'''%self.betRecord.imgNextStatusPath[2][nextStatus[0][1]])
		else:
			self.ibet_qlabel_banker3.setStyleSheet('''.QLabel {}''')
		if nextStatus[0][2] != -1:
			self.ibet_qlabel_banker4.setStyleSheet('''.QLabel {background-image: url(%s)}'''%self.betRecord.imgNextStatusPath[3][nextStatus[0][2]])
		else:
			self.ibet_qlabel_banker4.setStyleSheet('''.QLabel {}''')
		if nextStatus[1][0] != -1:
			self.ibet_qlabel_player2.setStyleSheet('''.QLabel {background-image: url(%s)}'''%self.betRecord.imgNextStatusPath[1][nextStatus[1][0]])
		else:
			self.ibet_qlabel_player2.setStyleSheet('''.QLabel {}''')
		if nextStatus[1][1] != -1:
			self.ibet_qlabel_player3.setStyleSheet('''.QLabel {background-image: url(%s)}'''%self.betRecord.imgNextStatusPath[2][nextStatus[1][1]])
		else:
			self.ibet_qlabel_player3.setStyleSheet('''.QLabel {}''')
		if nextStatus[1][2] != -1:
			self.ibet_qlabel_player4.setStyleSheet('''.QLabel {background-image: url(%s)}'''%self.betRecord.imgNextStatusPath[3][nextStatus[1][2]])
		else:
			self.ibet_qlabel_player4.setStyleSheet('''.QLabel {}''')
		
		self.ibet_qlabel1.setText(str(self.betRecord.countResult[0]))
		self.ibet_qlabel3.setText(str(self.betRecord.countResult[1]))
		self.ibet_qlabel4.setText(str(self.betRecord.countResult[2]))
		sumRecord = self.betRecord.countResult[0] + self.betRecord.countResult[1] + self.betRecord.countResult[2]
		self.ibet_qlabel2.setText(self.tr(str(sumRecord) + '\n局'))
	
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
			#test_vl.addWidget(QLabel(str(i)))
			test_vl.addWidget(QLabel(''))
		
		self.rbet_qscrollarea.setWidget(test_frame)
		
		#self.status_txt = QLabel(self)
		#movie = QMovie(imgDir + 'sug_big_red_cir.gif')
		#self.status_txt.setMovie(movie)
		#movie.start()
		#self.status_txt.setLayout(QHBoxLayout())
		#self.status_txt.layout().addWidget(QLabel('1'))
		#self.status_txt.setGeometry(QRect(100, 100, 30, 20))
		
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