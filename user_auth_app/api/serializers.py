from rest_framework import serializers
from user_auth_app.models import CustomUser
from rest_framework import serializers
import uuid
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