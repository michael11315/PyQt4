import base64
import sys
import string
import time
import os
import random
from PyQt4.QtGui import *
from PyQt4.QtCore import *

class GridWindow(QWidget):
	def __init__(self, parent = None):
		super(GridWindow, self).__init__(parent)
		self.getFileDialog()
	
	def getFileDialog(self):
		onTrail = str(random.randint(100, 1000)) + time.strftime(':%Y%m%d', time.localtime(time.time()))
		fileDialog = QFileDialog(self, 'select the Baccarat.exe')
		fileDialog.setFileMode(QFileDialog.ExistingFile)
		if fileDialog.exec_():
			filepath = str(fileDialog.selectedFiles()[0])
			if os.path.basename(filepath) == 'Baccarat.exe':
				filepath = os.path.dirname(filepath)
				with open(filepath + '/img/OnTrail', 'w') as file:
					file.write(base64.b64encode(onTrail))
				sys.exit()
			else:
				fileDialog.close()
				self.getFileDialog()
		else:
			sys.exit()

if __name__ == "__main__":
	app = QApplication(sys.argv)
	GridWindow = GridWindow()
	GridWindow.show()
	
	app.exec_()