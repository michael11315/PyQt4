import sys
from PyQt4.QtGui import *

app = QApplication(sys.argv)
widget = QWidget()
widget.setGeometry(300, 100, 500, 450)

#使用CSS語法調整樣式
widget.setStyleSheet("""
    QLineEdit{
        border : 5px solid brown;
    }
    QTextEdit{
        border : 5px double;
    }
    """)

#標籤內可以夾雜css語法
title = QLabel('<font color=blue>Title</font>')
author = QLabel('<font color=blue>Author</font>')
review = QLabel('<font color=red>Review</font>')
titleEdit = QLineEdit()
authorEdit = QLineEdit()
reviewEdit = QTextEdit()

grid = QGridLayout()

#設置排列後每列的間隔
grid.setSpacing(10)

#指定每個元件的列和行(後兩個參數為列、行)
grid.addWidget(title, 1, 0)
grid.addWidget(titleEdit, 1, 1)
grid.addWidget(author, 2, 0)
grid.addWidget(authorEdit, 2, 1)
grid.addWidget(review, 3, 0)

#四個參數分別為 row, col, rowspan, colspan
grid.addWidget(reviewEdit, 3, 1, 3, 3)

#讓主視窗套用剛剛設定的排列方法
widget.setLayout(grid)

widget.show()
app.exec_()