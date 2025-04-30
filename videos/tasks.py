import subprocess
import os
from django.conf import settings

RESOLUTIONS_TO_CONVERT = ["854x480", "1280x720", "1920x1080"]

def convert_video(source, resolution):
    width, height = map(int, resolution.split('x'))
    filename, ext = os.path.splitext(source)
    target_dir = os.path.join(os.path.dirname(source), 'converted')
    os.makedirs(target_dir, exist_ok=True)
    target_name = f"{os.path.basename(filename)}-{resolution}.mp4"
    target_path = os.path.join(target_dir, target_name)
    relative_path = os.path.join('videos', 'converted', target_name)

    cmd = f'ffmpeg -i "{source}" -s {width}x{height} -c:v libx264 -crf 23 -c:a aac -strict -2 "{target_path}"'
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        print(f"Conversion successful: {source} -> {target_path} ({resolution})")
        print(f"FFmpeg output:\n{result.stdout}")
        return relative_path
    except subprocess.CalledProcessError as e:
        print(f"Conversion error ({resolution}): {e}")
        print(f"FFmpeg error:\n{e.stderr}")
        return None
    except FileNotFoundError:
        print("Error: ffmpeg not found. Please check the path.")
        return None

def convert_480p(source):
    return convert_video(source, "854x480")

def convert_720p(source):
    return convert_video(source, "1280x720")

def convert_1080p(source):
    return convert_video(source, "1920x1080")