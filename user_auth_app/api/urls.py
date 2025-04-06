from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('register/', views.register_user, name='register'),
    path('confirm-email/', views.confirm_email, name='confirm_email'),
    path('set-password/', views.set_password, name='set_password'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('password-reset/', views.CustomPasswordResetView.as_view(), name="password_reset"),
    path('password-reset-confirm/', views.CustomPasswordResetConfirmView.as_view(), name="password_reset_confirm"),
]