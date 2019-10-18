import os
from moviepy.editor import CompositeVideoClip, VideoFileClip
from moviepy.video.fx.all import crop
from contextlib import redirect_stdout

import sys

class Logger(object):
    def __init__(self, filename="Default.log"):
        self.terminal = sys.stdout
        self.log = open(filename, "a")

    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)

class Flick:

    def __init__(self, back_video, over_video, ext_video):
        self.resize_factor = 0.5

        self.v1 = crop(VideoFileClip(back_video), y1=104, y2=860)
        self.v2 = VideoFileClip(over_video)
        self.v3 = None
        self.pos = (0, 0)
        self.v3_name = ext_video

    def _get_position(self):
        self.pos = (self.v1.w - self.v2.w - 50, self.v1.h - self.v2.h - 50)

    def _resize_v2(self):
        self.resize_factor = self.v1.h * 0.2 / self.v2.h
        self.v2 = self.v2.resize(self.resize_factor)

    def _trim_v1(self):
        self.v1 = self.v1.subclip(t_end=self.v2.end)

    def _make_adjustments(self):
        
        self._trim_v1()
        self._resize_v2()
        self._get_position()

    def compute_video(self):
        self.v3 = CompositeVideoClip([self.v1, self.v2.set_pos(self.pos)], use_bgclip=True)
    
    def write_video(self):
        if os.path.isfile(self.v3_name):
            return -1
        else:
            return self.v3.write_videofile(self.v3_name)


    def run(self):

        sys.stdout = Logger()

        self._make_adjustments()
        self.compute_video()
        return self.write_video()
