#!/usr/bin/python3
# -*- coding: UTF-8 -*-


class ArgsHelper(object):
    __slots__ = 'image', 'video', 'video_looping', 'rtsp', \
                'rtsp_latency', 'usb', 'gstr', 'onboard', \
                'copy_frame', 'do_resize', 'width', 'height'

    def __init__(self, *args, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)
