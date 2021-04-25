#!/usr/bin/python3
# -*- coding: UTF-8 -*-
import sys

from PyQt5.QtWidgets import QApplication

from ui.MainWindow import MainWindow

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MainWindow('appconfig/appconfig.xml')
    win.show()
    sys.exit(app.exec_())