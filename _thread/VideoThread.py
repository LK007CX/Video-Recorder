#!/usr/bin/python3
# -*- coding: UTF-8 -*-
import sys
import time
import xml.etree.ElementTree as ET

import cv2
import numpy as np
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import QApplication

from utils.ArgsHelper import ArgsHelper
from utils.camera import Camera
from utils.display import show_fps


class VideoThread(QThread):
    image_Signal = pyqtSignal(np.ndarray)

    def __init__(self, config_path, *args, **kwargs):
        super(VideoThread, self).__init__(*args, **kwargs)
        self._args = self._load_config(config_path)
        self._cam = Camera(self._args)


    def _load_config(self, config_path):
        # try:
        tree = ET.parse(config_path)
        root = tree.getroot()

        image = root.find('camera').find('image').text
        image = None if image == 'None' else image

        video = root.find('camera').find('video').text
        video = None if video == 'None' else video

        video_looping = root.find('camera').find('video_looping').text
        video_looping = True if video_looping == 'True' else False

        rtsp = root.find('camera').find('rtsp').text
        rtsp = None if rtsp == 'None' else rtsp

        rtsp_latency = root.find('camera').find('rtsp_latency').text
        rtsp_latency = int(rtsp_latency)

        usb = root.find('camera').find('usb').text
        usb = None if usb == 'None' else int(usb)

        gstr = root.find('camera').find('gstr').text
        gstr = None if gstr == 'gstr' else gstr

        onboard = root.find('camera').find('onboard').text
        onboard = None if onboard == 'None' else int(onboard)

        copy_frame = root.find('camera').find('copy_frame').text
        copy_frame = False if copy_frame == 'False' else True

        do_resize = root.find('camera').find('do_resize').text
        do_resize = False if do_resize == 'False' else True

        width = root.find('camera').find('width').text
        width = int(width)

        height = root.find('camera').find('height').text
        height = int(height)
        # except Exception as e:
        #     print(e)
        args = ArgsHelper(image=image, video=video, video_looping=video_looping, rtsp=rtsp,
                          rtsp_latency=rtsp_latency, usb=usb, gstr=gstr, onboard=onboard,
                          copy_frame=copy_frame, do_resize=do_resize, width=width, height=height)
        return args

    def run(self):
        if not self._cam.is_opened:
            print("打开相机失败")
        fps = 0
        tic = time.time()
        while True:
            img = self._cam.read()
            if img is None:
                print("没有相机数据")
            img = show_fps(img, fps)
            cv2.imshow(img)
            self.image_Signal.emit(img)
            toc = time.time()
            curr_fps = 1.0 / (toc - tic)
            # calculate the average value of exponential decay of FPS number
            fps = curr_fps if fps == 0.0 else (fps * 0.95 + curr_fps * 0.05)
            tic = toc


if __name__ == '__main__':
    app = QApplication(sys.argv)
    thread = VideoThread('../appconfig/appconfig.xml')
    thread.start()
    sys.exit(app.exec_())
