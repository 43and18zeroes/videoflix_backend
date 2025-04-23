from rest_framework import serializers
from videos.models import Video

class VideoSerializer(serializers.ModelSerializer):
    thumbnail_url = serializers.SerializerMethodField()
    video_url = serializers.SerializerMethodField()

    class Meta:
        model = Video
        fields = ['id', 'title', 'thumbnail_url', 'video_url', 'category']

    def get_thumbnail_url(self, obj):
        if obj.thumbnail:
            return self.context['request'].build_absolute_uri(obj.thumbnail.url)
        return None

    def get_video_url(self, obj):
        return self.context['request'].build_absolute_uri(obj.video_file.url)