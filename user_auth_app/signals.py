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
        confirmation_link = (
            f"{settings.FRONTEND_URL}/sign-up/{instance.confirmation_token}"
        )
        html_message = f"""
        <html>
  <head>
    <title>Confirm your email</title>
  </head>
  <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333333; background-color: #ffffff; padding: 20px;">
    <img
      src="http://videoflix.cw-coding.de/mail_logo/videoflix-logo.png"
      alt="Videoflix Logo"
      style="max-width: 200px; height: auto; margin-bottom: 20px;"
    />

    <p>
      Thank you for registering with
      <a href="https://videoflix.cw-coding.de" target="_blank" style="color: #1a73e8; text-decoration: none;">Videoflix</a>. To
      complete your registration and verify your email address, please click the
      link below:
    </p>

    <a
      href="{confirmation_link}"
      style="
        display: inline-block;
        padding: 12px 20px;
        background-color: #1a73e8;
        color: white;
        text-decoration: none;
        border-radius: 4px;
        font-weight: bold;
        margin: 20px 0;
      "
    >
      Activate account
    </a>

    <p>
      If you did not create an account with us, please disregard this email.
    </p>
    <p>Best regards,</p>
    <p>Your Videoflix Team.</p>
  </body>
</html>
        """
        text_message = f"Please click on the following link to confirm your email address: {confirmation_link}"
        send_mail(
            "Email confirmation",
            text_message,
            settings.DEFAULT_FROM_EMAIL,
            [instance.email],
            fail_silently=False,
            html_message=html_message,
        )
