import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *

app = QApplication(sys.argv)

spinBox = QSpinBox()
spinBox.setPrefix("$")
spinBox.setRange(0, 100)

slider = QSlider(Qt.Horizontal)
slider.setRange(0, 100)

spinBox.valueChanged.connect(slider.setValue)
slider.valueChanged.connect(spinBox.setValue)

layout = QHBoxLayout()
layout.addWidget(spinBox)
layout.addWidget(slider)

widget = QWidget()
widget.setLayout(layout)
widget.show()

app.exec_()