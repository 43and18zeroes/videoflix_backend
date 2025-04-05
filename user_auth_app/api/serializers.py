from rest_framework import serializers
from user_auth_app.models import CustomUser
from rest_framework import serializers
from dj_rest_auth.serializers import PasswordResetSerializer
from django.contrib.auth.tokens import default_token_generator

import logging
logger = logging.getLogger(__name__)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'email')

    def create(self, validated_data):
        email = validated_data['email']
        user = CustomUser.objects.create(email=email, username=email)
        return user

class EmailConfirmationSerializer(serializers.Serializer):
    token = serializers.UUIDField()
    
class SetPasswordSerializer(serializers.Serializer):
    token = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=128)
    
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    

class CustomPasswordResetSerializer(PasswordResetSerializer):
    def get_email_options(self):
        request = self.context.get('request')
        domain = request.get_host()
        protocol = 'https' if request.is_secure() else 'http'

        user = list(self.reset_form.get_users(self.data["email"]))[0]
        uid = user.pk
        token = default_token_generator.make_token(user)
        password_reset_url = f"{protocol}://{domain}/neuer-pfad-im-frontend/reset-password/{uid}/{token}/"

        return {
            'subject_template_name': 'registration/password_reset_subject.txt',
            'email_template_name': 'registration/password_reset_email.html',
            'html_email_template_name': 'registration/password_reset_email.html',
            'extra_email_context': {  # ← Korrektur hier
                'password_reset_url': password_reset_url,
                'site_name': 'Videoflix',
                'user': user,
                'uid': uid,
                'token': token,
                'protocol': protocol,
                'domain': domain,
            }
        }
