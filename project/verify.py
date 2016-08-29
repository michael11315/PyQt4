import base64
import sys
import string
import time
import os
import random
from PyQt4.QtGui import *
from PyQt4.QtCore import *

QTextCodec.setCodecForTr(QTextCodec.codecForName("utf8"))

class GridWindow(QWidget):
	def __init__(self, parent = None):
		super(GridWindow, self).__init__(parent)
		self.getFileDialog()
	
	def getFileDialog(self):
		path = 'C:/Python/record'
		if not os.path.exists(path):
			os.makedirs(path)
		
		onTrail = str(random.randint(100, 1000)) + time.strftime(':%Y%m%d', time.localtime(time.time()))
		with open(path + '/OnTrail', 'w') as file:
			file.write(base64.b64encode(onTrail))
		
		Record = str(random.randint(100, 1000)) + time.strftime(':%Y%m%d%H%M%S', time.localtime(time.time()))
		with open(path + '/Record', 'w') as file:
			file.write(base64.b64encode(Record))
		
		msgBox = QMessageBox(self)
		msgBox.setIcon(QMessageBox.Information)
		msgBox.setText(self.tr('認證完成'))
		msgBox.exec_()
		
		sys.exit()

if __name__ == "__main__":
	app = QApplication(sys.argv)
	GridWindow = GridWindow()
	GridWindow.show()
	
	app.exec_()