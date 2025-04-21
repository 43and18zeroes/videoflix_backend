import subprocess
import os

def convert_480p(source):
    filename, ext = os.path.splitext(source)
    target = f"{filename}-480p.mp4"
    cmd = f'ffmpeg -i "{source}" -s 854x480 -c:v libx264 -crf 23 -c:a aac -strict -2 "{target}"'
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        print(f"Conversion successful: {source} -> {target}")
        print(f"FFmpeg output:\n{result.stdout}")
        return target
    except subprocess.CalledProcessError as e:
        print(f"Conversion error: {e}")
        print(f"FFmpeg error:\n{e.stderr}")
        return None
    except FileNotFoundError:
        print("Error: ffmpeg not found. Please check the path.")
        return None
    
def convert_720p(source):
    filename, ext = os.path.splitext(source)
    target = f"{filename}-720p.mp4"
    cmd = f'ffmpeg -i "{source}" -s 1280x720 -c:v libx264 -crf 23 -c:a aac -strict -2 "{target}"'
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        print(f"Conversion successful: {source} -> {target}")
        print(f"FFmpeg output:\n{result.stdout}")
        return target
    except subprocess.CalledProcessError as e:
        print(f"Conversion error: {e}")
        print(f"FFmpeg error:\n{e.stderr}")
        return None
    except FileNotFoundError:
        print("Error: ffmpeg not found. Please check the path.")
        return None