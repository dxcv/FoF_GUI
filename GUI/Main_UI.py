# -*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon

class MainWindow(QMainWindow):
    '''
    This is the main window part of the software.
    '''
    def __init__(self):
        super().__init__()

        self.MainUI()

    def MainUI(self):

        # 设置主页面框架
        self.resize(640, 480)
        self.center()

        # 新增菜单栏及按钮属性
        # 选择文件
        openAction = QAction("&Open", self)
        openAction.setShortcut("Ctrl+O")
        openAction.setStatusTip("Open File")
        openAction.triggered.connect(self.openFile)
        # 选择文件夹
        openDAction = QAction("&Open FileD", self)
        openDAction.setShortcut("Ctrl+D")
        openDAction.setStatusTip("Open File Directory")
        openDAction.triggered.connect(self.openDFile)
        # 退出
        exitAction = QAction("&Exit", self)
        exitAction.setShortcut("Ctrl+Q")
        exitAction.setStatusTip("Exit Application")
        exitAction.triggered.connect(qApp.quit)
        # 关于
        aboutAction = QAction("&About", self)
        aboutAction.setStatusTip("About Application")
        aboutAction.triggered.connect(self.about)

        menubar = self.menuBar()
        fileMenu = menubar.addMenu("&File")
        fileMenu.addAction(openAction)
        fileMenu.addAction(openDAction)
        fileMenu.addAction(exitAction)

        helpMenu = menubar.addMenu("&Help")
        helpMenu.addAction(aboutAction)

        self.statusBar()

        # 设置状态属性
        self.statusBar().showMessage("Ready")

        # 标题
        self.setWindowTitle('投顾复盘系统')
        self.show()

    def openFile(self):
        filename = QFileDialog.getOpenFileName(self, "Open File")
        print(filename)

    def openDFile(self):
        dir_path = QFileDialog.getExistingDirectory(self, "Choose File Directory")
        print(dir_path)


    def about(self):
        QMessageBox.about(self, "About", \
        '''投顾复盘系统V1.0版本\n\n开发人员： 张晨、史龙龙\n\n日期：2017-06-14''')

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    sys.exit(app.exec_())