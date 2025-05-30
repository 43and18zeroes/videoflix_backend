from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status


class VideosTest(APITestCase):

    def test_get_videos(self):
        url = reverse('video-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)