from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from user_auth_app.models import CustomUser
import uuid


class UserAuthTests(APITestCase):
    def setUp(self):
        self.email = 'test@example.com'
        self.password = 'securepassword123'
        self.user = CustomUser.objects.create(
            email=self.email,
            username=self.email,
            email_confirmed=False
        )
        self.token = str(self.user.confirmation_token)

    def test_register_user(self):
        url = reverse('register')
        data = {'email': 'newuser@example.com'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(CustomUser.objects.filter(email='newuser@example.com').exists())

    def test_confirm_email_valid_token(self):
        url = reverse('confirm_email')
        data = {'token': self.token}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertTrue(self.user.email_confirmed)

    def test_confirm_email_invalid_token(self):
        url = reverse('confirm_email')
        data = {'token': uuid.uuid4()}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_set_password_valid_token(self):
        url = reverse('set_password')
        data = {'token': self.token, 'password': self.password}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password(self.password))

    def test_set_password_invalid_token(self):
        url = reverse('set_password')
        data = {
            'token': str(uuid.uuid4()),  # ✅ gültiger, aber nicht existierender Token
            'password': 'test123'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 404)

    def test_login_with_valid_credentials(self):
        # set password first
        self.user.set_password(self.password)
        self.user.save()

        url = reverse('login')
        data = {'email': self.email, 'password': self.password}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_login_with_invalid_credentials(self):
        url = reverse('login')
        data = {'email': self.email, 'password': 'wrong'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
