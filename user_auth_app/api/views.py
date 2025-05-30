from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import UserSerializer, EmailConfirmationSerializer, SetPasswordSerializer, LoginSerializer, CustomPasswordResetSerializer, CustomPasswordResetConfirmSerializer
from user_auth_app.models import CustomUser
from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from dj_rest_auth.views import PasswordResetView
HTTP_422_UNPROCESSABLE_ENTITY = 422

@api_view(['POST'])
def register_user(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def confirm_email(request):
    serializer = EmailConfirmationSerializer(data=request.data)
    if serializer.is_valid():
        try:
            token = serializer.validated_data['token']
            user = CustomUser.objects.get(confirmation_token=token)
        except CustomUser.DoesNotExist:
            return Response({'error': 'Invalid confirmation token'}, status=status.HTTP_404_NOT_FOUND)

        user.email_confirmed = True
        user.save()
        return Response({'message': 'Email confirmed'}, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def set_password(request):
    serializer = SetPasswordSerializer(data=request.data)
    if serializer.is_valid():
        try:
            token = serializer.validated_data['token']
            password = serializer.validated_data['password']
            user = CustomUser.objects.get(confirmation_token=token)
        except CustomUser.DoesNotExist:
            return Response({'error': 'Invalid confirmation token'}, status=status.HTTP_404_NOT_FOUND)

        user.password = make_password(password)
        user.save()
        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)


class LoginView(APIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        print(serializer)
        print(serializer.validated_data['email'])
        user = authenticate(
            request,
            username=serializer.validated_data['email'],
            password=serializer.validated_data['password']
        )
        print(user)

        if user is not None:
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        


class CustomPasswordResetView(PasswordResetView):
    serializer_class = CustomPasswordResetSerializer
    

class CustomPasswordResetConfirmView(APIView):
    serializer_class = CustomPasswordResetConfirmSerializer
    permission_classes = []

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({'detail': 'Password reset successfully.'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=HTTP_422_UNPROCESSABLE_ENTITY)