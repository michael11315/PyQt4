import sys
import copy
import functools
import os
import webbrowser
import time
import datetime
import subprocess
import base64
import random
import traceback

from PyQt4.QtGui import *
from PyQt4.QtCore import *

QTextCodec.setCodecForTr(QTextCodec.codecForName("utf8"))

# image path

imgDir = 'img/'
imgCell = imgDir + 'cell.gif'

imgRedBtn = imgDir + 'red_btn.png'
imgGreenBtn = imgDir + 'green_btn.png'
imgBlueBtn = imgDir + 'blue_btn.png'

imgCirGreen = imgDir + 'cir_green.gif'
imgBigRedCirGreen = imgDir + 'big_red_cir_green.gif'
imgBigBlueCirGreen = imgDir + 'big_blue_cir_green.gif'
imgBigRedCir = imgDir + 'big_red_cir.gif'
imgBigBlueCir = imgDir + 'big_blue_cir.gif'
imgEyeRedCir = imgDir + 'eye_red_cir.gif'
imgEyeBlueCir = imgDir + 'eye_blue_cir.gif'
imgSmaRedCir = imgDir + 'sma_red_cir.gif'
imgSmaBlueCir = imgDir + 'sma_blue_cir.gif'
imgPenRedCir = imgDir + 'pen_red_cir.gif'
imgPenBlueCir = imgDir + 'pen_blue_cir.gif'
# for printG
imgGRedCir = imgDir + 'G_red_cir.gif'
imgGBlueCir = imgDir + 'G_blue_cir.gif'
imgGRedCir_all_the_same = imgDir + 'G_red_cir_1.gif'
imgGBlueCir_all_the_same = imgDir + 'G_blue_cir_1.gif'

imgSugBigRedCir = imgDir + 'sug_big_red_cir.gif'
imgSugBigBlueCir = imgDir + 'sug_big_blue_cir.gif'
imgSugEyeRedCir = imgDir + 'sug_eye_red_cir.gif'
imgSugEyeBlueCir = imgDir + 'sug_eye_blue_cir.gif'
imgSugSmaRedCir = imgDir + 'sug_sma_red_cir.gif'
imgSugSmaBlueCir = imgDir + 'sug_sma_blue_cir.gif'
imgSugPenRedCir = imgDir + 'sug_pen_red_cir.gif'
imgSugPenBlueCir = imgDir + 'sug_pen_blue_cir.gif'

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
Need_Enter_First = 10
Game_End = 11
First_Tie = 20
Still_First_Tie = 21
Back_Still_First_Tie = 22
Back_From_First_Tie = 23

# UI grid size
row_size = 6
column_size = 47

#UI grid road count
road_count = 4

# start time
startTime = ''

# suggestNextBet algorithm
sugAlgorithm = 'A'
# D, E, F print algorithm  based on sugAlgorithm A
printDEFalgorithm = ''
printGalgorithm = ''

LOGLEVEL = 0

class betRecord():
	def __init__(self):
		self.recordAll = []
		self.recordBig = []
		self.recordEye = []
		self.recordSma = []
		self.recordPen = []
		# use record to reference recordBig, recordEye, recordSma, recordPen
		self.record = [self.recordBig, self.recordEye, self.recordSma, self.recordPen]
		
		# self.countResult[0] is the count of Banker
		# self.countResult[1] is the count of Player
		# self.countResult[2] is the count of Tie
		self.countResult = []
		for i in range(3):
			self.countResult.append(0)
		
		# count continuous times for Eye, Sma, Pen
		self.countBig = []
		for i in range(column_size + 1):
			self.countBig.append(0)
		
		self.mapBig = []
		self.mapEye = []
		self.mapSma = []
		self.mapPen = []
		for row in range(row_size):
			tmp = []
			tmp2 = []
			tmp3 = []
			tmp4 = []
			for col in range(column_size + 1):
				tmp.append(-1)
				tmp2.append(-1)
				tmp3.append(-1)
				tmp4.append(-1)
				
			self.mapBig.append(tmp)
			self.mapEye.append(tmp2)
			self.mapSma.append(tmp3)
			self.mapPen.append(tmp4)
		self.map = [self.mapBig, self.mapEye, self.mapSma, self.mapPen]
		
		self.betSugBig = []
		self.betSugBig_sum = []
		self.betSugEye = []
		self.betSugSma = []
		self.betSugPen = []
		# for manualChangeSug, need betSug*_origin to record origin betSug
		self.betSugBig_origin = []
		self.betSugEye_origin = []
		self.betSugSma_origin = []
		self.betSugPen_origin = []
		self.betCountBig = []
		self.betCountEye = []
		self.betCountSma = []
		self.betCountPen = []
		self.betSumCountBig = []
		self.betSumCountEye = []
		self.betSumCountSma = []
		self.betSumCountPen = []
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
		# imgPath[4] -> imgG
		self.imgPath.append([imgGRedCir, imgGBlueCir, imgGRedCir_all_the_same, imgGBlueCir_all_the_same])
		
		self.imgSugPath = []
		if printGalgorithm == '':
			self.imgSugPath.append([imgSugBigRedCir, imgSugBigBlueCir])
			self.imgSugPath.append([imgSugEyeRedCir, imgSugEyeBlueCir])
			self.imgSugPath.append([imgSugSmaRedCir, imgSugSmaBlueCir])
			self.imgSugPath.append([imgSugPenRedCir, imgSugPenBlueCir])
		else:
			self.imgSugPath.append([imgSugBigRedCir, imgSugBigBlueCir])
			self.imgSugPath.append([imgSugBigRedCir, imgSugBigBlueCir])
			self.imgSugPath.append([imgSugEyeRedCir, imgSugEyeBlueCir])
			self.imgSugPath.append([imgSugSmaRedCir, imgSugSmaBlueCir])
			self.imgSugPath.append([imgSugPenRedCir, imgSugPenBlueCir])
		
		self.imgNextStatusPath = []
		self.imgNextStatusPath.append(['', ''])
		self.imgNextStatusPath.append([imgNextStatusEyeRedCir, imgNextStatusEyeBlueCir])
		self.imgNextStatusPath.append([imgNextStatusSmaRedCir, imgNextStatusSmaBlueCir])
		self.imgNextStatusPath.append([imgNextStatusPenRedCir, imgNextStatusPenBlueCir])
		
		self.principal = 0
		self.startGame = False
		self.EndGame = False
		self.principalEntryList = []
		
		self.cutStopStatusBig = []
		self.cutStopStatusEye = []
		self.cutStopStatusSma = []
		self.cutStopStatusPen = []
		
		self.isFirstTie = False
		self.firstTieTimes = 0
		
		self.betSugD = []
		self.betSugE = []
		self.betSugF = []
		self.betSugDEF_sum = []
		
		self.imgG = []
		self.lastPredictCount = []
		
		self.isNotAlgorithmSug = False
	
	def bet(self, winner, isPredict = False):
		if not self.startGame:
			return {'status': Need_Enter_First}
		
		if self.EndGame and not isPredict:
			return {'status': Game_End}
		
		self.countResult[winner] += 1
		if winner != Tie:
			retPos = self.findPos(winner)
			if retPos.get('status') == 0:
				Big = retPos.get('Big')
				Eye = retPos.get('Eye')
				Sma = retPos.get('Sma')
				Pen = retPos.get('Pen')
				
				if Big[1] == column_size - 1 or  Eye[1] == column_size - 1 or  Sma[1] == column_size - 1 or  Pen[1] == column_size - 1:
					self.EndGame = True
				
				self.recordBig.append(Big)
				self.recordEye.append(Eye)
				self.recordSma.append(Sma)
				self.recordPen.append(Pen)
				self.mapBig[Big[0]][Big[1]] = Big[2]
				self.mapEye[Eye[0]][Eye[1]] = Eye[2]
				self.mapSma[Sma[0]][Sma[1]] = Sma[2]
				self.mapPen[Pen[0]][Pen[1]] = Pen[2]
				self.recordAll.append(winner)
				
				# handle about cut stop
				for i in range(4):
					self.cutStopStatusUpdate(i)
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
				self.betSugBig_origin.append(SugBig)
				self.betSugEye_origin.append(SugEye)
				self.betSugSma_origin.append(SugSma)
				self.betSugPen_origin.append(SugPen)
				
				if not isPredict:
					SugBig_sum = self.sumBetInSugBig(Big, SugBig, SugEye, SugSma, SugPen)
					self.betSugBig_sum.append(SugBig_sum)
				else:
					SugBig_sum = SugBig
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
						'SugBig_sum':SugBig_sum, 'lastSugBig_sum':lastSugBig_sum,
						'SugBig': SugBig, 'SugEye': SugEye, 'SugSma': SugSma, 'SugPen': SugPen,
						'lastSugBig': lastSugBig, 'lastSugEye': lastSugEye, 'lastSugSma': lastSugSma, 'lastSugPen': lastSugPen,
						'isBet': isBet, 'sameBet': sameBet, 'countBet': countBet}
		else:
			# handle first record is Tie
			if len(self.recordBig) == 0:
				self.countResult[winner] -= 1
				
				if not self.isFirstTie:
					self.isFirstTie = True
					self.firstTieTimes += 1
					return {'status': First_Tie}
				
				self.firstTieTimes += 1
				return {'status': Still_First_Tie}
			
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
			for i in range(column_size - 1, 0, -1):
				self.countBig[i] = self.countBig[i-1]
			self.countBig[0] = 1
		
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
		
		for col in range(column_size + 1):
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
					for i in range(column_size):
						self.countBig[i] = self.countBig[i+1]
					self.countBig[-1] = 0
				
				lastSug = self.lastSugBet()
				lastSugBig = lastSug.get('lastSugBig')
				lastSugBig_sum = lastSug.get('lastSugBig_sum')
				lastSugEye = lastSug.get('lastSugEye')
				lastSugSma = lastSug.get('lastSugSma')
				lastSugPen = lastSug.get('lastSugPen')
				
				SugBig = self.betSugBig.pop()
				SugBig_sum = self.betSugBig_sum.pop()
				SugEye = self.betSugEye.pop()
				SugSma = self.betSugSma.pop()
				SugPen = self.betSugPen.pop()
				self.betSugBig_origin.pop()
				self.betSugEye_origin.pop()
				self.betSugSma_origin.pop()
				self.betSugPen_origin.pop()
				self.betCountBig.pop()
				self.betCountEye.pop()
				self.betCountSma.pop()
				self.betCountPen.pop()
				self.betSumCountBig.pop()
				self.betSumCountEye.pop()
				self.betSumCountSma.pop()
				self.betSumCountPen.pop()
				self.betStatusBig.pop()
				self.betStatusEye.pop()
				self.betStatusSma.pop()
				self.betStatusPen.pop()
				self.cutStopStatusBig.pop()
				self.cutStopStatusEye.pop()
				self.cutStopStatusSma.pop()
				self.cutStopStatusPen.pop()
				
				return {'status': 0, 'Big': Big, 'Eye': Eye, 'Sma': Sma, 'Pen': Pen,
						'SugBig_sum':SugBig_sum, 'lastSugBig_sum':lastSugBig_sum,
						'SugBig': SugBig, 'SugEye': SugEye, 'SugSma': SugSma, 'SugPen': SugPen,
						'lastSugBig': lastSugBig, 'lastSugEye': lastSugEye, 'lastSugSma': lastSugSma, 'lastSugPen': lastSugPen}
			else:
				if self.recordAll[-1] == Tie:
					return {'status': Still_Tie}
				else:
					Big = self.recordBig[-1]
					return {'status': Back_From_Tie, 'Big': Big}
		else:
			# handle back to first Tie
			if self.isFirstTie:
				self.firstTieTimes -= 1
				
				if self.firstTieTimes != 0:
					return {'status': Back_Still_First_Tie}
				
				self.isFirstTie = False
				return {'status': Back_From_First_Tie}
				
			return {'status': No_Back}
	
	def predictNextStatus(self):
		nextStatus = []
		countImg = []
		
		for i in range(2):
			ret = self.bet(i, isPredict = True)
			if ret.get('status') == Need_Enter_First:
				return {'status': Need_Enter_First}
			
			nextStatus.append((ret.get('Eye')[2], ret.get('Sma')[2], ret.get('Pen')[2]))
			self.backOneStep()
			
			countList = [ret.get('Eye')[2], ret.get('Sma')[2], ret.get('Pen')[2]]
			countBanker = 0
			countPlayer = 0
			for entry in countList:
				if entry == 0:
					countBanker += 1
				elif entry == 1:
					countPlayer += 1
			
			countImg.append((countBanker, countPlayer))
		
		return {'status': 0, 'nextStatus': nextStatus, 'countImg': countImg}
	
	# handle small count and all count
	def storeBetStatus(self, Big, Eye, Sma, Pen):
		LastCutStopStatus = self.getLastCutStopStatus()
		bet = [Big, Eye, Sma, Pen]
		betSug = [self.betSugBig, self.betSugEye, self.betSugSma, self.betSugPen]
		betSug_origin = [self.betSugBig_origin, self.betSugEye_origin, self.betSugSma_origin, self.betSugPen_origin]
		betStatus = [self.betStatusBig, self.betStatusEye, self.betStatusSma, self.betStatusPen]
		betCount = [self.betCountBig, self.betCountEye, self.betCountSma, self.betCountPen]
		betSumCount = [self.betSumCountBig, self.betSumCountEye, self.betSumCountSma, self.betSumCountPen]
		
		for i in range(4):
			#bet status and count
			if len(betSug[i]) == 0:
				betStatus[i].append(-1)
				betCount[i].append(0)
			elif bet[i][2] == -1:
				betStatus[i].append(-1)
				betCount[i].append(betCount[i][-1])
			elif betSug[i][-1][2] == -1:
				betStatus[i].append(-1)
				betCount[i].append(betCount[i][-1])
			elif bet[i][2] == betSug_origin[i][-1][2] and (betSug[i][-1][3] != 0 or betSug_origin[i][-1][3] != 0):
				if betSug_origin[i][-1][3] == 0:
					betStatus[i].append(-1)
				else:
					betStatus[i].append(0)
				
				if LastCutStopStatus[i]:
					betCount[i].append(0)
				else:
					if betSug_origin[i][-1][2] == betSug[i][-1][2]:
						betCount[i].append(betCount[i][-1] + betSug[i][-1][3])
					else:
						betCount[i].append(betCount[i][-1] - betSug[i][-1][3])
			elif bet[i][2] != betSug_origin[i][-1][2] and (betSug[i][-1][3] != 0 or betSug_origin[i][-1][3] != 0):
				if betSug_origin[i][-1][3] == 0:
					betStatus[i].append(-1)
				else:
					betStatus[i].append(1)
				
				if LastCutStopStatus[i]:
					betCount[i].append(0)
				else:
					if betSug_origin[i][-1][2] == betSug[i][-1][2]:
						betCount[i].append(betCount[i][-1] - betSug[i][-1][3])
					else:
						betCount[i].append(betCount[i][-1] + betSug[i][-1][3])
			else:
				betStatus[i].append(-1)
				betCount[i].append(betCount[i][-1])
			
			# bet sum count
			if len(betSug[i]) == 0:
				betSumCount[i].append(0)
			else:
				betSumCount[i].append(betSumCount[i][-1] + betCount[i][-1] - betCount[i][-2])
		
		bet = None
		betSug = None
		betSug_origin = None
		betStatus = None
		betCount = None
		betSumCount = None
	
	def suggestNextBet(self, Big, Eye, Sma, Pen):
		SugBig, SugEye, SugSma, SugPen = (-1, -1, -1, -1), (-1, -1, -1, -1), (-1, -1, -1, -1), (-1, -1, -1, -1)
		Sug = [SugBig, SugEye, SugSma, SugPen]
		if len(self.recordAll) == 0:
			return {'SugBig': SugBig, 'SugEye': SugEye, 'SugSma': SugSma, 'SugPen': SugPen}
		
		LastCutStopStatus = self.getLastCutStopStatus()
		bet = [Big, Eye, Sma, Pen]
		map = [self.mapBig, self.mapEye, self.mapSma, self.mapPen]
		record = [self.recordBig, self.recordEye, self.recordSma, self.recordPen]
		betSug = [self.betSugBig, self.betSugEye, self.betSugSma, self.betSugPen]
		betSug_origin = [self.betSugBig_origin, self.betSugEye_origin, self.betSugSma_origin, self.betSugPen_origin]
		betStatus = [self.betStatusBig, self.betStatusEye, self.betStatusSma, self.betStatusPen]
		
		for i in range(4):
			# algorithm v1
			if sugAlgorithm == 'A' or sugAlgorithm == 'G':
				if bet[i][0] == -1 and bet[i][1] == -1:
					Sug[i] = (-1, -1, -1, -1)
				elif betStatus[i][-1] == -1:
					lastBet = record[i][-1]
					sugBet = 1
					tmp = self.PosNext(map[i], lastBet[0], lastBet[1], lastBet[2])
					Sug[i] = (tmp[0], tmp[1], tmp[2], sugBet)
				elif betStatus[i][-1] == 0:
					lastBet = record[i][-1]
					sugBet = betSug_origin[i][-1][3] + 1
					tmp = self.PosNext(map[i], lastBet[0], lastBet[1], lastBet[2])
					Sug[i] = (tmp[0], tmp[1], tmp[2], sugBet)
				elif betStatus[i][-1] == 1:
					lastBet = record[i][-1]
					if betSug_origin[i][-1][3] > 1:
						sugBet = betSug_origin[i][-1][3] - 1
						tmp = self.PosChangeCol(map[i], lastBet[2])
						Sug[i] = (tmp[0], tmp[1], tmp[2], sugBet)
					else:
						Sug[i] = (-1, -1, lastBet[2], 0)
			# algorithm v2
			elif sugAlgorithm == 'B':
				if bet[i][0] == -1 and bet[i][1] == -1:
					Sug[i] = (-1, -1, -1, -1)
				else:
					lastBet = record[i][-1]
					if lastBet[0] > 0:
						Sug[i] = (-1, -1, lastBet[2], 0)
					else:
						tmp = self.PosNext(map[i], lastBet[0], lastBet[1], lastBet[2])
						sugBet = 1
						for index in range(len(betSug_origin[i])):
							if betSug_origin[i][-1-index][0] != -1 and betSug_origin[i][-1-index][1] != -1:
								if betSug_origin[i][-1-index][2] == bet[i][2]:
									if betSug_origin[i][-1-index][3] == 7:
										continue
									if betStatus[i][-1-index] != 0:
										sugBet = betSug_origin[i][-1-index][3] * 2 + 1
										if sugBet == 7:
											tmp = self.PosChangeCol(map[i], lastBet[2])
										
									break
								elif betSug_origin[i][-1-index][2] != bet[i][2]:
									if betSug_origin[i][-1-index][3] == 7:
										break
									# cut stop at that time
									elif betSug_origin[i][-1-index][3] == 0:
										break
						
						Sug[i] = (tmp[0], tmp[1], tmp[2], sugBet)
			
			if self.isNotAlgorithmSug:
				for i in range(4):
					Sug[i] = (-1, -1, -1, -1)
				
					if bet[i][0] == -1 and bet[i][1] == -1:
						Sug[i] = (-1, -1, -1, -1)
					else:
						Sug[i] = (-1, -1, 0, 0)
			
			# if cut stop now, sugBet still 0
			if LastCutStopStatus[i]:
				sugBet = 0
				if bet[i][0] == -1 and bet[i][1] == -1:
					sugBet = -1
				Sug[i] = (Sug[i][0], Sug[i][1], Sug[i][2], sugBet)
		
		bet = None
		map = None
		record = None
		betSug = None
		betSug_origin = None
		betStatus = None
		
		return {'SugBig': Sug[0], 'SugEye': Sug[1], 'SugSma': Sug[2], 'SugPen': Sug[3]}
	
	def algorithmG(self, winner, noStore = False):
		predictCount = self.predictNextStatus().get('countImg')
		
		img = -1
		all_the_same = False
		if len(self.lastPredictCount) > 0:
			if self.lastPredictCount[-1][winner][0] == 2 and self.lastPredictCount[-1][winner][1] == 1:
				img = 0
			elif self.lastPredictCount[-1][winner][0] != 0 and self.lastPredictCount[-1][winner][1] == 0:
				img = 0
				all_the_same = True
			elif self.lastPredictCount[-1][winner][0] == 1 and self.lastPredictCount[-1][winner][1] == 2:
				img = 1
			elif self.lastPredictCount[-1][winner][1] != 0 and self.lastPredictCount[-1][winner][0] == 0:
				img = 1
				all_the_same = True
		
		if not noStore:
			self.imgG.append(img)
			self.lastPredictCount.append(predictCount)
		
		return {'imgG': img, 'all_the_same': all_the_same}
	
	def algorithmGbackOneStep(self):
		img = self.imgG.pop()
		self.lastPredictCount.pop()
		return {'imgG': img}
	
	def algorithmDEF(self):
		predictCount = self.predictNextStatus().get('countImg')
		ret_D = self.sugAlgorithm_D(predictCount)
		ret_E = self.sugAlgorithm_E(predictCount)
		ret_F = self.sugAlgorithm_F(predictCount)
		
		sugD = ret_D.get('sugD')
		lastSugD = ret_D.get('lastSugD')
		betStatusD = ret_D.get('betStatus')
		
		sugE = ret_E.get('sugE')
		lastSugE = ret_E.get('lastSugE')
		betStatusE = ret_E.get('betStatus')
		
		sugF = ret_F.get('sugF')
		lastSugF = ret_F.get('lastSugF')
		betStatusF = ret_F.get('betStatus')
		
		lastSugList = []
		showSugList = []
		isBet = []
		sameBet = []
		countBet = []
		
		if printDEFalgorithm == 'D':
			lastSugList.append(lastSugD)
			showSugList.append(sugD)
			isBet.append(betStatusD[0])
			sameBet.append(betStatusD[1])
			countBet.append(betStatusD[2])
		elif printDEFalgorithm == 'E':
			lastSugList.append(lastSugE)
			showSugList.append(sugE)
			isBet.append(betStatusE[0])
			sameBet.append(betStatusE[1])
			countBet.append(betStatusE[2])
		elif printDEFalgorithm == 'F':
			lastSugList.append(lastSugF)
			showSugList.append(sugF)
			isBet.append(betStatusF[0])
			sameBet.append(betStatusF[1])
			countBet.append(betStatusF[2])
		
		lastSugList.append(lastSugD)
		showSugList.append(sugD)
		isBet.append(betStatusD[0])
		sameBet.append(betStatusD[1])
		countBet.append(betStatusD[2])
		
		lastSugList.append(lastSugE)
		showSugList.append(sugE)
		isBet.append(betStatusE[0])
		sameBet.append(betStatusE[1])
		countBet.append(betStatusE[2])
		
		lastSugList.append(lastSugF)
		showSugList.append(sugF)
		isBet.append(betStatusF[0])
		sameBet.append(betStatusF[1])
		countBet.append(betStatusF[2])
		
		lastBig = self.recordBig[-1]
		if printDEFalgorithm == 'D':
			SugBig = sugD
		elif printDEFalgorithm == 'E':
			SugBig = sugE
		elif printDEFalgorithm == 'F':
			SugBig = sugF
		
		lastSugDEF_sum = (-1, -1, -1, -1)
		if len(self.betSugDEF_sum) > 0:
			lastSugDEF_sum = self.betSugDEF_sum[-1]
		
		SugDEF_sum = SugBig
		#SugDEF_sum = self.sumBetInSugBig(lastBig, SugBig, sugD, sugE, sugF)
		self.betSugDEF_sum.append(SugDEF_sum)
		
		return {'lastSugList': lastSugList, 'showSugList': showSugList, 'isBet': isBet, 'sameBet': sameBet, 'countBet': countBet, 'SugDEF_sum': SugDEF_sum, 'lastSugDEF_sum': lastSugDEF_sum}
	
	def algorithmDEFbackOneStep(self):
		SugD = self.betSugD.pop()
		SugE = self.betSugE.pop()
		SugF = self.betSugF.pop()
		if printDEFalgorithm == 'D':
			removeSugList = [SugD, SugD, SugE, SugF]
		elif printDEFalgorithm == 'E':
			removeSugList = [SugE, SugD, SugE, SugF]
		elif printDEFalgorithm == 'F':
			removeSugList = [SugF, SugD, SugE, SugF]
		
		lastSugD = (-1, -1, -1, -1)
		lastSugE = (-1, -1, -1, -1)
		lastSugF = (-1, -1, -1, -1)
		if len(self.betSugD) > 0:
			lastSugD = self.betSugD[-1]
		if len(self.betSugE) > 0:
			lastSugE = self.betSugE[-1]
		if len(self.betSugF) > 0:
			lastSugF = self.betSugF[-1]
		
		if printDEFalgorithm == 'D':
			ShowLastSugList = [lastSugD, lastSugD, lastSugE, lastSugF]
		elif printDEFalgorithm == 'E':
			ShowLastSugList = [lastSugE, lastSugD, lastSugE, lastSugF]
		elif printDEFalgorithm == 'F':
			ShowLastSugList = [lastSugF, lastSugD, lastSugE, lastSugF]
		
		return {'removeSugList': removeSugList, 'ShowLastSugList': ShowLastSugList}
	
	def sugAlgorithm_D(self, predictCount):
		# predict sugD
		row, col, img, bet = -1, -1, -1, -1
		if predictCount[0][0] == 2 and predictCount[0][1] == 1:
			img = 0
		elif predictCount[1][0] == 2 and predictCount[1][1] == 1:
			img = 1
		
		if img != -1:
			if len(self.betSugD) > 0:
				for i in range(len(self.betSugD)):
					if self.betSugD[-i][3] not in [0, -1]:
						if self.betSugD[-i][2] != self.recordBig[-i][2]:
							bet = self.betSugD[-i][3] * 2 + 1
							if bet > 15:
								bet = 1
						else:
							bet = 1
						break
					
					if i == len(self.betSugD) -1:
						bet = 1
			else:
				bet = 1
			
			lastBig = self.recordBig[-1]
			if img == lastBig[2]:
				tmp = self.PosNext(self.mapBig, lastBig[0], lastBig[1], lastBig[2])
			else:
				tmp = self.PosChangeCol(self.mapBig, lastBig[2])
			row, col = tmp[0], tmp[1]
		
		# get lastSugD and store sugD
		lastSugD = (-1, -1, -1, -1)
		if len(self.betSugD) > 0:
			lastSugD = self.betSugD[-1]
		self.betSugD.append((row, col, img, bet))
		
		# get bet status
		isBet, sameBet, countBet = False, False, 0
		if lastSugD[2] != -1:
			isBet = True
			if self.recordBig[-1][2] == lastSugD[2]:
				sameBet = True
			countBet = lastSugD[3]
		
		return {'sugD': (row, col, img, bet), 'lastSugD': lastSugD, 'betStatus': (isBet, sameBet, countBet)}
	
	def sugAlgorithm_E(self, predictCount):
		# predict sugE
		row, col, img, bet = -1, -1, -1, -1
		if predictCount[0][0] == 1 and predictCount[0][1] == 2:
			img = 0
		elif predictCount[1][0] == 1 and predictCount[1][1] == 2:
			img = 1
		
		if img != -1:
			if len(self.betSugE) > 0:
				for i in range(len(self.betSugE)):
					if self.betSugE[-i][3] not in [0, -1]:
						if self.betSugE[-i][2] != self.recordBig[-i][2]:
							bet = self.betSugE[-i][3] * 2 + 1
							if bet > 15:
								bet = 1
						else:
							bet = 1
						break
					
					if i == len(self.betSugE) -1:
						bet = 1
			else:
				bet = 1
			
			lastBig = self.recordBig[-1]
			if img == lastBig[2]:
				tmp = self.PosNext(self.mapBig, lastBig[0], lastBig[1], lastBig[2])
			else:
				tmp = self.PosChangeCol(self.mapBig, lastBig[2])
			row, col = tmp[0], tmp[1]
		
		# get lastSugE and store sugE
		lastSugE = (-1, -1, -1, -1)
		if len(self.betSugE) > 0:
			lastSugE = self.betSugE[-1]
		self.betSugE.append((row, col, img, bet))
		
		# get bet status
		isBet, sameBet, countBet = False, False, 0
		if lastSugE[2] != -1:
			isBet = True
			if self.recordBig[-1][2] == lastSugE[2]:
				sameBet = True
			countBet = lastSugE[3]
		
		return {'sugE': (row, col, img, bet), 'lastSugE': lastSugE, 'betStatus': (isBet, sameBet, countBet)}
	
	def sugAlgorithm_F(self, predictCount):
		row, col, img, bet = -1, -1, -1, -1
		lastSugF = (-1, -1, -1, -1)
		isBet, sameBet, countBet = False, False, 0
		
		self.betSugF.append((row, col, img, bet))
		
		return {'sugF': (row, col, img, bet), 'lastSugF': lastSugF, 'betStatus': (isBet, sameBet, countBet)}
	
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
	
	def getSugList(self):
		if len(self.betSugBig) > 0:
			return [self.betSugBig[-1], self.betSugEye[-1], self.betSugSma[-1], self.betSugPen[-1], self.betSugBig_sum[-1]]
		else:
			return [(-1, -1, -1, -1), (-1, -1, -1, -1), (-1, -1, -1, -1), (-1, -1, -1, -1), (-1, -1, -1, -1)]
	
	def sumBetInSugBig(self, Big, SugBig, SugEye, SugSma, SugPen):
		if Big[0] == 0 and Big[1] == 0:
			return SugBig
		
		ret = self.predictNextStatus()
		sumList = [SugEye, SugSma, SugPen]
		imgBig = SugBig[2]
		betBig = SugBig[3]
		for i in range(3):
			if sumList[i][2] != -1:
				if sumList[i][2] == ret['nextStatus'][SugBig[2]][i]:
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
		else:
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
		
		return {'isBet': isBet, 'sameBet': sameBet, 'countBet': countBet}
	
	def manualChangeSug(self, i, img, bet, isManual):
		betSug = [self.betSugBig, self.betSugEye, self.betSugSma, self.betSugPen]
		betSug_origin = [self.betSugBig_origin, self.betSugEye_origin, self.betSugSma_origin, self.betSugPen_origin]
		
		LastCutStopStatus = self.getLastCutStopStatus()
		row, col = -1, -1
		erase_row, rease_col = -1, -1
		
		if len(betSug[i]) != 0 and betSug[i][-1][3] != -1:
			tmp = betSug[i].pop()
			lastBet = self.record[i][-1]
			if img == lastBet[2]:
				sug = self.PosNext(self.map[i], lastBet[0], lastBet[1], lastBet[2])
				row = sug[0]
				col = sug[1]
				erase_row = tmp[0]
				rease_col = tmp[1]
			else:
				sug = self.PosChangeCol(self.map[i], img)
				row = sug[0]
				col = sug[1]
				erase_row = tmp[0]
				rease_col = tmp[1]
			
			if LastCutStopStatus[i]:
				bet = 0
			
			betSug[i].append((row, col, img, bet))
			
			if not isManual:
				betSug_origin[i].pop()
				betSug_origin[i].append((row, col, img, bet))
		
		SugBig_sum = self.sumBetInSugBig(self.recordBig[-1], self.betSugBig[-1], self.betSugEye[-1], self.betSugSma[-1], self.betSugPen[-1])
		SugBig_sum_otherimg = self.betSugBig_sum.pop()
		self.betSugBig_sum.append(SugBig_sum)
		
		betSug = None
		betSug_origin = None
		
		return (row, col, img, bet), (erase_row, rease_col), SugBig_sum, SugBig_sum_otherimg
	
	def getPossibleSugPosition(self):
		PossibleSugPosition = []
		for i in range(4):
			SugPosition = []
			for img in range(2):
				row, col = -1, -1
				lastBet = self.record[i][-1]
				if img == lastBet[2]:
					sugBig = self.PosNext(self.map[i], lastBet[0], lastBet[1], lastBet[2])
					row = sugBig[0]
					col = sugBig[1]
				else:
					sugBig = self.PosChangeCol(self.map[i], img)
					row = sugBig[0]
					col = sugBig[1]
				
				SugPosition.append((row, col))
			
			PossibleSugPosition.append(SugPosition)
		
		return PossibleSugPosition
	
	def gameIsBegin(self):
		if len(self.recordBig) == 0:
			return False
		else:
			return True
	
	def cutStop(self, i):
		betSumCount = [self.betSumCountBig, self.betSumCountEye, self.betSumCountSma, self.betSumCountPen]
		betCount = [self.betCountBig, self.betCountEye, self.betCountSma, self.betCountPen]
		
		cutStatus = False
		# check start game or not
		if len(self.betCountBig) > 0:
			betCount[i][-1] = 0
			self.cutStopStatusUpdate(i, True)
			cutStatus = True
		
		betSumCount = None
		betCount = None
		
		if cutStatus:
			return True
		else:
			return False
	
	def cutStopStatusUpdate(self, i, change = False):
		cutStopStatus = [self.cutStopStatusBig, self.cutStopStatusEye, self.cutStopStatusSma, self.cutStopStatusPen]
		
		if len(cutStopStatus[i]) == 0:
			cutStopStatus[i].append(False)
		else:
			# this is a trigger for cut stop, so just change the last cut stop status
			if change:
				tmpStopStatus = cutStopStatus[i].pop()
				cutStopStatus[i].append(not tmpStopStatus)
			else:
				cutStopStatus[i].append(cutStopStatus[i][-1])
		
		cutStopStatus = None
	
	def getLastCutStopStatus(self):
		if len(self.cutStopStatusBig) > 0:
			return (self.cutStopStatusBig[-1], self.cutStopStatusEye[-1], self.cutStopStatusSma[-1], self.cutStopStatusPen[-1])
		else:
			return (False, False, False, False)
	
	def lastShow(self, i):
		return self.record[i][-1]
	
	def enterPrincipal(self, principal):
		self.principal = principal
		self.startGame = True
	
	def getPrincipal(self):
		return self.principal
	
	def principalAddEntry(self, entry):
		self.principalEntryList.append(entry)
	
	def principalPopEntry(self):
		return self.principalEntryList.pop()
	
	def principalSum(self):
		sum = 0
		for entry in self.principalEntryList:
			sum += entry
		
		return sum
	
	def principalSumPositive(self):
		sum = 0
		for entry in self.principalEntryList:
			if entry > 0:
				sum += entry
		
		return sum
	
	def principalSumNegative(self):
		sum = 0
		for entry in self.principalEntryList:
			if entry < 0:
				sum += entry
		
		return sum
	
	def changeEndGameToFalse(self):
		self.EndGame = False
	
	def setIsNotAlgorithmSug(self, isNotAlgorithmSug):
		self.isNotAlgorithmSug = isNotAlgorithmSug
	
	def logRecord(self):
		if LOGLEVEL != 0:
			path = 'log'
			if not os.path.exists(path):
				os.makedirs(path)
			
			filename = path + '/%s.record' % startTime
			timeNow = time.strftime('%Y%m%d %H:%M:%S', time.localtime(time.time()))
			with open(filename, 'a') as file:
				file.write('[%s]\n' % (timeNow))
				
				map = [self.mapBig, self.mapEye, self.mapSma, self.mapPen]
				note_map = ['mapBig', 'mapEye', 'mapSma', 'mapPen']
				for i in range(4):
					file.write('	%s\n' % note_map[i])
					for map_row in map[i]:
							file.write('		')
							for entry in map_row:
								if entry != -1:
									file.write(' ' + str(entry) + ' ')
								else:
									file.write(str(entry) + ' ')
							file.write('\n')
				
				record = [self.recordAll, self.recordBig, self.recordEye, self.recordSma, self.recordPen]
				note_record = ['recordAll',  'recordBig', 'recordEye', 'recordSma', 'recordPen']
				for i in range(5):
					file.write('	%s\n' % note_record[i])
					count = 0
					for entry in record[i]:
						if count == 0:
							file.write('		')
						
						file.write(str(entry) + ' ')
						count += 1
						
						if count%10 == 0:
							if count != len(record[i]):
								file.write('\n')
								file.write('		')
							else:
								file.write('\n')
						else:
							if count == len(record[i]):
								file.write('\n')
				
				betSug = [self.betSugBig_sum, self.betSugBig, self.betSugEye, self.betSugSma, self.betSugPen]
				note_betSug = ['betSugBig_sum', 'betSugBig', 'betSugEye', 'betSugSma', 'betSugPen']
				
				for i in range(5):
					file.write('	[%s]\n' % note_betSug[i])
					count = 0
					for entry in betSug[i]:
						if count == 0:
							file.write('		')
							
						file.write(str(entry) + ' ')
						count += 1
						
						if count%10 == 0:
							if count != len(betSug[i]):
								file.write('\n')
								file.write('		')
							else:
								file.write('\n')
						else:
							if count == len(betSug[i]):
								file.write('\n')
				
				file.write('\n')
				
				map = None
				note_map = None
				record = None
				note_record = None
				betSug = None
				note_betSug = None

class GridWindow(QWidget):
	def __init__(self, parent = None):
		super(GridWindow, self).__init__(parent)
		
		self.UI_hl = QHBoxLayout(self)
		self.left_qframe = QFrame(self)
		self.left_vl = QVBoxLayout(self.left_qframe)
		self.bet_qframe = QFrame(self)
		self.bet_vl = QVBoxLayout(self.bet_qframe)
		
		# for log
		global startTime
		startTime = time.strftime('%Y%m%d %H-%M-%S', time.localtime(time.time()))
		
		self.betPrincipal = 0
		self.welcomeBaccarat()
		self.sizeDefine()
		self.globalValue()
		self.globalValue2()
		self.UIcreate()
		self.setPrincipal(self.betPrincipal)
		self.checkOnTrail()
		#if not onTrail():
			#sys.exit()
		
		self.logGame('start game')
		
		self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
		UI_width = 239 + column_size * (self.Width_Grid + 1) - 18
		#print UI_width
		UI_height = 683
		
		if printGalgorithm != '':
			UI_height += 171
		
		self.setFixedSize(UI_width, UI_height)
		print self.sizeHint()
		self.vline.setFixedHeight(self.sizeHint().height()-10)
	
	def welcomeBaccarat(self):
		self.Dialog = QDialog()
		self.Dialog.setWindowTitle('welcome Baccarat')
		qlabel1 = QLabel()
		qlabel1.setText(self.tr('請開啟驗證程式以及做好以下設定後按 OK'))
		qlabel2 = QLabel()
		qlabel3 = QLabel()
		qlabel3.setText(self.tr('選擇演算法 : '))
		self.comboBox =  QComboBox()
		self.comboBox.addItem('A')
		self.comboBox.addItem('B')
		self.comboBox.addItem('D')
		self.comboBox.addItem('E')
		self.comboBox.addItem('F')
		self.comboBox.addItem('G')
		qlabel4 = QLabel()
		qlabel4.setText(self.tr('本金 : '))
		self.Lineedit = QLineEdit()
		
		DialogButtonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
		
		dia_vl = QVBoxLayout()
		dia_vl.addWidget(qlabel1)
		dia_vl.addWidget(qlabel2)
		dia_vl.addWidget(qlabel3)
		dia_vl.addWidget(self.comboBox)
		dia_vl.addWidget(qlabel4)
		dia_vl.addWidget(self.Lineedit)
		dia_vl.addWidget(DialogButtonBox)
		self.Dialog.setLayout(dia_vl)
		
		DialogButtonBox.accepted.connect(self.welcomeBaccarat_accept)
		DialogButtonBox.rejected.connect(self.welcomeBaccarat_reject)
		
		self.Dialog.exec_()
	
	def welcomeBaccarat_accept(self):
		algorithm = self.comboBox.currentText()
		number = self.Lineedit.text()
		
		try:
			global sugAlgorithm
			global printDEFalgorithm
			global printGalgorithm
			
			if algorithm in ['A', 'B']:
				sugAlgorithm = algorithm
			elif algorithm in ['G']:
				printGalgorithm = algorithm
				sugAlgorithm = algorithm
			else:
				printDEFalgorithm = algorithm
				sugAlgorithm = 'A'
			
			number = int(number)
			self.betPrincipal = number
			
			self.Dialog.close()
		except:
			#print traceback.format_exc()
			self.Dialog.close()
			self.welcomeBaccarat()

	def welcomeBaccarat_reject(self):
		sys.exit()
	
	def setPrincipal(self, betPrincipal):
		self.betRecord.enterPrincipal(betPrincipal)
		self.bbet_qlabel1.setText(self.tr('檯面數 : %.2f' %betPrincipal))
		self.bbet_qlineedit.setText(str(betPrincipal))
		self.bbet_qlineedit.setReadOnly(True)
	
	def checkOnTrail(self):
		OnTrail = False
		
		path = 'C:/Python/record/OnTrail'
		if os.path.exists(path):
			try:
				with open(path, 'r') as file:
					lines = file.readlines()
					timeOnTrail_str = base64.b64decode(lines[0]).split(':')[1]
					timeOnTrail_year = int(timeOnTrail_str[0:4])
					timeOnTrail_month = int(timeOnTrail_str[4:6])
					timeOnTrail_day = int(timeOnTrail_str[6:8])
					timeOnTrail = datetime.date(timeOnTrail_year, timeOnTrail_month, timeOnTrail_day)
					
					timeNow_str = time.strftime('%Y%m%d', time.localtime(time.time()))
					timeNow_year = int(timeNow_str[0:4])
					timeNow_month = int(timeNow_str[4:6])
					timeNow_day = int(timeNow_str[6:8])
					timeNow = datetime.date(timeNow_year, timeNow_month, timeNow_day)
					
					delta = timeNow - timeOnTrail
					if timeNow >= timeOnTrail and delta.days <= 15:
						OnTrail = True
			except:
				OnTrail = False
		
		last_time_use = 'C:/Python/record/Record'
		if os.path.exists(last_time_use):
			try:
				with open(last_time_use, 'r') as file:
					lines = file.readlines()
					timeRecord_str = base64.b64decode(lines[0]).split(':')[1]
					timeRecord_year = int(timeRecord_str[0:4])
					timeRecord_month = int(timeRecord_str[4:6])
					timeRecord_day = int(timeRecord_str[6:8])
					timeRecord_hour = int(timeRecord_str[8:10])
					timeRecord_minute = int(timeRecord_str[10:12])
					timeRecord_second = int(timeRecord_str[12:14])
					timeRecord = datetime.datetime(timeRecord_year, timeRecord_month, timeRecord_day, timeRecord_hour, timeRecord_minute, timeRecord_second)
					
					timeNow_str = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
					timeNow_year = int(timeNow_str[0:4])
					timeNow_month = int(timeNow_str[4:6])
					timeNow_day = int(timeNow_str[6:8])
					timeNow_hour = int(timeNow_str[8:10])
					timeNow_minute = int(timeNow_str[10:12])
					timeNow_second = int(timeNow_str[12:14])
					timeNow = datetime.datetime(timeNow_year, timeNow_month, timeNow_day, timeNow_hour, timeNow_minute, timeNow_second)
					
					if timeNow < timeRecord:
						OnTrail = False
			except:
				OnTrail = False
		else:
			OnTrail = False
		
		if not OnTrail:
			msgBox = QMessageBox(self)
			msgBox.setIcon(QMessageBox.Information)
			msgBox.setText(self.tr('請使用驗證程式'))
			msgBox.exec_()
			sys.exit()
	
	def checkAndUpdateLastTime(self):
		last_time_use = 'C:/Python/record/Record'
		if os.path.exists(last_time_use):
			try:
				with open(last_time_use, 'r') as file:
					lines = file.readlines()
					timeRecord_str = base64.b64decode(lines[0]).split(':')[1]
					timeRecord_year = int(timeRecord_str[0:4])
					timeRecord_month = int(timeRecord_str[4:6])
					timeRecord_day = int(timeRecord_str[6:8])
					timeRecord_hour = int(timeRecord_str[8:10])
					timeRecord_minute = int(timeRecord_str[10:12])
					timeRecord_second = int(timeRecord_str[12:14])
					timeRecord = datetime.datetime(timeRecord_year, timeRecord_month, timeRecord_day, timeRecord_hour, timeRecord_minute, timeRecord_second)
					
					timeNow_str = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
					timeNow_year = int(timeNow_str[0:4])
					timeNow_month = int(timeNow_str[4:6])
					timeNow_day = int(timeNow_str[6:8])
					timeNow_hour = int(timeNow_str[8:10])
					timeNow_minute = int(timeNow_str[10:12])
					timeNow_second = int(timeNow_str[12:14])
					timeNow = datetime.datetime(timeNow_year, timeNow_month, timeNow_day, timeNow_hour, timeNow_minute, timeNow_second)
					
					if timeNow < timeRecord:
						return False
					else:
						Record = str(random.randint(100, 1000)) + time.strftime(':%Y%m%d%H%M%S', time.localtime(time.time()))
						with open(last_time_use, 'w') as file:
							file.write(base64.b64encode(Record))
						return True
			except:
				#print traceback.format_exc()
				return False
	
	def gameEndMessage(self):
		msgBox = QMessageBox(self)
		msgBox.setIcon(QMessageBox.Information)
		msgBox.setText(self.tr('記錄已到上限，請另開新局'))
		msgBox.exec_()
	
	def globalValue(self):
		self.betRecord = betRecord()
		if printGalgorithm != '':
			self.betRecord.setIsNotAlgorithmSug(True)
		self.listForMovie = [(-1, -1, -1, -1), (-1, -1, -1, -1), (-1, -1, -1, -1), (-1, -1, -1, -1)]
		self.recordHtml_list = []
	
	def globalValue2(self):
		if printGalgorithm != '':
			self.betRecord_G = betRecord()
			number = self.betRecord.getPrincipal()
			self.betRecord_G.enterPrincipal(number)
			
			global road_count
			road_count = 5
	
	def sizeDefine(self):
		# special size define
		self.Width_Grid = 23
		self.Height_Grid = 23
		self.Width_BetStatus = 215
		self.Height_BetStatus_rbet_qscroll = 243
		if printGalgorithm != '':
			self.Height_BetStatus_rbet_qscroll += 171
		self.binp_btnWidth = 37
		self.binp_btnHeight = 30
		self.Width_rbar = 400
		self.Height_tbar = 24
		self.Width_trbet_space = 25
		
		# general size define
		self.count = 0
		self.sizeWidth_qlabel = 60
		self.sizeHeight_qlabel = 22
		self.sizeWidth_btn = 70
		self.sizeHeight_btn = 22
		self.sizeWidth_qlineedit = 60
		self.sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
		self.sizeFontSize_Label = 12
		self.sizeFontSize_Button = 11
		self.sizeFontSize_Grid = 11
	
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
		
		for i in range(road_count):
			self.left_vl.addWidget(self.bar_qframe[i])
			self.left_vl.addWidget(self.grid_qframe[i])
		self.left_qframe.setLayout(self.left_vl)
	
	def UIcreate_GridLayout(self):
		# global data
		self.grid_qframe = []
		self.grid_gl = []
		self.grid_qlabelList = []
		
		# grid layout
		for i in range(road_count):
			# initial grid form
			self.grid_qframe.append(QFrame(self.left_qframe))
			self.grid_gl.append(QGridLayout(self.grid_qframe[i]))
			
			# initial each grid and set in gridlayout
			tmp = []
			for row in range(6):
				tmprow = []
				for col in range(column_size):
					tmprow.append(QLabel(self.grid_qframe[i]))
					imgGif = QMovie(imgCell)
					tmprow[len(tmprow)-1].setMovie(imgGif)
					tmprow[len(tmprow)-1].setFixedWidth(self.Width_Grid)
					tmprow[len(tmprow)-1].setFixedHeight(self.Height_Grid)
					tmprow[len(tmprow)-1].movie().start()
					tmprow[len(tmprow)-1].movie().stop()
					tmprow[len(tmprow)-1].setScaledContents(True)
					
					tmprow_hl = QHBoxLayout()
					tmprow_hl.setMargin(0)
					tmprow_hl.setSpacing(0)
					tmprow_qlabel = QLabel()
					tmprow_qlabel.setAlignment(Qt.AlignCenter)
					tmprow_qlabel.setStyleSheet('''.QLabel { background: transparent; font-family: Arial, Microsoft JhengHei, serif, sans-serif;}''')
					tmprow[len(tmprow)-1].setLayout(tmprow_hl)
					tmprow[len(tmprow)-1].layout().addWidget(tmprow_qlabel)
					
					self.grid_gl[i].addWidget(tmprow[len(tmprow)-1], row, col)
				
				tmp.append(tmprow)
			
			self.grid_qlabelList.append(tmp)
			
			# set relationship
			self.grid_qframe[i].setLayout(self.grid_gl[i])
	
	def UIcreate_GridBar(self):
		# full bar global data
		self.bar_qframe = []
		self.bar_hl = []
		
		for i in range(road_count):
			self.bar_qframe.append(QFrame(self.left_qframe))
			self.bar_hl.append(QHBoxLayout(self.bar_qframe[i]))
		
		# bar's title
		#----------------------------------------------------
		self.tbar_qframe = []
		self.tbar_hl = []
		self.tbar_qlabel = []
		
		for i in range(road_count):
			# initial title bar
			self.tbar_qframe.append(QFrame(self.bar_qframe[i]))
			self.tbar_hl.append(QHBoxLayout(self.tbar_qframe[i]))
			self.tbar_qlabel.append(QLabel(self.tbar_qframe[i]))
			
			# set relationship
			self.tbar_hl[i].addWidget(self.tbar_qlabel[i])
			self.tbar_qframe[i].setLayout(self.tbar_hl[i])
			self.bar_hl[i].addWidget(QFrame())
			self.bar_hl[i].addWidget(self.tbar_qframe[i])
		
		# left bar's global data
		#----------------------------------------------------
		self.lbar_qframe = []
		self.lbar_hl = []
		self.lbar_qlabel = []
		self.lbar_btn = []
		self.lbar_qlineedit = []
		
		for i in range(road_count):
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
		
		for i in range(road_count):
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
		self.pbet_qlabel2 = QLabel(self.pbet_qframe)
		self.pbet_qlabel3 = QLabel(self.pbet_qframe)
		self.pbet_btn = QPushButton(self.pbet_qframe)
		self.pbet_btn_allcut = QPushButton(self.pbet_qframe)
		
		# set relationship
		self.pbet_qframe.setLayout(self.pbet_gl)
		self.pbet_gl.addWidget(self.pbet_qlabel1, 0, 0, 2, 2)
		self.pbet_gl.addWidget(self.pbet_qlabel2, 0, 2, 2, 2)
		self.pbet_gl.addWidget(self.pbet_qlabel3, 0, 4, 2, 2)
		self.pbet_gl.addWidget(self.pbet_btn, 2, 0, 1, 3, Qt.AlignCenter)
		self.pbet_gl.addWidget(self.pbet_btn_allcut, 2, 3, 1, 3, Qt.AlignCenter)
		self.bet_vl.addWidget(self.pbet_qframe)
		
		# bet record area
		#----------------------------------------------------
		# initial
		self.rbet_qframe = QFrame(self.bet_qframe)
		self.rbet_vl = QVBoxLayout(self.rbet_qframe)
		self.rbet_qlabel = QLabel(self.rbet_qframe)
		self.rbet_qscrollarea = QScrollArea(self.rbet_qframe)
		self.rbet_qscrollarea_qframe = QFrame(self.rbet_qscrollarea)
		self.rbet_qscrollarea_vl = QVBoxLayout(self.rbet_qscrollarea_qframe)
		
		self.trbet_qframe = QFrame(self.rbet_qframe)
		self.trbet_hl = QHBoxLayout(self.trbet_qframe)
		self.trbet_qlabel1 = QLabel(self.trbet_qframe)
		self.trbet_qlabel2 = QLabel(self.trbet_qframe)
		self.trbet_qlabel3 = QLabel(self.trbet_qframe)
		self.trbet_qlabel4 = QLabel(self.trbet_qframe)
		self.trbet_qlabelspace = QLabel(self.trbet_qframe)
		
		# set relationship
		self.rbet_qframe.setLayout(self.rbet_vl)
		self.rbet_vl.addWidget(self.rbet_qlabel)
		self.rbet_vl.addWidget(self.trbet_qframe)
		self.rbet_vl.addWidget(self.rbet_qscrollarea)
		self.bet_vl.addWidget(self.rbet_qframe)
		self.rbet_qscrollarea.setWidget(self.rbet_qscrollarea_qframe)
		self.rbet_qscrollarea.setWidgetResizable(True)
		#self.rbet_qscrollarea_qframe.setLayout(self.rbet_qscrollarea_vl)
		
		self.trbet_qframe.setLayout(self.trbet_hl)
		self.trbet_hl.addWidget(self.trbet_qlabel1)
		self.trbet_hl.addWidget(self.trbet_qlabel2)
		self.trbet_hl.addWidget(self.trbet_qlabel3)
		self.trbet_hl.addWidget(self.trbet_qlabel4)
		self.trbet_hl.addWidget(self.trbet_qlabelspace)
	
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
		self.binp_btn12 = []
		self.binp_btn13 = []
		
		for i in range(road_count):
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
			self.binp_btn12.append(QPushButton(self.binp_qframe[i]))
			self.binp_btn13.append(QPushButton(self.binp_qframe[i]))
			
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
			self.binp_gl[i].addWidget(self.binp_btn12[i], 0, 3, 2, 1)
			self.binp_gl[i].addWidget(self.binp_btn13[i], 2, 3, 2, 1)
	
	def initialGlobalAttribute(self):
		# initail global values of UIcreate
		#----------------------------------------------------
		self.UI_hl.setSpacing(1)
		self.UI_hl.setMargin(0)
		self.left_vl.setSpacing(1)
		self.left_vl.setMargin(0)
		
		# initail global values of UIcreate_GridLayout
		#----------------------------------------------------
		for i in range(road_count):
			self.grid_qframe[i].setStyleSheet('''.QFrame {background-color: gray;}''')
			
			self.grid_gl[i].setSpacing(1)
			self.grid_gl[i].setMargin(1)
		
		# initail global values of UIcreate_BarForGrid
		#----------------------------------------------------
		for i in range(road_count):
			self.bar_hl[i].setMargin(0)
		
		# bar's title
		#--------------------------
		for i in range(road_count):
			self.tbar_hl[i].setSpacing(1)
			self.tbar_hl[i].setMargin(0)
			self.tbar_qlabel[i].setStyleSheet('''.QLabel {font-size: %dpt; font-family: Arial, Microsoft JhengHei, serif, sans-serif;}''' % self.sizeFontSize_Label)
			self.tbar_qlabel[i].setAlignment(Qt.AlignRight | Qt.AlignVCenter)
			self.tbar_qlabel[i].setFixedHeight(self.Height_tbar)
		
		self.tbar_qlabel[0].setText(self.tr('下局預測  大路'))
		self.tbar_qlabel[1].setText(self.tr('下局預測  眼路'))
		self.tbar_qlabel[2].setText(self.tr('下局預測  小路'))
		self.tbar_qlabel[3].setText(self.tr('下局預測  筆路'))
		
		if printGalgorithm != '':
			self.tbar_qlabel[1].setText(self.tr('下局預測  紅藍路'))
			self.tbar_qlabel[2].setText(self.tr('下局預測  眼路'))
			self.tbar_qlabel[3].setText(self.tr('下局預測  小路'))
			self.tbar_qlabel[4].setText(self.tr('下局預測  筆路'))
		
		# left bar
		#--------------------------
		for i in range(road_count):
			self.lbar_qframe[i].setStyleSheet('''.QFrame {background-color: gray; border: 1px solid gray;}''')
			self.lbar_qframe[i].setSizePolicy(self.sizePolicy)
			
			self.lbar_hl[i].setSpacing(1)
			self.lbar_hl[i].setMargin(0)
			
			self.lbar_qlabel[i].setText('')
			self.lbar_qlabel[i].setStyleSheet('''.QLabel {font-size: %dpt; color: white; font-family: Arial, Microsoft JhengHei, serif, sans-serif;}''' % self.sizeFontSize_Label)
			self.lbar_qlabel[i].setAlignment(Qt.AlignCenter)
			self.lbar_qlabel[i].setSizePolicy(self.sizePolicy)
			self.lbar_qlabel[i].setFixedWidth(self.sizeWidth_qlabel)
			self.lbar_qlabel[i].setFixedHeight(self.sizeHeight_qlabel)
			
			self.lbar_btn[i].setText(self.tr('手動'))
			self.lbar_btn[i].setStyleSheet('''.QPushButton {font-size: %dpt; font-family: Arial, Microsoft JhengHei, serif, sans-serif;}''' % self.sizeFontSize_Button)
			self.lbar_btn[i].setSizePolicy(self.sizePolicy)
			self.lbar_btn[i].setFixedWidth(self.sizeWidth_btn)
			self.lbar_btn[i].setFixedHeight(self.sizeHeight_btn)
			
			self.lbar_qlineedit[i].setStyleSheet('''.QLineEdit {font-size: %dpt; color: black; font-family: Arial, Microsoft JhengHei, serif, sans-serif;}''' % self.sizeFontSize_Label)
			self.lbar_qlineedit[i].setSizePolicy(self.sizePolicy)
			self.lbar_qlineedit[i].setFixedWidth(self.sizeWidth_qlabel)
			self.lbar_qlineedit[i].setFixedHeight(self.sizeHeight_qlabel)
			self.lbar_qlineedit[i].setReadOnly(True)
		
		# right bar
		#--------------------------
		for i in range(road_count):
			self.rbar_qframe[i].setStyleSheet('''.QFrame {border: 1px solid gray;}''')
			self.rbar_qframe[i].setSizePolicy(self.sizePolicy)
			self.rbar_qframe[i].setFixedWidth(self.Width_rbar)
			
			self.rbar_hl[i].setSpacing(0)
			self.rbar_hl[i].setMargin(0)
			
			self.rbar_qlabel1[i].setText(self.tr(' 小計 : '))
			self.rbar_qlabel1[i].setStyleSheet('''.QLabel {font-size: %dpt; font-family: Arial, Microsoft JhengHei, serif, sans-serif;}''' % self.sizeFontSize_Label)
			self.rbar_qlabel1[i].setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
			self.rbar_qlabel1[i].setSizePolicy(self.sizePolicy)
			#self.rbar_qlabel1[i].setFixedWidth(self.sizeWidth_qlabel)
			self.rbar_qlabel1[i].setFixedHeight(self.sizeHeight_qlabel)
			
			self.rbar_btn[i].setText(self.tr('停止'))
			self.rbar_btn[i].setStyleSheet('''.QPushButton {font-size: %dpt; font-family: Arial, Microsoft JhengHei, serif, sans-serif;}''' % self.sizeFontSize_Button)
			self.rbar_btn[i].setSizePolicy(self.sizePolicy)
			self.rbar_btn[i].setFixedWidth(self.sizeWidth_btn)
			self.rbar_btn[i].setFixedHeight(self.sizeHeight_btn)
			
			self.rbar_qlabel2[i].setText(self.tr(' 合計 : '))
			self.rbar_qlabel2[i].setStyleSheet('''.QLabel {font-size: %dpt; font-family: Arial, Microsoft JhengHei, serif, sans-serif;}''' % self.sizeFontSize_Label)
			self.rbar_qlabel2[i].setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
			self.rbar_qlabel2[i].setSizePolicy(self.sizePolicy)
			#self.rbar_qlabel2[i].setFixedWidth(self.sizeWidth_qlabel)
			self.rbar_qlabel2[i].setFixedHeight(self.sizeHeight_qlabel)
		
		# initail global values of UIcreate_BetStatus
		#----------------------------------------------------
		self.bet_vl.setSpacing(10)
		self.bet_vl.setMargin(0)
		
		# bet and print area
		#--------------------------
		self.bbet_qframe.setStyleSheet('''.QFrame {border: 1px solid gray;}''')
		self.bbet_qframe.setSizePolicy(self.sizePolicy)
		self.bbet_qframe.setFixedWidth(self.Width_BetStatus)
		self.bbet_qframe.setFixedHeight(80)
		
		self.bbet_gl.setSpacing(1)
		self.bbet_gl.setMargin(0)
		
		self.bbet_btn1.setText(self.tr('新局'))
		self.bbet_btn1.setStyleSheet('''.QPushButton {font-size: %dpt; font-family: Arial, Microsoft JhengHei, serif, sans-serif;}''' % self.sizeFontSize_Button)
		self.bbet_btn1.setSizePolicy(self.sizePolicy)
		self.bbet_btn1.setFixedWidth(self.sizeWidth_btn)
		self.bbet_btn1.setFixedHeight(self.sizeHeight_btn)
		
		self.bbet_qlineedit.setStyleSheet('''.QLineEdit {font-size: %dpt; color: black; font-family: Arial, Microsoft JhengHei, serif, sans-serif;}''' % self.sizeFontSize_Label)
		self.bbet_qlineedit.setFixedWidth(self.sizeWidth_qlineedit)
		
		self.bbet_btn2.setText(self.tr('列印'))
		self.bbet_btn2.setStyleSheet('''.QPushButton {font-size: %dpt; font-family: Arial, Microsoft JhengHei, serif, sans-serif;}''' % self.sizeFontSize_Button)
		self.bbet_btn2.setSizePolicy(self.sizePolicy)
		self.bbet_btn2.setFixedWidth(self.sizeWidth_btn)
		self.bbet_btn2.setFixedHeight(self.sizeHeight_btn)
		
		self.bbet_qlabel1.setText(self.tr('檯面數 : '))
		self.bbet_qlabel1.setStyleSheet('''.QLabel {font-size: %dpt; font-family: Arial, Microsoft JhengHei, serif, sans-serif;}''' % self.sizeFontSize_Label)
		self.bbet_qlabel1.setSizePolicy(self.sizePolicy)
		self.bbet_qlabel1.setFixedHeight(self.sizeHeight_qlabel)
		
		self.bbet_qlabel2.setText(self.tr('轉碼 : '))
		self.bbet_qlabel2.setStyleSheet('''.QLabel {font-size: %dpt; font-family: Arial, Microsoft JhengHei, serif, sans-serif;}''' % self.sizeFontSize_Label)
		self.bbet_qlabel2.setSizePolicy(self.sizePolicy)
		self.bbet_qlabel2.setFixedHeight(self.sizeHeight_qlabel)
		
		# next bet area
		#--------------------------
		self.nbet_qframe.setStyleSheet('''.QFrame {background-color: gray; border: 1px solid gray;} .QLabel {background-color: white;}''')
		self.nbet_qframe.setSizePolicy(self.sizePolicy)
		self.nbet_qframe.setFixedWidth(self.Width_BetStatus)
		self.nbet_qframe.setFixedHeight(55)
		
		self.nbet_gl.setSpacing(1)
		self.nbet_gl.setMargin(0)
		
		self.nbet_qlabel1.setText(self.tr('下局注碼'))
		self.nbet_qlabel1.setStyleSheet('''.QLabel {font-size: %dpt; font-family: Arial, Microsoft JhengHei, serif, sans-serif;}''' % self.sizeFontSize_Label)
		self.nbet_qlabel1.setAlignment(Qt.AlignCenter)
		
		self.nbet_qlabel2.setText(self.tr('總計'))
		self.nbet_qlabel2.setStyleSheet('''.QLabel {font-size: %dpt; font-family: Arial, Microsoft JhengHei, serif, sans-serif;}''' % self.sizeFontSize_Label)
		self.nbet_qlabel2.setAlignment(Qt.AlignCenter)
		
		self.nbet_qlabel3.setStyleSheet('''.QLabel {font-size: %dpt; font-family: Arial, Microsoft JhengHei, serif, sans-serif;}''' % self.sizeFontSize_Label)
		self.nbet_qlabel3.setAlignment(Qt.AlignCenter)
		
		self.nbet_qlabel4.setStyleSheet('''.QLabel {font-size: %dpt; font-family: Arial, Microsoft JhengHei, serif, sans-serif;}''' % self.sizeFontSize_Label)
		self.nbet_qlabel4.setAlignment(Qt.AlignCenter)
		
		self.nbet_qlabel5.setStyleSheet('''.QLabel {font-size: %dpt; font-family: Arial, Microsoft JhengHei, serif, sans-serif;}''' % self.sizeFontSize_Label)
		self.nbet_qlabel5.setAlignment(Qt.AlignCenter)
		
		# bet inning count area
		#--------------------------
		self.ibet_qframe.setStyleSheet('''.QFrame {background-color: gray; border: 1px solid gray;} .QLabel {background-color: white;}''')
		self.ibet_qframe.setSizePolicy(self.sizePolicy)
		self.ibet_qframe.setFixedWidth(self.Width_BetStatus)
		self.ibet_qframe.setFixedHeight(80)
		
		self.ibet_gl.setSpacing(1)
		self.ibet_gl.setMargin(0)
		
		self.ibet_qlabel1.setText('0')
		self.ibet_qlabel1.setAlignment(Qt.AlignCenter)
		self.ibet_qlabel1.setStyleSheet('''.QLabel {font-size: %dpt; color: red; font-family: Arial, Microsoft JhengHei, serif, sans-serif;}''' % self.sizeFontSize_Label)
		
		self.ibet_qlabel2.setText(self.tr('0\n局'))
		self.ibet_qlabel2.setStyleSheet('''.QLabel {font-size: %dpt; font-family: Arial, Microsoft JhengHei, serif, sans-serif;}''' % self.sizeFontSize_Label)
		self.ibet_qlabel2.setAlignment(Qt.AlignCenter)
		
		self.ibet_qlabel3.setText('0')
		self.ibet_qlabel3.setStyleSheet('''.QLabel {font-size: %dpt; color: blue; font-family: Arial, Microsoft JhengHei, serif, sans-serif;}''' % self.sizeFontSize_Label)
		self.ibet_qlabel3.setAlignment(Qt.AlignCenter)
		
		self.ibet_qlabel4.setText('0')
		self.ibet_qlabel4.setStyleSheet('''.QLabel {font-size: %dpt; color: green; font-family: Arial, Microsoft JhengHei, serif, sans-serif;}''' % self.sizeFontSize_Label)
		self.ibet_qlabel4.setAlignment(Qt.AlignCenter)
		
		self.libet_qframe.setStyleSheet('''.QFrame {background-color: white; border: 0px;} .QLabel {background-color: white;}''')
		
		self.libet_gl.setSpacing(0)
		self.libet_gl.setMargin(0)
		
		self.ibet_qlabel_banker1.setText(self.tr('莊'))
		self.ibet_qlabel_banker1.setStyleSheet('''.QLabel {font-size: %dpt; color: red; font-family: Arial, Microsoft JhengHei, serif, sans-serif;}''' % self.sizeFontSize_Label)
		self.ibet_qlabel_banker1.setAlignment(Qt.AlignCenter)
		self.ibet_qlabel_banker2.setAlignment(Qt.AlignCenter)
		self.ibet_qlabel_banker3.setAlignment(Qt.AlignCenter)
		self.ibet_qlabel_banker4.setAlignment(Qt.AlignCenter)
		
		self.ibet_qlabel_player1.setText(self.tr('閒'))
		self.ibet_qlabel_player1.setStyleSheet('''.QLabel {font-size: %dpt; color: blue; font-family: Arial, Microsoft JhengHei, serif, sans-serif;}''' % self.sizeFontSize_Label)
		self.ibet_qlabel_player1.setAlignment(Qt.AlignCenter)
		
		self.ibet_qlabel_tie1.setText(self.tr('和'))
		self.ibet_qlabel_tie1.setStyleSheet('''.QLabel {font-size: %dpt; color: green; font-family: Arial, Microsoft JhengHei, serif, sans-serif;}''' % self.sizeFontSize_Label)
		self.ibet_qlabel_tie1.setAlignment(Qt.AlignCenter)
		
		
		# bet push button area
		#--------------------------
		self.pbet_qframe.setStyleSheet('''.QFrame {background-color: white; border: 1px solid gray;}''')
		self.pbet_qframe.setSizePolicy(self.sizePolicy)
		self.pbet_qframe.setFixedWidth(self.Width_BetStatus)
		self.pbet_qframe.setFixedHeight(125)
		
		self.pbet_gl.setSpacing(0)
		self.pbet_gl.setMargin(0)
		
		self.pbet_qlabel1.setText(self.tr('莊'))
		self.pbet_qlabel1.setAlignment(Qt.AlignCenter)
		self.pbet_qlabel1.setFixedWidth(71)
		self.pbet_qlabel1.setFixedHeight(90)
		self.pbet_qlabel1.setStyleSheet('''.QLabel {font-size: 16pt; font-weight:bold; color: white; font-family: Arial, Microsoft JhengHei, serif, sans-serif;
													border-bottom: 1px solid gray; background-image: url(%s);}''' % imgRedBtn)
		#self.pbet_qlabel1.setScaledContents(True)
		
		self.pbet_qlabel2.setText(self.tr('和'))
		self.pbet_qlabel2.setAlignment(Qt.AlignCenter)
		self.pbet_qlabel2.setFixedWidth(71)
		self.pbet_qlabel2.setFixedHeight(90)
		self.pbet_qlabel2.setStyleSheet('''.QLabel {font-size: 16pt; font-weight:bold; color: white; font-family: Arial, Microsoft JhengHei, serif, sans-serif;
													border-bottom: 1px solid gray; background-image: url(%s);}''' % imgGreenBtn)
		#self.pbet_qlabel2.setScaledContents(True)
		
		self.pbet_qlabel3.setText(self.tr('閒'))
		self.pbet_qlabel3.setAlignment(Qt.AlignCenter)
		self.pbet_qlabel3.setFixedWidth(71)
		self.pbet_qlabel3.setFixedHeight(90)
		self.pbet_qlabel3.setStyleSheet('''.QLabel {font-size: 16pt; font-weight:bold; color: white; font-family: Arial, Microsoft JhengHei, serif, sans-serif;
													border-bottom: 1px solid gray; background-image: url(%s);}''' % imgBlueBtn)
		#self.pbet_qlabel3.setScaledContents(True)
		
		self.pbet_btn.setText(self.tr('返回'))
		self.pbet_btn.setStyleSheet('''.QPushButton {font-size: %dpt; font-family: Arial, Microsoft JhengHei, serif, sans-serif;}''' % self.sizeFontSize_Button)
		self.pbet_btn.setSizePolicy(self.sizePolicy)
		self.pbet_btn.setFixedWidth(90)
		self.pbet_btn.setFixedHeight(30)
		
		self.pbet_btn_allcut.setText(self.tr('全切'))
		self.pbet_btn_allcut.setStyleSheet('''.QPushButton {font-size: %dpt; font-family: Arial, Microsoft JhengHei, serif, sans-serif;}''' % self.sizeFontSize_Button)
		self.pbet_btn_allcut.setSizePolicy(self.sizePolicy)
		self.pbet_btn_allcut.setFixedWidth(90)
		self.pbet_btn_allcut.setFixedHeight(30)
		
		
		# bet record area
		#--------------------------
		self.rbet_qframe.setSizePolicy(self.sizePolicy)
		
		self.rbet_vl.setSpacing(0)
		self.rbet_vl.setMargin(0)
		
		self.rbet_qlabel.setText(self.tr('投注紀錄'))
		self.rbet_qlabel.setStyleSheet('''.QLabel {font-size: %dpt; background-color: white; border-top: 1px solid gray;
											border-left: 1px solid gray; border-right: 1px solid gray;
											font-family: Arial, Microsoft JhengHei, serif, sans-serif;}''' % self.sizeFontSize_Label)
		self.rbet_qlabel.setAlignment(Qt.AlignCenter)
		self.rbet_qlabel.setFixedWidth(self.Width_BetStatus)
		self.rbet_qlabel.setFixedHeight(30)
		
		self.rbet_qscrollarea.setStyleSheet('''.QScrollArea {background-color: white;}''')
		self.rbet_qscrollarea.setFixedWidth(self.Width_BetStatus)
		self.rbet_qscrollarea.setFixedHeight(self.Height_BetStatus_rbet_qscroll)
		self.rbet_qscrollarea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
		self.rbet_qscrollarea_qframe.setStyleSheet('''.QFrame {background-color: white;}''')
		self.rbet_qscrollarea_vl.setAlignment(Qt.AlignTop)
		self.rbet_qscrollarea_vl.setDirection(QBoxLayout.BottomToTop)
		self.rbet_qscrollarea_vl.setSpacing(0)
		self.rbet_qscrollarea_vl.setMargin(0)
		
		self.trbet_qframe.setStyleSheet('''.QFrame {background-color: gray; border-top: 1px solid gray;
											border-left: 1px solid gray; border-right: 1px solid gray;}''')
		self.trbet_qframe.setFixedWidth(self.Width_BetStatus)
		self.trbet_qframe.setFixedHeight(30)
		self.trbet_qlabel1.setText(self.tr('局'))
		self.trbet_qlabel1.setStyleSheet('''.QLabel {font-size: %dpt; color: white; font-family: Arial, Microsoft JhengHei, serif, sans-serif;}''' % self.sizeFontSize_Label)
		self.trbet_qlabel1.setAlignment(Qt.AlignCenter)
		self.trbet_qlabel2.setText(self.tr('注碼'))
		self.trbet_qlabel2.setStyleSheet('''.QLabel {font-size: %dpt; color: white; font-family: Arial, Microsoft JhengHei, serif, sans-serif;}''' % self.sizeFontSize_Label)
		self.trbet_qlabel3.setText(self.tr('莊/閒'))
		self.trbet_qlabel3.setStyleSheet('''.QLabel {font-size: %dpt; color: white; font-family: Arial, Microsoft JhengHei, serif, sans-serif;}''' % self.sizeFontSize_Label)
		self.trbet_qlabel4.setText(self.tr('實得分'))
		self.trbet_qlabel4.setStyleSheet('''.QLabel {font-size: %dpt; color: white; font-family: Arial, Microsoft JhengHei, serif, sans-serif;}''' % self.sizeFontSize_Label)
		self.trbet_qlabel4.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
		self.trbet_qlabelspace.setFixedWidth(self.Width_trbet_space)
		self.trbet_hl.setSpacing(0)
		self.trbet_hl.setMargin(0)
		
		# initail global values of UIcreate_numberInput
		#----------------------------------------------------
		self.binp_qframe[0].setGeometry(QRect(486, 24, 180, 145))
		self.binp_qframe[1].setGeometry(QRect(486, 195, 180, 145))
		self.binp_qframe[2].setGeometry(QRect(486, 366, 180, 145))
		self.binp_qframe[3].setGeometry(QRect(486, 537, 180, 145))
		if printGalgorithm != '':
			self.binp_qframe[4].setGeometry(QRect(486, 708, 180, 145))
		
		for i in range(road_count):
			self.binp_qframe[i].setStyleSheet('''.QFrame {background-color: rgb(230, 230, 230); border: 1px solid gray;}
												.QPushButton {font-size: %dpt; background-color: rgb(250, 250, 250);
												font-family: Arial, Microsoft JhengHei, serif, sans-serif;}''' % self.sizeFontSize_Label)
			self.binp_qframe[i].setFrameShape(QFrame.StyledPanel)
			self.binp_qframe[i].setFrameShadow(QFrame.Raised)
			self.binp_qframe[i].close()
			
			self.binp_gl[i].setSpacing(1)
			self.binp_gl[i].setMargin(0)
			
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
			self.binp_btn12[i].setText(self.tr('清\n除'))
			self.binp_btn13[i].setText(self.tr('確\n認'))
			
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
			self.binp_btn12[i].setFixedWidth(self.binp_btnWidth)
			self.binp_btn12[i].setFixedHeight(self.binp_btnHeight*2)
			self.binp_btn13[i].setFixedWidth(self.binp_btnWidth)
			self.binp_btn13[i].setFixedHeight(self.binp_btnHeight*2)
	
	def initialBtnConnect(self):
		# initail left bar btn in UIcreate_Grid
		#----------------------------------------------------
		for i in range(road_count):
			if printGalgorithm != '':
				if i == 0:
					continue
			self.lbar_btn[i].clicked.connect(functools.partial(self.connect_lbar_btn, i))
		
		# initail right bar btn in UIcreate_Grid
		#----------------------------------------------------
		for i in range(road_count):
			if printGalgorithm != '':
				if i == 0:
					continue
			self.rbar_btn[i].clicked.connect(functools.partial(self.connect_rbar_btn, i))
		
		# initail bet and print area in UIcreate_BetStatus
		#----------------------------------------------------
		self.bbet_btn1.clicked.connect(self.connect_bbet_btn1)
		self.bbet_btn2.clicked.connect(self.connect_bbet_btn2)
		
		# initail bet inning count area in UIcreate_BetStatus
		#----------------------------------------------------
		#clickable(self.libet_qframe).connect(self.connect_libet_qframe)
		if printGalgorithm == '':
			clickable(self.ibet_qlabel_banker1).connect(functools.partial(self.connect_libet_qframe, 0))
			clickable(self.ibet_qlabel_banker2).connect(functools.partial(self.connect_libet_qframe, 0))
			clickable(self.ibet_qlabel_banker3).connect(functools.partial(self.connect_libet_qframe, 0))
			clickable(self.ibet_qlabel_banker4).connect(functools.partial(self.connect_libet_qframe, 0))
			clickable(self.ibet_qlabel_player1).connect(functools.partial(self.connect_libet_qframe, 1))
			clickable(self.ibet_qlabel_player2).connect(functools.partial(self.connect_libet_qframe, 1))
			clickable(self.ibet_qlabel_player3).connect(functools.partial(self.connect_libet_qframe, 1))
			clickable(self.ibet_qlabel_player4).connect(functools.partial(self.connect_libet_qframe, 1))
		
		# initail push button area in UIcreate_BetStatus
		#----------------------------------------------------
		clickable(self.pbet_qlabel1).connect(functools.partial(self.connect_pbet_qlabel, Banker))
		clickable(self.pbet_qlabel2).connect(functools.partial(self.connect_pbet_qlabel, Tie))
		clickable(self.pbet_qlabel3).connect(functools.partial(self.connect_pbet_qlabel, Player))
		self.pbet_btn.clicked.connect(self.connect_pbet_btn)
		if printGalgorithm == '':
			self.pbet_btn_allcut.clicked.connect(self.connect_pbet_btn_allcut)
		
		
		# initail UIcreate_numberInput
		#----------------------------------------------------
		for i in range(road_count):
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
			self.binp_btn12[i].clicked.connect(functools.partial(self.connect_binp_btn, i , 12))
			self.binp_btn13[i].clicked.connect(functools.partial(self.connect_binp_btn, i, 13))
	
	def connect_lbar_btn(self, i):
		betRecord = self.betRecord
		index = i
		if printGalgorithm != '':
			if i != 0:
				index -= 1
				betRecord = self.betRecord_G
		
		if self.lbar_btn[i].text().toUtf8() == '手動':
			LastCutStopStatus = betRecord.getLastCutStopStatus()
			if not LastCutStopStatus[index]:
				self.lbar_btn[i].setText(self.tr(''))
				self.lbar_qlineedit[i].setText('')
				self.binp_qframe[i].show()
		else:
			self.lbar_btn[i].setText(self.tr('手動'))
			if betRecord.gameIsBegin():
				if len(self.lbar_qlineedit[i].text()) > 0:
					img = 0
					bet = int(self.lbar_qlineedit[i].text())
					if self.lbar_qlabel[i].text().toUtf8() == '莊':
						img = 0
					else:
						img = 1
					
					if index != 0:
						ret = betRecord.predictNextStatus()
						if ret.get('status') == 0:
							img = ret['nextStatus'][img][index-1]
					
					if printGalgorithm != '':
						sugList_G = self.betRecord_G.getSugList()
						ret_G = self.betRecord.algorithmG(sugList_G[0][2], True)
						imgG = ret_G.get('imgG')
						if imgG != -1:
							if sugList_G[0][2] != imgG:
								if img == 0:
									img = 1
								elif img == 1:
									img = 0
								else:
									img = -1
					
					self.changeSug(i, img, bet, True)
					self.logGame('手動: (road = %d, img = %d, bet = %d)' % (i, img, bet))
			
			self.binp_qframe[i].close()
	
	# cut stop
	def connect_rbar_btn(self, i):
		betRecord = self.betRecord
		index = i
		if printGalgorithm != '':
			if i != 0:
				index -= 1
				betRecord = self.betRecord_G
		
		ret = betRecord.cutStop(index)
		if ret:
			if self.rbar_btn[i].text().toUtf8() == '停止':
				self.logGame('停止: road = %d' %i)
				self.rbar_btn[i].setText(self.tr('開始'))
				self.rbar_btn[i].setStyleSheet('''.QPushButton {background-color: rgb(255, 255, 127); font-size: %dpt; font-family: Arial, Microsoft JhengHei, serif, sans-serif;}''' % self.sizeFontSize_Button)
				
				# add black border on the grid
				show = betRecord.lastShow(index)
				if show[0] != -1 and show[1] != -1:
					style = str(self.grid_qlabelList[i][show[0]][show[1]].layout().itemAt(0).widget().styleSheet())
					style = style.replace('{', '{ border: 1px solid black;')
					self.grid_qlabelList[i][show[0]][show[1]].layout().itemAt(0).widget().setStyleSheet('''%s'''%style)
				
				# change Sug to 0
				self.changeSug(i, show[2], 0, False)
			else:
				self.logGame('開始: road = %d' %i)
				self.rbar_btn[i].setText(self.tr('停止'))
				self.rbar_btn[i].setStyleSheet('''.QPushButton {font-size: %dpt; font-family: Arial, Microsoft JhengHei, serif, sans-serif;}''' % self.sizeFontSize_Button)
				show = betRecord.lastShow(index)
				# algorithm v1
				if sugAlgorithm == 'A':
					self.changeSug(i, show[2], 1, False)
				# algorithm v2
				elif sugAlgorithm == 'B':
					self.changeSug(i, show[2], 0, False)
				elif sugAlgorithm == 'G':
					self.changeSug(i, show[2], 0, False)
			
			self.update_lbar()
			self.update_rbar()
			self.update_nbet(-1, -1)
	
	def connect_bbet_btn1(self):
		reply = QMessageBox.question(self, self.tr('訊息'),
		self.tr('確定要重開新局嗎?'), QMessageBox.Yes, QMessageBox.No)
		
		if reply == QMessageBox.Yes:
			FILEPATH = 'Baccarat.exe'
			if os.path.exists(FILEPATH):
				log('重開新局')
				try:
					subprocess.Popen([sys.executable, FILEPATH])
				except OSError as exception:
					print('ERROR: could not restart aplication:')
					print('  %s' % str(exception))
				else:
					qApp.quit()
			else:
				log('重開失敗，檔名不對')
	
	def connect_bbet_btn2(self):
		filename_list = ['gridShot_big', 'gridShot_eye', 'gridShot_sma', 'gridShot_pen']
		image_description = ['大路', '眼路', '小路', '筆路']
		nowPath = os.getcwd()
		nowPath = nowPath.replace('\\', '/')
		url = nowPath + '/print/baccarat_print.html'
		fontFamily = 'font-family: Arial, Microsoft JhengHei, serif, sans-serif;'
		
		if not os.path.isdir(os.path.join(os.getcwd(), 'print')):
			os.mkdir(os.path.join(os.getcwd(), 'print'))
		
		# store screenshot_grid image
		for i in range(4):
			screenshot_grid = QPixmap.grabWidget(self.grid_qframe[i])
			screenshot_grid.save('print/' + filename_list[i] + '.png', 'PNG')
		
		# output html file
		file = open('print/baccarat_print.html', 'w')
		file.write('<!DOCTYPE html>\n<html>\n<head>\n<meta charset="UTF-8">\n</head>\n<body>\n<h1><span style="%s">Baccarat</span></h1>\n' % fontFamily)
		
		enum = enumerate(filename_list)
		for index, filename in enum:
			file.write('<p><span style="%s">%s</span></p>\n<img id="%s" src="%s">\n</br>\n' % (fontFamily, image_description[index], filename, filename+'.png'))
		
		if len(self.recordHtml_list) > 0:
			file.write('<p><span style="%s">投注紀錄</span></p>\n' % fontFamily)
			file.write('<table border="1">\n')
			
			enum = enumerate(self.recordHtml_list)
			for index, recordHtml in enum:
				countBet = recordHtml[0]
				sameBet = recordHtml[1]
				colorBet = recordHtml[2]
				pointBet = recordHtml[3]
				
				file.write('<tr>\n')
				file.write('<td><span style="color: gray; %s">%d</span></td>\n' %(fontFamily, index))
				
				if countBet == 0:
					file.write('<td><span style="%s">%d</span></td>\n' % (fontFamily, countBet))
				else:
					if sameBet:
						file.write('<td><span style="color: blue; %s">+%d</span></td>\n' % (fontFamily, countBet))
					else:
						file.write('<td><span style="color: red; %s">-%d</span></td>\n' % (fontFamily, countBet))
				
				if colorBet == 0:
					file.write('<td><span style="color: red; %s">莊</span></td>\n' % fontFamily)
				# colorBet == 1
				else:
					file.write('<td><span style="color: blue; %s">閒</span></td>\n' % fontFamily)
				
				file.write('<td><span style="color: gray; %s">%.2f</span></td>\n' % (fontFamily, pointBet))
				
				file.write('</tr>\n')
			
			file.write('</table>\n')
		
		file.write('</body>\n</html>')
		file.close()
		
		webbrowser.open_new(url)
	
	def connect_libet_qframe(self, img):
		self.controlGridGif()
		nextStatus = self.betRecord.predictNextStatus().get('nextStatus')
		PossibleSugPosition = self.betRecord.getPossibleSugPosition()
		
		self.initialGridGifList()
		
		for i in range(4):
			tmp_img = img
			if i != 0:
				tmp_img = nextStatus[img][i-1]
			
			row = PossibleSugPosition[i][tmp_img][0]
			col = PossibleSugPosition[i][tmp_img][1]
			if row == 0 and col == 0:
				row = -1
				col = -1
			
			pop = self.listForMovie.pop(i)
			self.listForMovie.insert(i, (row, col, tmp_img, 0))
			self.changeGridGif(i, row, col, tmp_img)
		
		self.restartGridGif()
	
	def connect_pbet_qlabel(self, winner):
		if not self.checkAndUpdateLastTime():
			msgBox = QMessageBox(self)
			msgBox.setIcon(QMessageBox.Information)
			msgBox.setText(self.tr('請使用驗證程式'))
			msgBox.exec_()
			sys.exit()
		
		self.controlGridGif()
		self.initialGridGifList()
		
		ret = self.betRecord.bet(winner)
		self.logGame('result:' + str(winner))
		if ret.get('status') == 0:
			lastSugList = [ret.get('lastSugBig'), ret.get('lastSugEye'), ret.get('lastSugSma'), ret.get('lastSugPen')]
			showSugList = [ret.get('SugBig'), ret.get('SugEye'), ret.get('SugSma'), ret.get('SugPen')]
			showList = [ret.get('Big'), ret.get('Eye'), ret.get('Sma'), ret.get('Pen')]
			isBet = ret.get('isBet')
			sameBet = ret.get('sameBet')
			countBet = ret.get('countBet')
			
			# new insert code for new algorithm DEF
			if printDEFalgorithm != '' and winner != Tie:
				ret_DEF = self.betRecord.algorithmDEF()
				lastSugList = ret_DEF.get('lastSugList')
				showSugList = ret_DEF.get('showSugList')
				showList = [ret.get('Big'), ret.get('Big'), ret.get('Big'), ret.get('Big')]
				isBet = ret_DEF.get('isBet')
				sameBet = ret_DEF.get('sameBet')
				countBet = ret_DEF.get('countBet')
				#ret['SugBig_sum'] = ret_DEF.get('SugDEF_sum')
				#ret['lastSugBig_sum'] = ret_DEF.get('lastSugDEF_sum')
			
			if printGalgorithm != '' and winner != Tie:
				lastSugList_G = [(-1, -1, -1, -1), (-1, -1, -1, -1), (-1, -1, -1, -1), (-1, -1, -1, -1)]
				showSugList_G = [(-1, -1, -1, -1), (-1, -1, -1, -1), (-1, -1, -1, -1), (-1, -1, -1, -1)]
				showList_G = [(-1, -1, -1), (-1, -1, -1), (-1, -1, -1), (-1, -1, -1)]
				isBet_G = [False, False, False, False]
				sameBet_G = [False, False, False, False]
				countBet_G = [0, 0, 0, 0]
				
				for i in range(4):
					if i != 3:
						lastSugList[i+1] = lastSugList_G[i]
						showSugList[i+1] = showSugList_G[i]
						showList[i+1] = showList_G[i]
						isBet[i+1] = isBet_G[i]
						sameBet[i+1] = sameBet_G[i]
						countBet[i+1] = countBet_G[i]
					else:
						lastSugList.append(lastSugList_G[i])
						showSugList.append(showSugList_G[i])
						showList.append(showList_G[i])
						isBet.append(isBet_G[i])
						sameBet.append(sameBet_G[i])
						countBet.append(countBet_G[i])
				
				ret_G = self.betRecord.algorithmG(winner)
				imgG = ret_G.get('imgG')
				all_the_same = ret_G.get('all_the_same')
				if imgG != -1:
					ret_G = self.betRecord_G.bet(imgG)
				
				if imgG != -1:
					lastSugList_G = [ret_G.get('lastSugBig'), ret_G.get('lastSugEye'), ret_G.get('lastSugSma'), ret_G.get('lastSugPen')]
					showSugList_G = [ret_G.get('SugBig'), ret_G.get('SugEye'), ret_G.get('SugSma'), ret_G.get('SugPen')]
					showList_G = [ret_G.get('Big'), ret_G.get('Eye'), ret_G.get('Sma'), ret_G.get('Pen')]
					isBet_G = ret_G.get('isBet')
					sameBet_G = ret_G.get('sameBet')
					countBet_G = ret_G.get('countBet')
					
					for i in range(4):
						lastSugList[i+1] = lastSugList_G[i]
						showSugList[i+1] = showSugList_G[i]
						showList[i+1] = showList_G[i]
						isBet[i+1] = isBet_G[i]
						sameBet[i+1] = sameBet_G[i]
						countBet[i+1] = countBet_G[i]
				
				# get next imgG to check if add sug_sum to road 1
				tmp = self.betRecord.algorithmG(winner)
				tmp_img = tmp.get('imgG')
				self.betRecord.algorithmGbackOneStep()
				
				if tmp_img != -1:
					SugBig_sum = self.betRecord_G.getSugList()[4]
					if SugBig_sum[2] != -1 and SugBig_sum[3] != -1:
						if tmp_img != winner:
							if SugBig_sum[2] == 0:
								SugBig_sum = (SugBig_sum[0], SugBig_sum[1], 1, SugBig_sum[3])
							else:
								SugBig_sum = (SugBig_sum[0], SugBig_sum[1], 0, SugBig_sum[3])
						
						retSug, eraseSug, SugBig_sum, SugBig_sum_otherimg = self.betRecord.manualChangeSug(0, SugBig_sum[2], SugBig_sum[3], False)
						showSugList[0] = SugBig_sum
						ret['SugBig_sum'] = SugBig_sum
			elif printGalgorithm != '' and winner == Tie:
				lastSugList.append((-1, -1, -1, -1))
				showSugList.append((-1, -1, -1, -1))
				showList.append((-1, -1, -1))
			
			for i in range(road_count):
				row = lastSugList[i][0]
				col = lastSugList[i][1]
				img = lastSugList[i][2]
				bet = lastSugList[i][3]
				if row >= 0 and col >= 0:
					if winner != Tie:
						self.grid_qlabelList[i][row][col].layout().itemAt(0).widget().setText('')
						self.grid_qlabelList[i][row][col].movie().setFileName(imgCell)
						self.grid_qlabelList[i][row][col].movie().start()
						self.grid_qlabelList[i][row][col].movie().stop()
			
			for i in range(road_count):
				row = showSugList[i][0]
				col = showSugList[i][1]
				img = showSugList[i][2]
				bet = showSugList[i][3]
				if row >= 0 and col >= 0:
					if bet == 0:
						self.grid_qlabelList[i][row][col].layout().itemAt(0).widget().setText('')
						self.grid_qlabelList[i][row][col].movie().setFileName(imgCell)
					else:
						self.grid_qlabelList[i][row][col].layout().itemAt(0).widget().setText(str(bet))
						self.grid_qlabelList[i][row][col].layout().itemAt(0).widget().setStyleSheet('''.QLabel { font-family: Arial, Microsoft JhengHei, serif, sans-serif;
																														color: black; font-weight: bold; font-size: %dpt;}''' % self.sizeFontSize_Grid)
						self.grid_qlabelList[i][row][col].movie().setFileName(self.betRecord.imgSugPath[i][img])
					
					self.grid_qlabelList[i][row][col].movie().start()
					self.grid_qlabelList[i][row][col].movie().stop()
			
			for i in range(road_count):
				row = showList[i][0]
				col = showList[i][1]
				img = showList[i][2]
				if row >= 0 and col >= 0:
					if winner != Tie:
						if isBet[i]:
							if countBet[i] == 0:
								self.grid_qlabelList[i][row][col].layout().itemAt(0).widget().setText('')
							else:
								self.grid_qlabelList[i][row][col].layout().itemAt(0).widget().setText(str(countBet[i]))
							
							if sameBet[i]:
								self.grid_qlabelList[i][row][col].layout().itemAt(0).widget().setStyleSheet('''.QLabel { font-family: Arial, Microsoft JhengHei, serif, sans-serif;
																														color: black; font-weight: bold; font-size: %dpt;}''' % self.sizeFontSize_Grid)
							else:
								self.grid_qlabelList[i][row][col].layout().itemAt(0).widget().setStyleSheet('''.QLabel { font-family: Arial, Microsoft JhengHei, serif, sans-serif;
																														color: red; font-weight: bold; font-size: %dpt;}''' % self.sizeFontSize_Grid)
						
						self.grid_qlabelList[i][row][col].movie().setFileName(self.betRecord.imgPath[i][img])
						if i == 1 and printGalgorithm != '' and all_the_same:
							self.grid_qlabelList[i][row][col].movie().setFileName(self.betRecord.imgPath[4][img+2])
					else:
						self.grid_qlabelList[i][row][col].movie().setFileName(self.betRecord.imgPath[i][Tie][img])
					
					self.grid_qlabelList[i][row][col].movie().start()
					self.grid_qlabelList[i][row][col].movie().stop()
			
			if winner != Tie:
				# update next bet area (sum of 4 road)
				Sugsum = ret.get('SugBig_sum')
				self.update_nbet(Sugsum[2], Sugsum[3])
				
				# add a record in record area
				recordEntry = ret.get('lastSugBig_sum')
				if recordEntry == (-1, -1, -1, -1):
					recordEntry = (0, 0, winner, 0)
				self.update_rbet(recordEntry[3], (recordEntry[2] == winner), recordEntry[2])
			
		elif ret.get('status') == Still_Tie:
			pass
		elif ret.get('status') == Need_Enter_First:
			pass
		elif ret.get('status') == First_Tie:
			self.grid_qlabelList[0][0][0].layout().itemAt(0).widget().setStyleSheet('''.QLabel { font-family: Arial, Microsoft JhengHei, serif, sans-serif;
																								border: 1px solid green;}''')
		elif ret.get('status') == Still_First_Tie:
			pass
		elif ret.get('status') == Game_End:
			self.gameEndMessage()
		
		self.update_lbar()
		self.update_rbar()
		self.update_bbet()
		self.update_ibet()
	
	def connect_pbet_btn(self):
		self.controlGridGif()
		self.initialGridGifList()
		
		ret = self.betRecord.backOneStep()
		self.logGame('back')
		self.betRecord.changeEndGameToFalse()
		if ret.get('status') == 0:
			removeList = [ret.get('Big'), ret.get('Eye'), ret.get('Sma'), ret.get('Pen')]
			removeSugList = [ret.get('SugBig'), ret.get('SugEye'), ret.get('SugSma'), ret.get('SugPen')]
			ShowLastSugList = [ret.get('lastSugBig'), ret.get('lastSugEye'), ret.get('lastSugSma'), ret.get('lastSugPen')]
			
			# new insert code for new algorithm DEF
			if printDEFalgorithm != '':
				ret_DEF = self.betRecord.algorithmDEFbackOneStep()
				removeList = [ret.get('Big'), ret.get('Big'), ret.get('Big'), ret.get('Big')]
				removeSugList = ret_DEF.get('removeSugList')
				ShowLastSugList = ret_DEF.get('ShowLastSugList')
			
			if printGalgorithm != '':
				removeList_G = [(-1, -1, -1), (-1, -1, -1), (-1, -1, -1), (-1, -1, -1)]
				removeSugList_G = [(-1, -1, -1, -1), (-1, -1, -1, -1), (-1, -1, -1, -1), (-1, -1, -1, -1)]
				ShowLastSugList_G = [(-1, -1, -1, -1), (-1, -1, -1, -1), (-1, -1, -1, -1), (-1, -1, -1, -1)]
				
				ret_G = self.betRecord.algorithmGbackOneStep()
				imgG = ret_G.get('imgG')
				if imgG != -1:
					ret_G = self.betRecord_G.backOneStep()
					removeList_G = [ret_G.get('Big'), ret_G.get('Eye'), ret_G.get('Sma'), ret_G.get('Pen')]
					removeSugList_G = [ret_G.get('SugBig'), ret_G.get('SugEye'), ret_G.get('SugSma'), ret_G.get('SugPen')]
					ShowLastSugList_G = [ret_G.get('lastSugBig'), ret_G.get('lastSugEye'), ret_G.get('lastSugSma'), ret_G.get('lastSugPen')]
				
				for i in range(4):
					if i != 3:
						removeList[i+1] = removeList_G[i]
						removeSugList[i+1] = removeSugList_G[i]
						ShowLastSugList[i+1] = ShowLastSugList_G[i]
					else:
						removeList.append(removeList_G[i])
						removeSugList.append(removeSugList_G[i])
						ShowLastSugList.append(ShowLastSugList_G[i])
			
			for i in range(road_count):
				row = removeList[i][0]
				col = removeList[i][1]
				if row >= 0 and col >= 0:
					self.grid_qlabelList[i][row][col].layout().itemAt(0).widget().setText('')
					self.grid_qlabelList[i][row][col].movie().setFileName(imgCell)
					self.grid_qlabelList[i][row][col].movie().start()
					self.grid_qlabelList[i][row][col].movie().stop()
			
			for i in range(road_count):
				row = removeSugList[i][0]
				col = removeSugList[i][1]
				img = removeSugList[i][2]
				bet = removeSugList[i][3]
				if row >= 0 and col >= 0:
					self.grid_qlabelList[i][row][col].layout().itemAt(0).widget().setText('')
					self.grid_qlabelList[i][row][col].movie().setFileName(imgCell)
					self.grid_qlabelList[i][row][col].movie().start()
					self.grid_qlabelList[i][row][col].movie().stop()
			
			for i in range(road_count):
				row = ShowLastSugList[i][0]
				col = ShowLastSugList[i][1]
				img = ShowLastSugList[i][2]
				bet = ShowLastSugList[i][3]
				if row >= 0 and col >= 0:
					self.grid_qlabelList[i][row][col].layout().itemAt(0).widget().setStyleSheet('''.QLabel { font-family: Arial, Microsoft JhengHei, serif, sans-serif;
																									color: black; font-weight: bold; font-size: %dpt;}''' % self.sizeFontSize_Grid)
					if bet == 0:
						self.grid_qlabelList[i][row][col].layout().itemAt(0).widget().setText('')
						self.grid_qlabelList[i][row][col].movie().setFileName(imgCell)
					else:
						self.grid_qlabelList[i][row][col].layout().itemAt(0).widget().setText(str(bet))
						self.grid_qlabelList[i][row][col].movie().setFileName(self.betRecord.imgSugPath[i][img])
					
					self.grid_qlabelList[i][row][col].movie().start()
					self.grid_qlabelList[i][row][col].movie().stop()
			
			self.betRecord.principalPopEntry()
			self.popRecordForHtml()
			removeQframe = self.rbet_qscrollarea_vl.itemAt(self.rbet_qscrollarea_vl.count()-1).widget()
			removeQframe.close()
			self.rbet_qscrollarea_vl.removeWidget(removeQframe)
			
			lastSugBig_sum = ret.get('lastSugBig_sum')
			if removeList[0][0] == 0 and removeList[0][1] == 0:
				self.update_nbet(-2, -2)
			else:
				self.update_nbet(lastSugBig_sum[2], lastSugBig_sum[3])
			
			# handle cut stop
			self.backFromCutStop(removeList)
			
		elif ret.get('status') == No_Back:
			pass
		elif ret.get('status') == Still_Tie:
			pass
		elif ret.get('status') == Back_From_Tie:
			BackBig = ret.get('Big')
			self.grid_qlabelList[0][BackBig[0]][BackBig[1]].movie().setFileName(self.betRecord.imgPath[0][BackBig[2]])
			self.grid_qlabelList[0][BackBig[0]][BackBig[1]].movie().start()
			self.grid_qlabelList[0][BackBig[0]][BackBig[1]].movie().stop()
		elif ret.get('status') == Back_Still_First_Tie:
			pass
		elif ret.get('status') == Back_From_First_Tie:
			self.grid_qlabelList[0][0][0].layout().itemAt(0).widget().setStyleSheet('''.QLabel { font-family: Arial, Microsoft JhengHei, serif, sans-serif;}''')
		
		self.update_lbar()
		self.update_rbar()
		self.update_bbet()
		self.update_ibet()
	
	# cut stop all
	def connect_pbet_btn_allcut(self):
		log('全切')
		LastCutStopStatus = self.betRecord.getLastCutStopStatus()
		for i in range(road_count):
			if not LastCutStopStatus[i]:
				self.connect_rbar_btn(i)
	
	def connect_binp_btn(self, i, number):
		ret = self.betRecord.predictNextStatus()
		nextStatus = ret['nextStatus']
		
		if printGalgorithm != '':
			ret = self.betRecord_G.predictNextStatus()
			nextStatus_G = ret['nextStatus']
			
			ret_G = self.betRecord.algorithmG(0, True)
			imgG = ret_G.get('imgG')
			if imgG == 0:
				nextStatus = [[0, nextStatus_G[0][0], nextStatus_G[0][1], nextStatus_G[0][2]], [1, nextStatus_G[1][0], nextStatus_G[1][1], nextStatus_G[1][2]]]
			elif imgG == 1:
				nextStatus = [[1, nextStatus_G[1][0], nextStatus_G[1][1], nextStatus_G[1][2]], [0, nextStatus_G[0][0], nextStatus_G[0][1], nextStatus_G[0][2]]]
			else:
				nextStatus = [[0, nextStatus_G[0][0], nextStatus_G[0][1], nextStatus_G[0][2]], [1, nextStatus_G[1][0], nextStatus_G[1][1], nextStatus_G[1][2]]]
		
		if number in range(10):
			tmp = self.lbar_qlineedit[i].text() + str(number)
			self.lbar_qlineedit[i].setText(tmp)
		elif number == 10:
			self.lbar_qlabel[i].setText(self.tr('莊'))
			
			if i == 0:
				self.lbar_qframe[i].setStyleSheet('''.QFrame {background-color: red; border: 1px solid gray;}''')
			else:
				if nextStatus[0][i-1] == 0:
					self.lbar_qframe[i].setStyleSheet('''.QFrame {background-color: red; border: 1px solid gray;}''')
				elif nextStatus[0][i-1] == 1:
					self.lbar_qframe[i].setStyleSheet('''.QFrame {background-color: blue; border: 1px solid gray;}''')
				else:
					self.lbar_qframe[i].setStyleSheet('''.QFrame {background-color: red; border: 1px solid gray;}''')
		elif number == 11:
			self.lbar_qlabel[i].setText(self.tr('閒'))
			
			if i == 0:
				self.lbar_qframe[i].setStyleSheet('''.QFrame {background-color: blue; border: 1px solid gray;}''')
			else:
				if nextStatus[1][i-1] == 0:
					self.lbar_qframe[i].setStyleSheet('''.QFrame {background-color: red; border: 1px solid gray;}''')
				elif nextStatus[1][i-1] == 1:
					self.lbar_qframe[i].setStyleSheet('''.QFrame {background-color: blue; border: 1px solid gray;}''')
				else:
					self.lbar_qframe[i].setStyleSheet('''.QFrame {background-color: blue; border: 1px solid gray;}''')
		elif number == 12:
			self.lbar_qlineedit[i].setText('')
		elif number == 13:
			self.connect_lbar_btn(i)
	
	def update_lbar(self):
		check_color = []
		sugList = self.betRecord.getSugList()
		sugList_img = [sugList[0][2], sugList[1][2], sugList[2][2], sugList[3][2]]
		if sugList_img[0] != -1:
			# predict next status
			ret = self.betRecord.predictNextStatus()
			
			check_color.append(sugList_img[0])
			check_color.append(ret['nextStatus'][sugList_img[0]][0])
			check_color.append(ret['nextStatus'][sugList_img[0]][1])
			check_color.append(ret['nextStatus'][sugList_img[0]][2])
		else:
			check_color = [-1, -1, -1, -1]
		
		if printGalgorithm != '':
			sugList_G = self.betRecord_G.getSugList()
			sugList_img_G = [sugList_G[0][2], sugList_G[1][2], sugList_G[2][2], sugList_G[3][2]]
			if sugList_img_G[0] != -1:
				ret_G = self.betRecord.algorithmG(sugList_img[0], True)
				imgG = ret_G.get('imgG')
				if imgG != -1:
					# predict next status
					ret = self.betRecord_G.predictNextStatus()
					
					for i in range(3):
						del check_color[-1]
						del sugList_img[-1]
					
					check_color.append(imgG)
					check_color.append(ret['nextStatus'][imgG][0])
					check_color.append(ret['nextStatus'][imgG][1])
					check_color.append(ret['nextStatus'][imgG][2])
					
					sugList_img.append(sugList_G[0][2])
					sugList_img.append(sugList_G[1][2])
					sugList_img.append(sugList_G[2][2])
					sugList_img.append(sugList_G[3][2])
				else:
					check_color = [sugList_img[0], -1, -1, -1, -1]
					sugList_img = [sugList_img[0], -1, -1, -1, -1]
			else:
				check_color = [sugList_img[0], -1, -1, -1, -1]
				sugList_img = [sugList_img[0], -1, -1, -1, -1]
		
		for i in range(road_count):
			# reset lbar
			self.lbar_btn[i].setText(self.tr('手動'))
			self.lbar_qlineedit[i].setText('')
			self.binp_qframe[i].close()
			
			# change lbar color and text
			# change number input color
			if sugList_img[0] == 0:
				if sugList_img[i] == check_color[i]:
					self.lbar_qlabel[i].setText(self.tr('莊'))
					if sugList_img[i] == 0:
						self.binp_btn10[i].setStyleSheet('''.QPushButton {font-size: %dpt; background-color: rgb(255, 47, 61); color: white;}''' % self.sizeFontSize_Label)
						self.binp_btn11[i].setStyleSheet('''.QPushButton {font-size: %dpt; background-color: rgb(116, 106, 255); color: white;}''' % self.sizeFontSize_Label)
					else:
						self.binp_btn10[i].setStyleSheet('''.QPushButton {font-size: %dpt; background-color: rgb(116, 106, 255); color: white;}''' % self.sizeFontSize_Label)
						self.binp_btn11[i].setStyleSheet('''.QPushButton {font-size: %dpt; background-color: rgb(255, 47, 61); color: white;}''' % self.sizeFontSize_Label)
				else:
					self.lbar_qlabel[i].setText(self.tr('閒'))
					if sugList_img[i] == 1:
						self.binp_btn10[i].setStyleSheet('''.QPushButton {font-size: %dpt; background-color: rgb(255, 47, 61); color: white;}''' % self.sizeFontSize_Label)
						self.binp_btn11[i].setStyleSheet('''.QPushButton {font-size: %dpt; background-color: rgb(116, 106, 255); color: white;}''' % self.sizeFontSize_Label)
					else:
						self.binp_btn10[i].setStyleSheet('''.QPushButton {font-size: %dpt; background-color: rgb(116, 106, 255); color: white;}''' % self.sizeFontSize_Label)
						self.binp_btn11[i].setStyleSheet('''.QPushButton {font-size: %dpt; background-color: rgb(255, 47, 61); color: white;}''' % self.sizeFontSize_Label)
			else:
				if sugList_img[i] == check_color[i]:
					self.lbar_qlabel[i].setText(self.tr('閒'))
					if sugList_img[i] == 1:
						self.binp_btn10[i].setStyleSheet('''.QPushButton {font-size: %dpt; background-color: rgb(255, 47, 61); color: white;}''' % self.sizeFontSize_Label)
						self.binp_btn11[i].setStyleSheet('''.QPushButton {font-size: %dpt; background-color: rgb(116, 106, 255); color: white;}''' % self.sizeFontSize_Label)
					else:
						self.binp_btn10[i].setStyleSheet('''.QPushButton {font-size: %dpt; background-color: rgb(116, 106, 255); color: white;}''' % self.sizeFontSize_Label)
						self.binp_btn11[i].setStyleSheet('''.QPushButton {font-size: %dpt; background-color: rgb(255, 47, 61); color: white;}''' % self.sizeFontSize_Label)
				else:
					self.lbar_qlabel[i].setText(self.tr('莊'))
					if sugList_img[i] == 0:
						self.binp_btn10[i].setStyleSheet('''.QPushButton {font-size: %dpt; background-color: rgb(255, 47, 61); color: white;}''' % self.sizeFontSize_Label)
						self.binp_btn11[i].setStyleSheet('''.QPushButton {font-size: %dpt; background-color: rgb(116, 106, 255); color: white;}''' % self.sizeFontSize_Label)
					else:
						self.binp_btn10[i].setStyleSheet('''.QPushButton {font-size: %dpt; background-color: rgb(116, 106, 255); color: white;}''' % self.sizeFontSize_Label)
						self.binp_btn11[i].setStyleSheet('''.QPushButton {font-size: %dpt; background-color: rgb(255, 47, 61); color: white;}''' % self.sizeFontSize_Label)
			
			if sugList_img[i] == 0:
				self.lbar_qframe[i].setStyleSheet('''.QFrame {background-color: red; border: 1px solid gray;}''')
			elif sugList_img[i] == 1:
				self.lbar_qframe[i].setStyleSheet('''.QFrame {background-color: blue; border: 1px solid gray;}''')
			else:
				self.lbar_qlabel[i].setText('')
				self.lbar_qframe[i].setStyleSheet('''.QFrame {background-color: gray; border: 1px solid gray;}''')
	
	def update_rbar(self):
		if len(self.betRecord.betCountBig) > 0:
			smallCount = [self.betRecord.betCountBig[-1], self.betRecord.betCountEye[-1], self.betRecord.betCountSma[-1], self.betRecord.betCountPen[-1]]
		else:
			smallCount = [0, 0, 0, 0]
		
		if printGalgorithm != '':
			if len(self.betRecord.betCountBig) > 0:
				if len(self.betRecord_G.betCountBig) > 0:
					smallCount = [self.betRecord.betCountBig[-1], self.betRecord_G.betCountBig[-1], self.betRecord_G.betCountEye[-1], self.betRecord_G.betCountSma[-1], self.betRecord_G.betCountPen[-1]]
				else:
					smallCount = [self.betRecord.betCountBig[-1], 0, 0, 0, 0]
			else:
				smallCount = [0, 0, 0, 0, 0]
		
		for i in range(road_count):
			self.rbar_qlabel1[i].setText(self.tr(' 小計 : %s' % str(smallCount[i])))
		
		if len(self.betRecord.betSumCountBig) > 0:
			sumCount = [self.betRecord.betSumCountBig[-1], self.betRecord.betSumCountEye[-1], self.betRecord.betSumCountSma[-1], self.betRecord.betSumCountPen[-1]]
		else:
			sumCount = [0, 0, 0, 0]
		
		if printGalgorithm != '':
			if len(self.betRecord.betSumCountBig) > 0:
				if len(self.betRecord_G.betSumCountBig) > 0:
					sumCount = [self.betRecord.betSumCountBig[-1], self.betRecord_G.betSumCountBig[-1], self.betRecord_G.betSumCountEye[-1], self.betRecord_G.betSumCountSma[-1], self.betRecord_G.betSumCountPen[-1]]
				else:
					sumCount = [self.betRecord.betSumCountBig[-1], 0, 0, 0, 0]
			else:
				sumCount = [0, 0, 0, 0, 0]
		
		for i in range(road_count):
			self.rbar_qlabel2[i].setText(self.tr(' 合計 : %s' % str(sumCount[i])))
	
	def update_bbet(self):
		tmp = self.betRecord.getPrincipal() + self.betRecord.principalSum()
		self.bbet_qlabel1.setText(self.tr('檯面數 : %.2f' %tmp))
		tmp = self.betRecord.principalSumNegative() * -1
		self.bbet_qlabel2.setText(self.tr('轉碼 : %d' %tmp))
	
	def update_nbet(self, img, bet):
		if img == 0:
			self.nbet_qlabel3.setText(self.tr('莊'))
			self.nbet_qlabel3.setStyleSheet('''.QLabel {font-size: %dpt; color: red; font-family: Arial, Microsoft JhengHei, serif, sans-serif;}'''  % self.sizeFontSize_Label)
			self.nbet_qlabel4.setText(str(bet))
		elif img == 1:
			self.nbet_qlabel3.setText(self.tr('閒'))
			self.nbet_qlabel3.setStyleSheet('''.QLabel {font-size: %dpt; color: blue; font-family: Arial, Microsoft JhengHei, serif, sans-serif;}'''  % self.sizeFontSize_Label)
			self.nbet_qlabel4.setText(str(bet))
		elif img == -1:
			pass
		elif img == -2:
			self.nbet_qlabel3.setText('')
			self.nbet_qlabel4.setText('')
		
		if len(self.betRecord.betSumCountBig) > 0:
			sumCount = self.betRecord.betSumCountBig[-1] + self.betRecord.betSumCountEye[-1] + self.betRecord.betSumCountSma[-1] + self.betRecord.betSumCountPen[-1]
		else:
			sumCount = 0
		self.nbet_qlabel5.setText(str(sumCount))
	
	def update_ibet(self):
		# predict next status
		ret = self.betRecord.predictNextStatus()
		if ret.get('status') == 0:
			if ret['nextStatus'][0][0] != -1:
				self.ibet_qlabel_banker2.setStyleSheet('''.QLabel {background-image: url(%s)}'''%self.betRecord.imgNextStatusPath[1][ret['nextStatus'][0][0]])
			else:
				self.ibet_qlabel_banker2.setStyleSheet('''.QLabel {}''')
			if ret['nextStatus'][0][1] != -1:
				self.ibet_qlabel_banker3.setStyleSheet('''.QLabel {background-image: url(%s)}'''%self.betRecord.imgNextStatusPath[2][ret['nextStatus'][0][1]])
			else:
				self.ibet_qlabel_banker3.setStyleSheet('''.QLabel {}''')
			if ret['nextStatus'][0][2] != -1:
				self.ibet_qlabel_banker4.setStyleSheet('''.QLabel {background-image: url(%s)}'''%self.betRecord.imgNextStatusPath[3][ret['nextStatus'][0][2]])
			else:
				self.ibet_qlabel_banker4.setStyleSheet('''.QLabel {}''')
			if ret['nextStatus'][1][0] != -1:
				self.ibet_qlabel_player2.setStyleSheet('''.QLabel {background-image: url(%s)}'''%self.betRecord.imgNextStatusPath[1][ret['nextStatus'][1][0]])
			else:
				self.ibet_qlabel_player2.setStyleSheet('''.QLabel {}''')
			if ret['nextStatus'][1][1] != -1:
				self.ibet_qlabel_player3.setStyleSheet('''.QLabel {background-image: url(%s)}'''%self.betRecord.imgNextStatusPath[2][ret['nextStatus'][1][1]])
			else:
				self.ibet_qlabel_player3.setStyleSheet('''.QLabel {}''')
			if ret['nextStatus'][1][2] != -1:
				self.ibet_qlabel_player4.setStyleSheet('''.QLabel {background-image: url(%s)}'''%self.betRecord.imgNextStatusPath[3][ret['nextStatus'][1][2]])
			else:
				self.ibet_qlabel_player4.setStyleSheet('''.QLabel {}''')
		
		self.ibet_qlabel1.setText(str(self.betRecord.countResult[0]))
		self.ibet_qlabel3.setText(str(self.betRecord.countResult[1]))
		self.ibet_qlabel4.setText(str(self.betRecord.countResult[2]))
		sumRecord = self.betRecord.countResult[0] + self.betRecord.countResult[1] + self.betRecord.countResult[2]
		self.ibet_qlabel2.setText(self.tr(str(sumRecord) + '\n局'))
	
	def update_rbet(self, countBet, sameBet, colorBet):
		if colorBet != 2:
			pointBet = countBet
			if colorBet == 0 and sameBet and countBet != 0:
				pointBet = pointBet * 0.95
			
			if sameBet:
				self.betRecord.principalAddEntry(pointBet)
			else:
				self.betRecord.principalAddEntry(-1 * pointBet)
			self.addOneRecord(countBet, sameBet, colorBet, pointBet)
	
	def addOneRecord(self, countBet, sameBet, colorBet, pointBet):
		if colorBet != 2:
			tmp_qframe = QFrame()
			tmp_hl = QHBoxLayout()
			tmp_hl.setSpacing(0)
			#tmp_hl.setMargin(0)
			tmp_hl.setContentsMargins(0, 0, 0, 1)
			tmp_qframe.setLayout(tmp_hl)
			tmp_qframe.setStyleSheet('''.QFrame {background-color: white; border-bottom: 2px solid gray;}''')
			
			qlabel_no = QLabel()
			qlabel_no.setAlignment(Qt.AlignCenter)
			qlabel_no.setText(str(self.rbet_qscrollarea_vl.count()+1))
			qlabel_no.setStyleSheet('''.QLabel {font-size: %dpt; background-color: white; color: gray;
										font-family: Arial, Microsoft JhengHei, serif, sans-serif;}''' % self.sizeFontSize_Label)
			
			qlabel_countBet = QLabel()
			qlabel_countBet.setText(str(countBet))
			if countBet == 0:
				qlabel_countBet.setStyleSheet('''.QLabel {font-size: %dpt; background-color: white; color: gray;
													font-family: Arial, Microsoft JhengHei, serif, sans-serif;}''' % self.sizeFontSize_Label)
			elif sameBet:
				qlabel_countBet.setStyleSheet('''.QLabel {font-size: %dpt; background-color: white; color: black;
													font-family: Arial, Microsoft JhengHei, serif, sans-serif;}''' % self.sizeFontSize_Label)
			else:
				qlabel_countBet.setStyleSheet('''.QLabel {font-size: %dpt; background-color: white; color: red;
													font-family: Arial, Microsoft JhengHei, serif, sans-serif;}''' % self.sizeFontSize_Label)
			
			qlabel_colorBet = QLabel()
			if colorBet == 0:
				qlabel_colorBet.setText(self.tr('莊'))
				qlabel_colorBet.setStyleSheet('''.QLabel {font-size: %dpt; background-color: white; color: red;
													font-family: Arial, Microsoft JhengHei, serif, sans-serif;}''' % self.sizeFontSize_Label)
			elif colorBet == 1:
				qlabel_colorBet.setText(self.tr('閒'))
				qlabel_colorBet.setStyleSheet('''.QLabel {font-size: %dpt; background-color: white; color: blue;
													font-family: Arial, Microsoft JhengHei, serif, sans-serif;}''' % self.sizeFontSize_Label)
			
			qlabel_pointBet = QLabel()
			if pointBet == 0:
				qlabel_pointBet.setText('%.2f' % pointBet)
				qlabel_pointBet.setStyleSheet('''.QLabel {font-size: %dpt; background-color: white; color: gray;
													font-family: Arial, Microsoft JhengHei, serif, sans-serif;}''' % self.sizeFontSize_Label)
			else:
				if sameBet:
					qlabel_pointBet.setText('%.2f' % pointBet)
					qlabel_pointBet.setStyleSheet('''.QLabel {font-size: %dpt; background-color: white; color: blue;
														font-family: Arial, Microsoft JhengHei, serif, sans-serif;}''' % self.sizeFontSize_Label)
				else:
					qlabel_pointBet.setText('%.2f' % pointBet)
					qlabel_pointBet.setStyleSheet('''.QLabel {font-size: %dpt; background-color: white; color: red;
														font-family: Arial, Microsoft JhengHei, serif, sans-serif;}''' % self.sizeFontSize_Label)
			
			qlabel_space = QLabel()
			qlabel_space.setStyleSheet('''.QLabel {background-color: white; color: gray; font-family: Arial, Microsoft JhengHei, serif, sans-serif;}''')
			qlabel_space.setFixedWidth(self.Width_trbet_space)
			
			tmp_hl.addWidget(qlabel_no)
			tmp_hl.addWidget(qlabel_countBet)
			tmp_hl.addWidget(qlabel_colorBet)
			tmp_hl.addWidget(qlabel_pointBet)
			tmp_hl.addWidget(qlabel_space)
			tmp_qframe.setFixedWidth(215)
			tmp_qframe.setFixedHeight(30)
			
			self.rbet_qscrollarea_vl.addWidget(tmp_qframe)
			
			self.storeRecordForHtml(countBet, sameBet, colorBet, pointBet)
	
	def changeSug(self, i, img, bet, isManual):
		self.controlGridGif()
		self.initialGridGifList()
		
		betRecord = self.betRecord
		index = i
		if printGalgorithm != '':
			if i != 0:
				index -= 1
				betRecord = self.betRecord_G
		
		retSug, eraseSug, SugBig_sum, SugBig_sum_otherimg = betRecord.manualChangeSug(index, img, bet, isManual)
		
		row = eraseSug[0]
		col = eraseSug[1]
		if row >= 0 and col >= 0:
			self.grid_qlabelList[i][row][col].layout().itemAt(0).widget().setText('')
			self.grid_qlabelList[i][row][col].movie().setFileName(imgCell)
			self.grid_qlabelList[i][row][col].movie().start()
			self.grid_qlabelList[i][row][col].movie().stop()
		
		row = retSug[0]
		col = retSug[1]
		img = retSug[2]
		bet = retSug[3]
		if row >= 0 and col >= 0:
			if bet == 0:
				self.grid_qlabelList[i][row][col].layout().itemAt(0).widget().setText('')
				self.grid_qlabelList[i][row][col].movie().setFileName(imgCell)
			else:
				self.grid_qlabelList[i][row][col].layout().itemAt(0).widget().setText(str(bet))
				self.grid_qlabelList[i][row][col].layout().itemAt(0).widget().setStyleSheet('''.QLabel { font-family: Arial, Microsoft JhengHei, serif, sans-serif;
																								color: black; font-weight: bold; font-size: %dpt;}''' % self.sizeFontSize_Grid)
				self.grid_qlabelList[i][row][col].movie().setFileName(betRecord.imgSugPath[i][img])
			
			self.grid_qlabelList[i][row][col].movie().start()
			self.grid_qlabelList[i][row][col].movie().stop()
		
		img = SugBig_sum[2]
		bet = SugBig_sum[3]
		
		if printGalgorithm != '':
			ret_G = self.betRecord.algorithmG(img, True)
			imgG = ret_G.get('imgG')
			if imgG != -1:
				if img != imgG:
					img = imgG
			else:
				img = imgG
		
		self.update_nbet(img, bet)
		
		if printGalgorithm != '' and imgG != -1:
			i = 0
			retSug, eraseSug, SugBig_sum, SugBig_sum_otherimg = self.betRecord.manualChangeSug(i, img, bet, isManual)
			
			row = SugBig_sum_otherimg[0]
			col = SugBig_sum_otherimg[1]
			if row >= 0 and col >= 0:
				self.grid_qlabelList[i][row][col].layout().itemAt(0).widget().setText('')
				self.grid_qlabelList[i][row][col].movie().setFileName(imgCell)
				self.grid_qlabelList[i][row][col].movie().start()
				self.grid_qlabelList[i][row][col].movie().stop()
			
			row = SugBig_sum[0]
			col = SugBig_sum[1]
			img = SugBig_sum[2]
			bet = SugBig_sum[3]
			if row >= 0 and col >= 0:
				if bet == 0:
					self.grid_qlabelList[i][row][col].layout().itemAt(0).widget().setText('')
					self.grid_qlabelList[i][row][col].movie().setFileName(imgCell)
				else:
					self.grid_qlabelList[i][row][col].layout().itemAt(0).widget().setText(str(bet))
					self.grid_qlabelList[i][row][col].layout().itemAt(0).widget().setStyleSheet('''.QLabel { font-family: Arial, Microsoft JhengHei, serif, sans-serif;
																									color: black; font-weight: bold; font-size: %dpt;}''' % self.sizeFontSize_Grid)
					self.grid_qlabelList[i][row][col].movie().setFileName(betRecord.imgSugPath[i][img])
				
				self.grid_qlabelList[i][row][col].movie().start()
				self.grid_qlabelList[i][row][col].movie().stop()
	
	def changeGridGif(self, i, row, col, img):
		self.controlGridGif()
		if row >= 0 and col >= 0:
			self.grid_qlabelList[i][row][col].movie().setFileName(self.betRecord.imgSugPath[i][img])
			self.grid_qlabelList[i][row][col].movie().start()
			self.grid_qlabelList[i][row][col].movie().stop()
	
	# control about sug GridGif
	def controlGridGif(self, control = False):
		for i in range(4):
			row = self.listForMovie[i][0]
			col = self.listForMovie[i][1]
			bet = self.listForMovie[i][3]
			if row >= 0 and col >= 0:
				self.grid_qlabelList[i][row][col].movie().stop()
				self.grid_qlabelList[i][row][col].movie().jumpToFrame(0)
				if control:
					# control = True, set Grid gif to start
					self.grid_qlabelList[i][row][col].movie().start()
	
	# reset all sug gif to sync the flicker
	def restartGridGif(self):
		self.controlGridGif()
		
		for i in range(4):
			row = self.listForMovie[i][0]
			col = self.listForMovie[i][1]
			img = self.listForMovie[i][2]
			bet = self.listForMovie[i][3]
			if row >= 0 and col >= 0:
				self.grid_qlabelList[i][row][col].layout().itemAt(0).widget().setStyleSheet('''.QLabel { font-family: Arial, Microsoft JhengHei, serif, sans-serif;
																								color: black; font-weight: bold; font-size: %dpt;}''' % self.sizeFontSize_Grid)
				
				self.grid_qlabelList[i][row][col].movie().start()
				self.grid_qlabelList[i][row][col].movie().stop()
		
		self.controlGridGif(True)
	
	def initialGridGifList(self):
		self.listForMovie = [(-1, -1, -1, -1), (-1, -1, -1, -1), (-1, -1, -1, -1), (-1, -1, -1, -1)]
	
	def storeRecordForHtml(self, countBet, sameBet, colorBet, pointBet):
		self.recordHtml_list.append((countBet, sameBet, colorBet, pointBet))
	
	def popRecordForHtml(self):
		self.recordHtml_list.pop()
	
	def backFromCutStop(self, removeList):
		LastCutStopStatus = self.betRecord.getLastCutStopStatus()
		for i in range(4):
			if LastCutStopStatus[i]:
				self.rbar_btn[i].setText(self.tr('開始'))
				self.rbar_btn[i].setStyleSheet('''.QPushButton {background-color: rgb(255, 255, 127); font-size: %dpt; font-family: Arial, Microsoft JhengHei, serif, sans-serif;}''' % self.sizeFontSize_Button)
			else:
				self.rbar_btn[i].setText(self.tr('停止'))
				self.rbar_btn[i].setStyleSheet('''.QPushButton {font-size: %dpt; font-family: Arial, Microsoft JhengHei, serif, sans-serif;}''' % self.sizeFontSize_Button)
			
			style = str(self.grid_qlabelList[i][removeList[i][0]][removeList[i][1]].layout().itemAt(0).widget().styleSheet())
			style = style.replace('{ border: 1px solid black;','{')
			self.grid_qlabelList[i][removeList[i][0]][removeList[i][1]].layout().itemAt(0).widget().setStyleSheet('''%s'''%style)
	
	def logGame(self, msg):
		log(msg)
		self.betRecord.logRecord()

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

def onTrail():
	timeNow = time.strftime("%Y %m %d %H", time.localtime(time.time())).split()
	yearNow = int(timeNow[0])
	monthNow = int(timeNow[1])
	dayNow = int(timeNow[2])
	hourNow = int(timeNow[3])
	
	if yearNow == 2016 and monthNow == 11 and dayNow <= 15 and dayNow >= 1:
		return True
	else:
		return False

def log(msg):
	if LOGLEVEL != 0:
		try:
			path = 'log'
			if not os.path.exists(path):
				os.makedirs(path)
			
			filename = path + '/%s.log' % startTime
			timeNow = time.strftime('%Y%m%d %H:%M:%S', time.localtime(time.time()))
			with open(filename, 'a') as file:
				file.write('[%s] %s\n' % (timeNow, str(msg)))
		except:
			pass

if __name__ == "__main__":
	app = QApplication(sys.argv)
	GridWindow = GridWindow()
	GridWindow.show()
	
	app.exec_()