#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import sys

from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QMainWindow, QApplication, QHBoxLayout, QWidget

from ui.VideoWidget import VideoWidget
from _thread.VideoThread import VideoThread


class MainWindow(QMainWindow):

    def __init__(self, config_path, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self._videoWidget = VideoWidget()
        self._init_ui()
        self._video_thread = VideoThread(config_path)

    def _init_ui(self):
        # self._videoWidget.setFixedSize(QSize(960, 540))
        layout = QHBoxLayout(spacing=0)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self._videoWidget)
        centralWidget = QWidget()
        centralWidget.setLayout(layout)
        self.setCentralWidget(centralWidget)
        self.resize(QSize(1280, 720))

    def _init_thread(self):
        self._video_thread.image_Signal.connect(self._videoWidget.handleDisplay)
        self._video_thread.start()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MainWindow('../appconfig/appconfig.xml')
    win.show()
    sys.exit(app.exec_())
