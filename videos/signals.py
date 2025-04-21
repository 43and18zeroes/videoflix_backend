from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
from .models import Video
from .tasks import convert_480p


@receiver(post_save, sender=Video)
def video_post_save(sender, instance, created, **kwargs):
    print('Video saved')
    if created:
        print('New video created')
        source_path = instance.video_file.path
        print(f"Quellpfad: {source_path}")  # Testausgabe
        convert_480p(source_path)