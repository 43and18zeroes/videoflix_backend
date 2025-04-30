import subprocess
import os
from django.conf import settings

RESOLUTIONS_TO_CONVERT = ["854x480", "1280x720", "1920x1080"]

def convert_to_hls(source):
    import subprocess
    import os

    filename, _ = os.path.splitext(os.path.basename(source))
    output_dir = os.path.join(os.path.dirname(source), 'hls', filename)
    os.makedirs(output_dir, exist_ok=True)

    output_path = os.path.join(output_dir, 'master.m3u8')
    relative_master_path = os.path.join('videos', 'hls', filename, 'master.m3u8')

    # Einfache HLS-Konvertierung mit drei Auflösungen und sicherem Mapping
    cmd = [
        'ffmpeg', '-y', '-i', source,
        '-filter_complex',
        "[0:v]split=3[v1][v2][v3];"
        "[v1]scale=w=854:h=480[v1out];"
        "[v2]scale=w=1280:h=720[v2out];"
        "[v3]scale=w=1920:h=1080[v3out]",
        '-map', '[v1out]',
        '-map', '0:a?',  # <-- das Fragezeichen erlaubt "optional"
        '-c:v:0', 'libx264', '-b:v:0', '800k',
        '-c:a:0', 'aac', '-ac:0', '2', '-b:a:0', '128k',

        '-map', '[v2out]',
        '-map', '0:a?',
        '-c:v:1', 'libx264', '-b:v:1', '2800k',
        '-c:a:1', 'aac', '-ac:1', '2', '-b:a:1', '128k',

        '-map', '[v3out]',
        '-map', '0:a?',
        '-c:v:2', 'libx264', '-b:v:2', '5000k',
        '-c:a:2', 'aac', '-ac:2', '2', '-b:a:2', '128k',

        '-f', 'hls',
        '-hls_time', '6',
        '-hls_playlist_type', 'vod',
        '-master_pl_name', 'master.m3u8',
        '-var_stream_map', 'v:0,a:0 v:1,a:1 v:2,a:2',
        os.path.join(output_dir, 'output_%v.m3u8'),
    ]

    try:
        print("FFmpeg command:", " ".join(cmd))
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        print("HLS conversion successful.")
        print(result.stdout)
        return relative_master_path
    except subprocess.CalledProcessError as e:
        print("HLS conversion failed:")
        print(e.stderr)
        return None
