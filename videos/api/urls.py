from django.urls import path
from . import views

urlpatterns = [
    path('videos/', views.VideoListView.as_view(), name='video-list'),
    path('videos/<int:pk>/', views.VideoDetailView.as_view(), name='video-detail'),
    path('videos/<int:pk>/play/', views.play_video, name='play-video'),
]