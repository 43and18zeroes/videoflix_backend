from rest_framework import serializers
from user_auth_app.models import CustomUser
from rest_framework import serializers
from dj_rest_auth.serializers import PasswordResetSerializer
from django.contrib.auth.tokens import default_token_generator
from django.conf import settings
import logging
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth import get_user_model
User = get_user_model()
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
        domain = settings.FRONTEND_URL.split('://')[1] if '://' in settings.FRONTEND_URL else settings.FRONTEND_URL
        protocol = 'https' if request.is_secure() else 'http'

        user = list(self.reset_form.get_users(self.data["email"]))[0]
        uid = user.pk
        token = default_token_generator.make_token(user)
        password_reset_url = f"{protocol}://{domain}/password-reset/{uid}/{token}/"

        return {
            'subject_template_name': 'registration/password_reset_subject.txt',
            'email_template_name': 'registration/password_reset_email.html',
            'html_email_template_name': 'registration/password_reset_email.html',
            'extra_email_context': {
                'password_reset_url': password_reset_url,
                'site_name': 'Videoflix',
                'user': user,
                'uid': uid,
                'token': token,
                'protocol': protocol,
                'domain': domain,
            }
        }


class CustomPasswordResetConfirmSerializer(serializers.Serializer):
    uid = serializers.CharField(write_only=True)
    token = serializers.CharField(write_only=True)
    new_password1 = serializers.CharField(write_only=True, style={'input_type': 'password'})
    new_password2 = serializers.CharField(write_only=True, style={'input_type': 'password'})

    def validate(self, attrs):
        uid = attrs.get('uid')
        token = attrs.get('token')
        new_password1 = attrs.get('new_password1')
        new_password2 = attrs.get('new_password2')

        if new_password1 != new_password2:
            raise serializers.ValidationError({"new_password2": ["The two password fields didn't match."]})

        try:
            user_pk = int(uid)
            self.user = User.objects.get(pk=user_pk)
        except (ValueError, User.DoesNotExist):
            raise serializers.ValidationError({"uid": ["User not found"]})

        if not default_token_generator.check_token(self.user, token):
            raise serializers.ValidationError({"token": ["Invalid or expired token"]})

        attrs['user'] = self.user
        return attrs

    def save(self):
        user = self.validated_data['user']
        new_password = self.validated_data['new_password1']
        user.set_password(new_password)
        user.save()
        return user