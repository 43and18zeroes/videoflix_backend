from rest_framework import generics
from videos.models import Video
from .serializers import VideoSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.conf import settings

class VideoListView(generics.ListAPIView):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer

class VideoDetailView(generics.RetrieveAPIView):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer
    

@api_view(['GET'])
def get_video_urls(request, pk):
    try:
        video = get_object_or_404(Video, pk=pk)
        video_urls = {}
        if video.video_file:
            video_urls['original'] = request.build_absolute_uri(f'{settings.MEDIA_URL}{video.video_file}')
        if video.video_file_480p:
            video_urls['480p'] = request.build_absolute_uri(f'{settings.MEDIA_URL}{video.video_file_480p}')
        if video.video_file_720p:
            video_urls['720p'] = request.build_absolute_uri(f'{settings.MEDIA_URL}{video.video_file_720p}')
        if video.video_file_1080p:
            video_urls['1080p'] = request.build_absolute_uri(f'{settings.MEDIA_URL}{video.video_file_1080p}')
        return Response(video_urls)
    except Exception as e:
        return Response({'error': f'Error retrieving video URLs: {e}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

@api_view(['GET'])
def play_video(request, pk):
    try:
        video = get_object_or_404(Video, pk=pk)
        if video.hls_playlist_url:
            video_url = request.build_absolute_uri(f'{settings.MEDIA_URL}{video.hls_playlist_url}')
            return Response({'videoUrl': video_url})
        else:
            return Response({'error': 'HLS playlist not available for this video'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': f'Error retrieving video URL: {e}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)