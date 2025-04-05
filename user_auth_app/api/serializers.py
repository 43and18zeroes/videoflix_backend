from rest_framework import serializers
from user_auth_app.models import CustomUser
from rest_framework import serializers
from dj_rest_auth.serializers import PasswordResetSerializer
from django.contrib.auth.tokens import default_token_generator

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
        site = request.site
        domain = site.domain
        protocol = 'https' if request.is_secure() else 'http'
        uid = self.user.pk
        token = default_token_generator.make_token(self.user)
        password_reset_url = f"{protocol}://{domain}/neuer-pfad-im-frontend/reset-password/{uid}/{token}/"  # Passe den Pfad an dein Frontend an

        return {
            'subject_template_name': 'registration/password_reset_subject.txt',  # Optional: Betreff-Template
            'email_template_name': 'registration/password_reset_email.html',
            'html_email_template_name': 'registration/password_reset_email.html', # Für HTML-Mails
            'context': {
                'password_reset_url': password_reset_url,
                'site_name': site.name,
                'user': self.user,
                'uid': uid,
                'token': token,
                'protocol': protocol,
                'domain': domain,
            }
        }