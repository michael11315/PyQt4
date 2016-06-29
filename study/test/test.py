import sys
from PyQt4 import QtGui

app = QtGui.QApplication(sys.argv)

line_edit = QtGui.QLineEdit()
btn_go = QtGui.QPushButton("&GO")
layout_h1 = QtGui.QHBoxLayout()
layout_h1.addWidget(line_edit)
layout_h1.addWidget(btn_go)

btn_ok = QtGui.QPushButton("&OK")
btn_cancel = QtGui.QPushButton("&Cancel")
layout_h2 = QtGui.QHBoxLayout()
layout_h2.addStretch(1)
layout_h2.addWidget(btn_ok)
layout_h2.addWidget(btn_cancel)

layout_v1 = QtGui.QVBoxLayout()
layout_v1.addLayout(layout_h1)
layout_v1.addLayout(layout_h2)

widget = QtGui.QWidget()
widget.setLayout(layout_v1)
widget.show()

app.exec_()