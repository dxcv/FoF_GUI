# -*- coding: utf-8 -*-
'''
PyQt5 tutorial Page27
'''
import sys
from PyQt5.QtWidgets import QMainWindow, QTextEdit, QAction, QApplication
from PyQt5.QtGui import QIcon

class Example(QMainWindow):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):

        textEdit = QTextEdit()
        self.setCentralWidget(textEdit)

        exitAction = QAction(QIcon('exit24.png'), 'Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip(u'关闭程序')
        exitAction.triggered.connect(self.close)

        self.statusBar()

        menubar = self.menuBar()
        fileMenu = menubar.addMenu(u'文件')
        fileMenu.addAction(exitAction)

        toolbar = self.addToolBar('退出')
        toolbar.addAction(exitAction)

        self.setGeometry(300, 300, 300, 200)
        # self.setWindowTitle('Menubar')
        self.setWindowTitle('Main Window')
        self.show()

if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())