from PyQt4.QtCore import *
from PyQt4.QtGui import *

class Widget(QWidget):
	def init(self, parent=None, **kwargs):
		QWidget.init(self, parent, **kwargs)
		self.resize(640,480)

		l=QHBoxLayout(self)

		self.l1=QVBoxLayout()
		self.label1=QLabel("QLabel<br />(centered)", self, alignment=Qt.AlignCenter)
		self.label1.setStyleSheet("border: 1px solid black;")
		self.label1.setFixedSize(100,50)
		self.l1.addWidget(self.label1, alignment=Qt.AlignCenter)
		l.addLayout(self.l1)

		self.l2=QVBoxLayout()
		self.label2=QLabel("QLabel<br />(centered)", self, alignment=Qt.AlignCenter)
		self.label2.setStyleSheet("border: 1px solid black;")
		self.label2.setFixedSize(100,50)
		self.l2.addWidget(self.label2, alignment=Qt.AlignCenter)
		l.addLayout(self.l2)

		fl=QFormLayout()

		self.label1pa=QLabel('0px', self)
		self.l1pa=QLabel('0px', self)
		self.label1pr=QLabel('0px', self)

		fl.addRow("Label 1 Position (absolute):", self.label1pa)
		fl.addRow("Layout 1 Position (absolute):", self.l1pa)
		fl.addRow("Label 1 Position (relative):", self.label1pr)

		self.label2pa=QLabel('0px', self)
		self.l2pa=QLabel('0px', self)
		self.label2pr=QLabel('0px', self)

		fl.addRow("Label 2 Position (absolute):", self.label2pa)
		fl.addRow("Layout 2 Position (absolute):", self.l2pa)
		fl.addRow("Label 2 Position (relative):", self.label2pr)
		l.addLayout(fl)

	def resizeEvent(self, event):
		QWidget.resizeEvent(self, event)

		label1pa=self.label1.geometry().topLeft()
		l1pa=self.l1.geometry().topLeft()
		label1pr=label1pa-l1pa

		self.label1pa.setText('({0},{1})px'.format(label1pa.x(), label1pa.y()))
		self.l1pa.setText('({0},{1})px'.format(l1pa.x(), l1pa.y()))
		self.label1pr.setText('({0},{1})px'.format(label1pr.x(), label1pr.y()))

		label2pa=self.label2.geometry().topLeft()
		l2pa=self.l2.geometry().topLeft()
		label2pr=label2pa-l2pa

		self.label2pa.setText('({0},{1})px'.format(label2pa.x(), label2pa.y()))
		self.l2pa.setText('({0},{1})px'.format(l2pa.x(), l2pa.y()))
		self.label2pr.setText('({0},{1})px'.format(label2pr.x(), label2pr.y()))
	
if __name__ == "__main__":
	from sys import argv, exit
	
	a=QApplication(argv)
	w=Widget()
	w.show()
	w.raise_()
	exit(a.exec_())