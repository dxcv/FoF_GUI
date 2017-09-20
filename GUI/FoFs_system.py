from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

import sys

class MainWindow(QMainWindow):
    '''
    This is the main window of the FOF management system.
    '''
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.MainUI()

    def MainUI(self):

        # 设置主页面框架
        self.resize(640, 480)
        self.center()

        # 新增菜单栏及按钮属性
        menubar = self.menuBar()

        ########################################################
        # 文件菜单栏
        file_Menu = menubar.addMenu("&File")

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

        # 增加控件
        file_Menu.addAction(openAction)
        file_Menu.addAction(openDAction)
        file_Menu.addSeparator()
        file_Menu.addAction(exitAction)

        ########################################################
        # 帮助菜单栏
        help_Menu = menubar.addMenu("&Help")
        # 关于
        aboutAction = QAction("&About", self)
        aboutAction.setStatusTip("About Application")
        aboutAction.triggered.connect(self.about)

        # 增加控件
        help_Menu.addAction(aboutAction)

        ########################################################
        # 网格布局
        grid = QGridLayout()


        ########################################################
        self.statusBar()

        # 标题
        self.setWindowTitle('FoF Management System -- V1.0')

        ########################################################

        self.show()

    def openFile(self):
        filename = QFileDialog.getOpenFileName(self, "Open File")
        print(filename)

    def openDFile(self):
        dir_path = QFileDialog.getExistingDirectory(self, "Choose File Directory")
        print(dir_path)


    def about(self):
        QMessageBox.about(self, "About - V1.0", \
        '''投顾复盘系统V1.0版本\n\n开发人员： 张晨\n\n日期：2017-09-18''')

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    sys.exit(app.exec_())
