from moviepy.editor import *
#from moviepy.video.compositing import CompositeVideoClip

clip1 = VideoFileClip("videos/v1.mp4")
clip2 = VideoFileClip("videos/v2.mp4")

clip1 = clip1.subclip(t_end=10)
clip2 = clip2.subclip(t_end=10)

clip2 = clip2.resize(0.5)
video = CompositeVideoClip([clip1.subclip(t_end=clip2.end), clip2.set_pos(("right","bottom"))], use_bgclip=True)

video.write_videofile("ext.mp4")

