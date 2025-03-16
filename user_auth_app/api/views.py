from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import UserSerializer, EmailConfirmationSerializer
from user_auth_app.models import CustomUser
from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import get_object_or_404

@api_view(['POST'])
def register_user(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        confirmation_link = f"{settings.FRONTEND_URL}/confirm-email/{user.confirmation_token}"
        send_mail(
            'E-Mail-Bestätigung',
            f'Bitte klicke auf den folgenden Link, um deine E-Mail-Adresse zu bestätigen: {confirmation_link}',
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=False,
        )
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def confirm_email(request):
    serializer = EmailConfirmationSerializer(data=request.data)
    if serializer.is_valid():
        token = serializer.validated_data['token']
        user = get_object_or_404(CustomUser, confirmation_token=token)
        user.email_confirmed = True
        user.save()
        return Response({'message': 'E-Mail bestätigt'}, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)