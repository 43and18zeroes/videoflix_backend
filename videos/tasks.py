import subprocess
import os
from django.conf import settings

def convert_to_hls(source):
    filename, _ = os.path.splitext(os.path.basename(source))
    output_dir = os.path.join(os.path.dirname(source), 'hls', filename)
    os.makedirs(output_dir, exist_ok=True)

    output_path = os.path.join(output_dir, 'master.m3u8')

    # Prüfen, ob Input Audio enthält
    has_audio = False
    try:
        ffprobe_cmd = ['ffprobe', '-v', 'error', '-select_streams', 'a', '-show_entries', 'stream=codec_type', '-of', 'default=noprint_wrappers=1', source]
        ffprobe_result = subprocess.run(ffprobe_cmd, capture_output=True, text=True, check=True)
        has_audio = 'codec_type=audio' in ffprobe_result.stdout
    except Exception as e:
        print("ffprobe failed:", e)

    filter_complex = (
        "[0:v]split=3[v1][v2][v3];"
        "[v1]scale=w=854:h=480[v1out];"
        "[v2]scale=w=1280:h=720[v2out];"
        "[v3]scale=w=1920:h=1080[v3out]"
    )

    cmd = [
        'ffmpeg', '-y', '-i', source,
        '-filter_complex', filter_complex,
    ]

    var_stream_map = []

    for i, (label, bitrate) in enumerate(zip(
        ['v1out', 'v2out', 'v3out'],
        ['800k', '2800k', '5000k']
    )):
        cmd += ['-map', f'[{label}]']
        if has_audio:
            cmd += ['-map', '0:a']
            cmd += ['-c:a:' + str(i), 'aac', '-b:a:' + str(i), '128k']
            var_stream_map.append(f"v:{i},a:{i}")
        else:
            var_stream_map.append(f"v:{i}")

        cmd += ['-c:v:' + str(i), 'libx264', '-b:v:' + str(i), bitrate]

    cmd += [
        '-f', 'hls',
        '-hls_time', '6',
        '-hls_playlist_type', 'vod',
        '-hls_segment_filename', os.path.join(output_dir, 'output_%v_%03d.ts'),
        '-master_pl_name', 'master.m3u8',
        '-var_stream_map', ' '.join(var_stream_map),
        os.path.join(output_dir, 'output_%v.m3u8'),
    ]

    try:
        print("FFmpeg command:", " ".join(cmd))
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        print("HLS conversion successful.")
        print(result.stdout)

        relative_master_path = os.path.relpath(output_path, settings.MEDIA_ROOT)
        return relative_master_path
    except subprocess.CalledProcessError as e:
        print("HLS conversion failed:")
        print(e.stderr)
        return None
