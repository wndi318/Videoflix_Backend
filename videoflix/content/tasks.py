import subprocess
import os

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
    target = os.path.join(os.path.dirname(source), "thumbnails", os.path.basename(source).replace(".mp4", "_thumbnail.jpg"))
    cmd = [
        'ffmpeg', '-i', source, '-ss', '00:00:01.000', '-vframes', '1', target
    ]
    subprocess.run(cmd, check=True)
    print(f"Thumbnail created: {target}")