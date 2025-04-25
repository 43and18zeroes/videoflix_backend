from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import Video
from .tasks import convert_video

RESOLUTIONS_TO_FIELDS = {
    "854x480": "video_file_480p",
    "1280x720": "video_file_720p",
    "1920x1080": "video_file_1080p",
}

@receiver(post_save, sender=Video)
def video_post_save(sender, instance, created, **kwargs):
    print('Video saved')
    if created:
        print('New video created')
        source_path = instance.video_file.path
        print(f"Path: {source_path}")
        for resolution, field_name in RESOLUTIONS_TO_FIELDS.items():
            relative_path = convert_video(source_path, resolution)
            if relative_path:
                setattr(instance, field_name, relative_path)
        instance.save()