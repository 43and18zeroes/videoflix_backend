from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from videos.models import Video
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import override_settings


class VideoAPITests(APITestCase):
    def setUp(self):
        self.video = Video.objects.create(
            title="Test Video",
            description="A test video.",
            video_file=SimpleUploadedFile("video.mp4", b"dummycontent", content_type="video/mp4"),
            views=5,
            hls_playlist_url="videos/hls/1/playlist.m3u8",
            video_file_480p="videos/hls/1/480p.m3u8",
            video_file_720p="videos/hls/1/720p.m3u8",
            video_file_1080p="videos/hls/1/1080p.m3u8",
        )

    def test_video_list(self):
        url = reverse('video-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['title'], self.video.title)

    def test_video_detail(self):
        url = reverse('video-detail', args=[self.video.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.video.pk)

    def test_video_urls(self):
        url = reverse('video-urls', args=[self.video.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('720p', response.data)

    def test_video_urls_not_found(self):
        url = reverse('video-urls', args=[9999])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_play_video(self):
        url = reverse('video-play', args=[self.video.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('videoUrl', response.data)

    def test_play_video_without_hls(self):
        self.video.hls_playlist_url = None
        self.video.save()
        url = reverse('video-play', args=[self.video.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    @override_settings(FFMPEG_ENABLED=False)
    def test_video_upload(self):
        url = reverse('video-upload')
        video_file = SimpleUploadedFile("upload.mp4", b"dummycontent", content_type="video/mp4")
        data = {
            'title': 'Test Upload',
            'description': 'Nur ein Test',
            'video_file': video_file,
        }
        response = self.client.post(url, data, format='multipart')
        self.assertEqual(response.status_code, 201)

    def test_video_upload_missing_file(self):
        url = reverse('video-upload')
        data = {'title': 'Missing file'}
        response = self.client.post(url, data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('video_file', response.data)
