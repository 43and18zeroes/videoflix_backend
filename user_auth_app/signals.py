import base64
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import CustomUser
from django.core.mail import send_mail
from django.conf import settings

from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import CustomUser
from django.core.mail import send_mail
from django.conf import settings

@receiver(post_save, sender=CustomUser)
def send_confirmation_email(sender, instance, created, **kwargs):
    if created:
        confirmation_link = f"{settings.FRONTEND_URL}/sign-up/{instance.confirmation_token}"
        # Bild in Base64 codieren
        with open("media/img/brand/videoflix-logo.jpg", "rb") as image_file:
            encoded_image = base64.b64encode(image_file.read()).decode('utf-8')
        html_message = f"""
        <html>
        <head>
          <title>Email Confirmation</title>
        </head>
        <body>
          <h1>Please confirm your email address</h1>
          <img src="data:image/png;base64,{encoded_image}" alt="Beispielbild">
          <p>Click the following link to confirm your email:</p>
          <a href="{confirmation_link}">Confirm Email</a>
          <p>Or copy and paste this link into your browser:</p>
          <p>{confirmation_link}</p>
        </body>
        </html>
        """
        text_message = f"Please click on the following link to confirm your email address: {confirmation_link}"
        send_mail(
            'Email confirmation',
            text_message,
            settings.DEFAULT_FROM_EMAIL,
            [instance.email],
            fail_silently=False,
            html_message=html_message,
        )