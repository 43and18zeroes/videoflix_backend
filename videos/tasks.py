import subprocess
import os

def convert_480p(source):
    filename, ext = os.path.splitext(source)
    target = f"{filename}_480p.mp4"
    cmd = f'ffmpeg -i "{source}" -s 854x480 -c:v libx264 -crf 23 -c:a aac -strict -2 "{target}"'
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        print(f"Konvertierung erfolgreich: {source} -> {target}")
        print(f"FFmpeg Ausgabe:\n{result.stdout}")
        return target
    except subprocess.CalledProcessError as e:
        print(f"Fehler bei der FFmpeg-Konvertierung: {e}")
        print(f"FFmpeg Fehler:\n{e.stderr}")
        return None
    except FileNotFoundError:
        print("Fehler: ffmpeg nicht gefunden. Stellen Sie sicher, dass es in Ihrem Pfad ist.")
        return None