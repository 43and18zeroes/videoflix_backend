from rest_framework import serializers
from videos.models import Video
from django.conf import settings
import logging
import subprocess
import os

logger = logging.getLogger(__name__)

class VideoSerializer(serializers.ModelSerializer):
    hls_playlist_url = serializers.SerializerMethodField()
    category = serializers.SerializerMethodField()  # <-- hier änderst du es

    class Meta:
        model = Video
        fields = ['id', 'title', 'description', 'upload_date', 'video_file', 'thumbnail', 'duration', 'views', 'hls_playlist_url', 'category']
        read_only_fields = ['id', 'upload_date', 'views', 'hls_playlist_url']

    def get_hls_playlist_url(self, obj):
        if obj.hls_playlist_url:
            return self.context['request'].build_absolute_uri(f'{settings.MEDIA_URL}{obj.hls_playlist_url}')
        return None
    
    def get_category(self, obj):
        return obj.get_category_display()
    

logger = logging.getLogger(__name__)

class VideoUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = ('title', 'description', 'video_file')

    def create(self, validated_data):
        logger.info("VideoUploadSerializer.create() start")

        video_file = validated_data.pop('video_file')
        video = Video.objects.create(**validated_data)

        # Datei ans Model hängen und speichern
        video.video_file = video_file
        video.save()

        try:
            self.process_video(video)
        except subprocess.CalledProcessError as e:
            logger.error(f"Videoverarbeitung fehlgeschlagen: {e}")
            logger.error(f"stdout: {e.stdout}")
            logger.error(f"stderr: {e.stderr}")
            raise serializers.ValidationError("Fehler bei der Videoverarbeitung.")

        return video

    def process_video(self, video):
        logger.info(f"Starte Videokonvertierung für Video ID {video.id}")

        video_path = os.path.join(settings.MEDIA_ROOT, video.video_file.name)
        hls_base_path = os.path.join(settings.MEDIA_ROOT, 'videos', 'hls', str(video.id))
        os.makedirs(hls_base_path, exist_ok=True)

        resolutions = {
            '1080p': '1920x1080',
            '720p': '1280x720',
            '480p': '854x480',
        }

        hls_segments_path = os.path.join(hls_base_path, '%v')
        playlist_path = os.path.join(hls_base_path, 'playlist.m3u8')

        for quality, resolution in resolutions.items():
            output_path = os.path.join(hls_base_path, f'{quality}.m3u8')
            segment_path = os.path.join(hls_segments_path, f'{quality}_%05d.ts')

            command = [
                'ffmpeg',
                '-i', video_path,
                '-vf', f'scale={resolution}',
                '-c:a', 'aac',
                '-ar', '48000',
                '-c:v', 'libx264',
                '-crf', '22',
                '-preset', 'slow',
                '-hls_time', '10',
                '-hls_playlist_type', 'event',
                '-hls_segment_filename', segment_path,
                output_path
            ]

            logger.info(f"Führe ffmpeg aus für {quality}: {command}")
            subprocess.run(command, check=True, capture_output=True)

            if quality == '1080p':
                video.video_file_1080p = os.path.join('videos', 'hls', str(video.id), f'{quality}.m3u8')
            elif quality == '720p':
                video.video_file_720p = os.path.join('videos', 'hls', str(video.id), f'{quality}.m3u8')
            elif quality == '480p':
                video.video_file_480p = os.path.join('videos', 'hls', str(video.id), f'{quality}.m3u8')

        # Playlist schreiben
        with open(playlist_path, 'w') as f:
            f.write("#EXTM3U\n")
            for quality, resolution in resolutions.items():
                f.write(f"#EXT-X-MEDIA:TYPE=VIDEO,GROUP-ID=\"v{quality}\",NAME=\"{quality}\",AUTOSELECT=YES,DEFAULT=NO\n")
                f.write(f"#EXT-X-STREAM-INF:BANDWIDTH=1280000,RESOLUTION={resolution},CODECS=\"avc1.4d001f,mp4a.40.2\",MEDIA=\"v{quality}\"\n")
                f.write(f"{quality}.m3u8\n")

        video.hls_playlist_url = os.path.join('videos', 'hls', str(video.id), 'playlist.m3u8')
        video.save()
        logger.info(f"Videoverarbeitung für Video ID {video.id} abgeschlossen")
