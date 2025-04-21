from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import Video
from .tasks import convert_video

RESOLUTIONS_TO_CONVERT = ["854x480", "1280x720", "1920x1080"]

@receiver(post_save, sender=Video)
def video_post_save(sender, instance, created, **kwargs):
    print('Video saved')
    if created:
        print('New video created')
        source_path = instance.video_file.path
        print(f"Path: {source_path}")
        for resolution in RESOLUTIONS_TO_CONVERT:
            convert_video(source_path, resolution)