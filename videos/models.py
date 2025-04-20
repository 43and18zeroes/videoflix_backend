from django.db import models

class Video(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(max_length=255)
    upload_date = models.DateTimeField(auto_now_add=True)
    video_file = models.FileField(upload_to='videos/')
    thumbnail = models.ImageField(upload_to='thumbnails/', blank=True, null=True)
    duration = models.PositiveIntegerField(blank=True, null=True, help_text="Dauer in Sekunden")
    views = models.PositiveIntegerField(default=0)
    
    CATEGORY_CHOICES = [
        ('new', 'New on Videoflix'),
        ('documentary', 'Documentary'),
        ('drama', 'Drama'),
        ('romance', 'Romance'),
    ]
    category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES,
        default='new',  # Optional: Standardkategorie
    )

    def __str__(self):
        return self.title