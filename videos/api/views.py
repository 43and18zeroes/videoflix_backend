from rest_framework import generics
from videos.models import Video
from .serializers import VideoSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from .serializers import VideoUploadSerializer
from django.http import Http404
import logging
from rest_framework.exceptions import NotFound
logger = logging.getLogger(__name__)

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
        return Response(video_urls, status=status.HTTP_200_OK)
    except Http404:
        return Response({'error': 'Video not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        logger.exception("Unexpected error in get_video_urls")
        return Response({'error': 'Unexpected error retrieving video URLs'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

@api_view(['GET'])
def play_video(request, pk):
    try:
        video = get_object_or_404(Video, pk=pk)
        if not video.hls_playlist_url:
            return Response({'error': 'HLS playlist not available for this video'}, status=status.HTTP_404_NOT_FOUND)

        normalized_path = video.hls_playlist_url.replace('\\', '/')
        video_url = request.build_absolute_uri(f'{settings.MEDIA_URL}{normalized_path}')
        return Response({'videoUrl': video_url}, status=status.HTTP_200_OK)

    except Video.DoesNotExist:
        raise NotFound("Video not found")
    except Exception as e:
        logger.exception("Unexpected error in play_video")
        return Response({'error': 'Unexpected error retrieving video URL'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
          

class VideoUploadView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        logger.info(f"VideoUploadView post start")
        serializer = VideoUploadSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)