import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "videoflix.settings")
django.setup()

from django.contrib.admin.models import LogEntry
from user_auth_app.models import CustomUser

existing_user_ids = CustomUser.objects.values_list('id', flat=True)

invalid_log_entries = LogEntry.objects.exclude(user_id__in=existing_user_ids)

if invalid_log_entries.exists():
    print("Folgende ungültige Log-Einträge wurden gefunden:")
    for entry in invalid_log_entries:
        print(f"ID: {entry.id}, User ID: {entry.user_id}, Content Type: {entry.content_type}, Object ID: {entry.object_id}")

    invalid_log_entries.delete()
    print("Ungültige Log-Einträge wurden gelöscht.")
else:
    print("Keine ungültigen Log-Einträge gefunden.")