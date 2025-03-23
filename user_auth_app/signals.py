from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import CustomUser
from django.core.mail import send_mail
from django.conf import settings

@receiver(post_save, sender=CustomUser)
def send_confirmation_email(sender, instance, created, **kwargs):
    if created:  # Nur ausführen, wenn ein neuer Benutzer erstellt wurde
        confirmation_link = f"{settings.FRONTEND_URL}/sign-up/{instance.confirmation_token}"
        send_mail(
            'Email confirmation',
            f'Please click on the following link to confirm your e-mail address: {confirmation_link}',
            settings.DEFAULT_FROM_EMAIL,
            [instance.email],
            fail_silently=False,
        )