# -*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QTextEdit, QGridLayout, QApplication
# from PyQt5.QtWidgets import (QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QApplication)
# P37

class Example(QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):

        title = QLabel('Title')
        author = QLabel('Author')
        review = QLabel('Review')

        titleEdit = QLineEdit()
        authorEdit = QLineEdit()
        reviewEdit = QTextEdit()

        grid = QGridLayout()
        grid.setSpacing(10)

        grid.addWidget(title, 1, 0)
        grid.addWidget(titleEdit, 1, 1)

        grid.addWidget(author, 2, 0)
        grid.addWidget(authorEdit, 2, 1)

        grid.addWidget(review, 3, 0)
        grid.addWidget(reviewEdit, 3, 1, 5, 1)

        self.setLayout(grid)

        # lbl1 = QLabel('Zetcode', self)
        # lbl1.move(15, 10)
        #
        # lbl2 = QLabel('tutorials', self)
        # lbl2.move(35, 40)
        #
        # lbl3 = QLabel('for programmers', self)
        # lbl3.move(55, 70)

        self.setGeometry(300, 300, 350, 300)
        self.setWindowTitle('Review')
        # self.setWindowTitle('Absolute')
        # self.setWindowIcon(QIcon('web.png')) # 图标样式
        #
        self.show()

if __name__ == '__main__':

    app = QApplication(sys.argv)

    ex = Example()
    # w = QWidget()
    # w.resize(250, 150)
    # w.move(300, 300)
    # w.setWindowTitle('Simple')
    # w.show()

    sys.exit(app.exec_())

