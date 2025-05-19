# from django.dispatch import receiver
# from django.db.models.signals import post_save
# from .models import Video
# from django.conf import settings
# import os

# from .tasks import convert_to_hls  # ggf. anpassen

# @receiver(post_save, sender=Video)
# def video_post_save(sender, instance, created, **kwargs):
#     if created and instance.video_file:
#         print('Neues Video wurde hochgeladen. Starte HLS-Konvertierung...')
#         source_path = instance.video_file.path
#         print(f"Pfad zur Quelldatei: {source_path}")

#         hls_relative_path = convert_to_hls(source_path)
#         if hls_relative_path:
#             instance.hls_playlist_url = hls_relative_path
#             instance.save()
#             print(f"HLS-Konvertierung abgeschlossen: {hls_relative_path}")
#         else:
#             print("HLS-Konvertierung fehlgeschlagen.")
