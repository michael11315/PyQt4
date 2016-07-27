# pos in the main widget
	def mousePressEvent(self, QMouseEvent):
		#print 'pos in the widget', QMouseEvent.pos()
		pass
	
	# pos in the windows screen
	def mouseReleaseEvent(self, QMouseEvent):
		cursor = QCursor()
		#print 'pos in the windows screen', cursor.pos()