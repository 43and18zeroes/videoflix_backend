from django.db import models

class Video(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(max_length=255)
    upload_date = models.DateTimeField(auto_now_add=True)
    video_file = models.FileField(upload_to='videos/')
    thumbnail = models.ImageField(upload_to='thumbnails/', blank=True, null=True)
    duration = models.PositiveIntegerField(blank=True, null=True, help_text="Dauer in Sekunden")
    views = models.PositiveIntegerField(default=0)

    hls_playlist_url = models.CharField(max_length=255, blank=True, null=True) # Für HLS falls du es später nutzen willst

    video_file_480p = models.CharField(max_length=255, blank=True, null=True)
    video_file_720p = models.CharField(max_length=255, blank=True, null=True)
    video_file_1080p = models.CharField(max_length=255, blank=True, null=True)

    CATEGORY_CHOICES = [
        ('new', 'New on Videoflix'),
        ('documentary', 'Documentary'),
        ('drama', 'Drama'),
        ('romance', 'Romance'),
    ]
    category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES,
        default='new',
    )

    def __str__(self):
        return self.title