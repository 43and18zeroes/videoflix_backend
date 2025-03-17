from rest_framework import serializers
from user_auth_app.models import CustomUser
import uuid
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'email')

    def create(self, validated_data):
        email = validated_data['email']
        username = f"{email.split('@')[0]}-{uuid.uuid4().hex[:6]}" # Eindeutigen Benutzernamen generieren
        user = CustomUser.objects.create(email=email, username=username)
        return user

class EmailConfirmationSerializer(serializers.Serializer):
    token = serializers.UUIDField()