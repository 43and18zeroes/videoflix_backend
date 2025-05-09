from rest_framework import serializers
from videos.models import Video
from django.conf import settings

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