from rest_framework import viewsets
from rest_framework.response import Response
from django.db.models import Prefetch
from videos.models import Video
from .serializers import VideoSerializer

class VideoViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = VideoSerializer
    queryset = Video.objects.all().order_by('-upload_date') # Standardmäßige Sortierung nach neuestem zuerst

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True, context={'request': request})
        # Strukturieren Sie die Daten nach Kategorie für die Sections im Frontend
        sections_data = {}
        for video in serializer.data:
            category = video['category']
            if category not in sections_data:
                # Finden Sie den Anzeigenamen der Kategorie
                for choice in Video.CATEGORY_CHOICES:
                    if choice[0] == category:
                        sections_data[category] = {'title': choice[1], 'thumbnails': []}
                        break
            sections_data[category]['thumbnails'].append({
                'thumbnailUrl': video['thumbnail_url'],
                'videoId': str(video['id']),  # Verwenden Sie die ID als Video-ID
                'altText': video['title'],
            })

        # Sortieren Sie die Thumbnails innerhalb jeder Sektion nach dem neuesten Video zuerst
        for category in sections_data:
            sections_data[category]['thumbnails'].sort(key=lambda x: int(x['videoId']), reverse=True)

        # Konvertieren Sie das Dictionary in eine Liste von Sections im gewünschten Format
        sections_list = list(sections_data.values())
        return Response(sections_list)