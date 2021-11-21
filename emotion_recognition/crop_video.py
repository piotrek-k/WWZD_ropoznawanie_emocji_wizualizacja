"""
Skrypt do skracania filmów
"""

from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip

ffmpeg_extract_subclip("./test_images/inception.mp4", 30, 40, targetname="./test_images/inception_shortened.mp4")