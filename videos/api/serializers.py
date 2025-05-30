from rest_framework import serializers
from videos.models import Video
from django.conf import settings
import logging
import subprocess
import os
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage

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
        fields = ('title', 'description', 'video_file', 'thumbnail')

    def create(self, validated_data):
        logger.info("create() aufgerufen – vor Video.objects.create")

        video_file = validated_data.pop('video_file')
        thumbnail = validated_data.pop('thumbnail', None)

        video = Video.objects.create(**validated_data)
        logger.info(f"Video erstellt mit ID: {video.id}")

        file_path = default_storage.save(f"videos/{video_file.name}", ContentFile(video_file.read()))
        video.video_file.name = file_path

        if thumbnail:
            thumb_path = default_storage.save(f"thumbnails/{thumbnail.name}", ContentFile(thumbnail.read()))
            video.thumbnail.name = thumb_path
            logger.info(f"Thumbnail gespeichert unter: {thumb_path}")

        video.save()

        try:
            self.process_video(video)
        except subprocess.CalledProcessError as e:
            logger.error(f"ffmpeg fehlgeschlagen: {e}")
            # Kein ValidationError – stattdessen expliziter 422 Fehler
            raise serializers.APIException(detail="Videoverarbeitung fehlgeschlagen (ffmpeg)", code=422)

        return video




    def process_video(self, video):
        logger.info(f"Beginne ffmpeg-Verarbeitung für Video ID {video.id}")

        video_path = os.path.join(settings.MEDIA_ROOT, video.video_file.name)
        hls_base_path = os.path.join(settings.MEDIA_ROOT, 'videos', 'hls', str(video.id))
        os.makedirs(hls_base_path, exist_ok=True)

        resolutions = {
            '1080p': '1920x1080',
            '720p': '1280x720',
            '480p': '854x480',
        }

        hls_segments_path = hls_base_path
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
                '-preset', 'veryfast',
                '-hls_time', '10',
                '-hls_playlist_type', 'event',
                '-hls_segment_filename', segment_path,
                output_path
            ]

            logger.info(f"Starte ffmpeg für {quality} mit Befehl: {' '.join(command)}")

            result = subprocess.run(command, check=True)

            rel_path = os.path.join('videos', 'hls', str(video.id), f'{quality}.m3u8')
            if quality == '1080p':
                video.video_file_1080p = rel_path
            elif quality == '720p':
                video.video_file_720p = rel_path
            elif quality == '480p':
                video.video_file_480p = rel_path

        # Playlist-Datei schreiben
        with open(playlist_path, 'w') as f:
            f.write("#EXTM3U\n")
            f.write("#EXT-X-VERSION:3\n")
            
            quality_bandwidths = {
                '1080p': 5000000,
                '720p': 3000000,
                '480p': 1000000,
            }

            for quality, resolution in resolutions.items():
                bandwidth = quality_bandwidths[quality]
                f.write(f"#EXT-X-STREAM-INF:BANDWIDTH={bandwidth},RESOLUTION={resolution},CODECS=\"avc1.4d001f,mp4a.40.2\"\n")
                f.write(f"{quality}.m3u8\n")


        video.hls_playlist_url = os.path.join('videos', 'hls', str(video.id), 'playlist.m3u8')
        video.save()
        logger.info(f"ffmpeg-Verarbeitung abgeschlossen für Video ID {video.id}")