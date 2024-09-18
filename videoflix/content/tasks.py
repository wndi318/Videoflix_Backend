import subprocess
import os
from django.conf import settings

def convert_480p(source):
    target = source.replace(".mp4", "_480p.mp4")
    cmd = [
        'ffmpeg', '-i', source, '-s', 'hd480', '-c:v', 'libx264', '-crf', '23', '-c:a', 'aac', '-strict', '-2', target
    ]
    subprocess.run(cmd, check=True)

def convert_720p(source):
    target = source.replace(".mp4", "_720p.mp4")
    cmd = [
        'ffmpeg', '-i', source, '-s', 'hd720', '-c:v', 'libx264', '-crf', '23', '-c:a', 'aac', '-strict', '-2', target
    ]
    subprocess.run(cmd, check=True)

def convert_1080p(source):
    target = source.replace(".mp4", "_1080p.mp4")
    cmd = [
        'ffmpeg', '-i', source, '-s', 'hd1080', '-c:v', 'libx264', '-crf', '23', '-c:a', 'aac', '-strict', '-2', target
    ]
    subprocess.run(cmd, check=True)


def create_thumbnail(source):
    video_dir = os.path.dirname(source)
    thumbnails_dir = os.path.join(video_dir, "thumbnails")
    if not os.path.exists(thumbnails_dir):
        os.makedirs(thumbnails_dir)
    target = os.path.join(thumbnails_dir, os.path.basename(source).replace(".mp4", "_thumbnail.jpg"))
    cmd = [
        'ffmpeg', '-i', source, '-ss', '00:00:01.000', '-vframes', '1', target
    ]
    try:
        subprocess.run(cmd, check=True)
        print(f"Thumbnail created: {target}")
    except subprocess.CalledProcessError as e:
        print(f"Error creating thumbnail: {e}")
    relative_path = os.path.relpath(target, settings.MEDIA_ROOT)
    return relative_path