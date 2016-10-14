# -*- coding:utf-8 -*-

import sys
import types

from PyQt4 import Qt
from PyQt4 import QtCore
from PyQt4 import QtGui

import screen_window
from client import config_window


class systemTray(QtGui.QSystemTrayIcon):
    def __init__(self, parent, *args):
        QtGui.QSystemTrayIcon.__init__(self, parent, *args)

        self.setIcon(QtGui.QIcon('icon.ico'))

        menu = QtGui.QMenu(parent)
        self.configAction = QtGui.QAction('Config', menu)
        menu.addAction(self.configAction)
        self.aboutAction = QtGui.QAction('About', menu)
        menu.addAction(self.aboutAction)
        self.exitAction = QtGui.QAction('Exit', menu)
        menu.addAction(self.exitAction)

        self.setContextMenu(menu)

        self.activated.connect(self.on_activated)

        self.show()

    @QtCore.pyqtSlot(QtGui.QSystemTrayIcon.ActivationReason)
    def on_activated(self, e):
        if e == QtGui.QSystemTrayIcon.DoubleClick:
            if not isinstance(self.parent(), types.NoneType):
                if self.parent().isVisible():
                    self.parent().hide()
                else:
                    self.parent().show()
                    self.parent().activateWindow()


class MainWindow(QtGui.QWidget):
    def __init__(self):
        self.screen_window_list = list()

        QtGui.QWidget.__init__(self)

        self.system_tray = systemTray(self)

        self.system_tray.configAction.triggered.connect(self.configButtonClicked)
        self.system_tray.aboutAction.triggered.connect(self.aboutButtonClicked)
        self.system_tray.exitAction.triggered.connect(QtGui.qApp.quit)

        layout = QtGui.QVBoxLayout(self)

        h_boxlayout = QtGui.QHBoxLayout()
        h_boxlayout.addWidget(QtGui.QLabel('Server:'))
        self.serverLineEdit = QtGui.QLineEdit()
        self.serverLineEdit.setText('https://www.google.com')
        h_boxlayout.addWidget(self.serverLineEdit)
        layout.addLayout(h_boxlayout)

        h_boxlayout = QtGui.QHBoxLayout()
        h_boxlayout.addWidget(QtGui.QLabel('Password:'))
        self.passwordLineEdit = QtGui.QLineEdit()
        self.passwordLineEdit.setEchoMode(QtGui.QLineEdit.Password)
        self.passwordLineEdit.setText('123')
        h_boxlayout.addWidget(self.passwordLineEdit)
        layout.addLayout(h_boxlayout)

        h_boxlayout = QtGui.QHBoxLayout()
        self.hideButton = QtGui.QPushButton('&Hide')
        self.hideButton.clicked.connect(self.hideButtonClicked)
        h_boxlayout.addWidget(self.hideButton)
        self.configButton = QtGui.QPushButton('&Config')
        self.configButton.clicked.connect(self.configButtonClicked)
        h_boxlayout.addWidget(self.configButton)
        self.aboutButton = QtGui.QPushButton('&About')
        self.aboutButton.clicked.connect(self.aboutButtonClicked)
        h_boxlayout.addWidget(self.aboutButton)
        layout.addLayout(h_boxlayout)

        h_boxlayout = QtGui.QHBoxLayout()
        self.startButton = QtGui.QPushButton('&Start')
        h_boxlayout.addWidget(self.startButton)
        layout.addLayout(h_boxlayout)

        self.setWindowFlags(Qt.Qt.WindowCloseButtonHint
                            | Qt.Qt.WindowMinimizeButtonHint)

        self.setLayout(layout)
        self.setFixedSize(600, 225)
        self.setWindowTitle('Main Window')
        self.setWindowIcon(QtGui.QIcon('icon.ico'))

        # self.initScreenTestWindow()

        screen_count = QtGui.QDesktopWidget().screenCount()

        self.initScreenWindow(range(screen_count))

        self.show()



    def initScreenWindow(self, screen_list):
        for screen_id in screen_list:
            self.screen_window_list.append(screen_window.ScreenWindow(self, screen_id))

    @QtCore.pyqtSlot()
    def hideButtonClicked(self):
        self.hide()

    @QtCore.pyqtSlot()
    def configButtonClicked(self):
        con = config_window.ConfigWindow(self)

    @QtCore.pyqtSlot()
    def aboutButtonClicked(self):
        if not self.isVisible():
            self.show()
        QtGui.QMessageBox().about(self, 'About',
                                  u'''
                                  <strong>看什么看</strong>
                                  <p>就是个填坑中的弹幕小程序</p>
                                  <p>有什么好看的</p>
                                  <a href="https://github.com/Frederick-Zhu/danmu">https://github.com/Frederick-Zhu/danmu</a>
                                  ''')


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)

    main_window = MainWindow()

    sys.exit(app.exec_())
