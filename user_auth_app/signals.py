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
  <body style="color: #000;">
    <header style="display: flex; justify-content: center;">
      <img
        src="http://videoflix.cw-coding.de/mail_logo/videoflix-logo.png"
        alt="Videoflix Logo"
      />
    </header>
    <p>
      Thank you for registering with
      <a href="https://videoflix.cw-coding.de" target="_blank">Videoflix</a>. To
      complete your registration and verify your email address, please click the
      link below:
    </p>
    <button href="{confirmation_link}"
      style="font-weight: 700; font-size: 18px; letter-spacing: 0.75px; color: white; background-color: #2e3edf; padding: 12px 24px; border: 0; border-radius: 50px; white-space: nowrap; cursor: pointer;"
    >
      Activate account
    </button>
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
