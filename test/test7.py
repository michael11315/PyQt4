import sys
from PyQt4.QtGui import *
from PyQt4.QtCore import *

# show width and height
sizeHint()

# home size
PyQt4.QtCore.QSize(1239, 902)
PyQt4.QtCore.QSize(1251, 917)

# blue
setStyleSheet('background-color: rgb(0, 85, 255);')

# set alignment
self.tbar_qlabel[i].setAlignment(Qt.AlignCenter)

# set sizePolicy
sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
setSizePolicy(sizePolicy)

# set item bottom border in list widget
myListWidget->setStyleSheet( "QListWidget::item { border-bottom: 1px solid black; }" );

# 按鈕的連結
#----------------------------------------------------
QObject.connect(self.lbar_btn[0], SIGNAL("clicked()"), self.test_frame.show)
QObject.connect(self.lbar_btn[1], SIGNAL("clicked()"), self.binp_qframe.close)

# 中文字處理
#----------------------------------------------------
# 支援 utf8
QTextCodec.setCodecForTr(QTextCodec.codecForName("utf8"))
# 設 utf8 字串
self.lbar_qlabel.setText(self.tr('哈哈'))
# 印出 utf8 字串
print self.lbar_qlabel.text().toUtf8()

# 顯示滑鼠位置(要放在 widget class中)
#----------------------------------------------------
# 滑鼠在視窗內的位置
def mousePressEvent(self, QMouseEvent):
	print 'pos in the widget', QMouseEvent.pos()
	
# 滑鼠在螢幕中的位置
def mouseReleaseEvent(self, QMouseEvent):
	cursor = QCursor()
	print 'pos in the windows screen', cursor.pos()

# mouse press and release
def clickable(widget):
	class Filter(QObject):
		
		clicked = pyqtSignal()
		
		def eventFilter(self, obj, event):
			if obj == widget:
				if event.type() == QEvent.MouseButtonRelease:
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
				if event.type() == QEvent.MouseButtonPress:
					if obj.rect().contains(event.pos()):
						self.clicked.emit()
						# The developer can opt for .emit(obj) to get the object within the slot.
						return True
			
			return False
	
	filter = Filter(widget)
	widget.installEventFilter(filter)
	return filter.clicked

		self.pbet_qlabel1.setText(self.tr('莊'))
		clickable(self.pbet_qlabel1).connect(self.showText1)
		pressed(self.pbet_qlabel1).connect(self.showText3)
		
		pixmap = QPixmap('../img/grey.jpg')
		self.pbet_qlabel2.setPixmap(pixmap)
		self.pbet_qlabel2.setScaledContents(True)
		self.pbet_qlabel2.mousePressEvent = self.showText2
		
	def showText1(self):
		pixmap = QPixmap('../img/grey.jpg')
		self.pbet_qlabel2.setPixmap(pixmap)
		#self.pbet_qlabel2.setScaledContents(True)
		print 'haha'
		
	def showText2(self, event):
		print 'haha'
		
	def showText3(self):
		pixmap = QPixmap('../img/red.jpg')
		self.pbet_qlabel2.setPixmap(pixmap)
		#self.pbet_qlabel2.setScaledContents(True)
		print 'haha'