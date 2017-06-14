# -*- coding: utf-8 -*-

import sys
# from PyQt5.QtWidgets import QWidget, QLabel, QApplication
from PyQt5.QtWidgets import (QMainWindow, QDesktopWidget, QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QApplication)


class ApplicationWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):

        okButton = QPushButton('OK')
        cancelButton = QPushButton('Cancel')

        hbox = QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(okButton)
        hbox.addWidget(cancelButton)

        vbox = QVBoxLayout()
        vbox.addStretch(1)
        vbox.addLayout(hbox)

        self.setLayout(vbox)

        # lbl1 = QLabel('Zetcode', self)
        # lbl1.move(15, 10)
        #
        # lbl2 = QLabel('tutorials', self)
        # lbl2.move(35, 40)
        #
        # lbl3 = QLabel('for programmers', self)
        # lbl3.move(55, 70)

        self.setGeometry(300, 300, 250, 150)
        self.setWindowTitle('Buttons')
        # self.setWindowTitle('Absolute')
        # self.setWindowIcon(QIcon('web.png')) # 图标样式
        #
        self.show()

    def center(self):

        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

if __name__ == '__main__':

    app = QApplication(sys.argv)

    ex = ui_Main()

    sys.exit(app.exec_())

