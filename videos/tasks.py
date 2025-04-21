import subprocess
import os

def convert_video(source, resolution):
    width, height = map(int, resolution.split('x'))
    filename, ext = os.path.splitext(source)
    target = f"{filename}-{resolution}.mp4"
    cmd = f'ffmpeg -i "{source}" -s {width}x{height} -c:v libx264 -crf 23 -c:a aac -strict -2 "{target}"'
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        print(f"Conversion successful: {source} -> {target} ({resolution})")
        print(f"FFmpeg output:\n{result.stdout}")
        return target
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