from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_user, name='register'),
    path('confirm-email/', views.confirm_email, name='confirm_email'),
]