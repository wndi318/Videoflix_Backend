from django.contrib import admin
from django.urls import path, include
from debug_toolbar.toolbar import debug_toolbar_urls
from user.views import LoginView, LogoutView, RegisterView, VerifyEmailView, PasswordResetRequestView, PasswordResetConfirmView
from content.views import VideoListView, VideoDetailView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('django-rq/', include('django_rq.urls')),
    path('api/verify-email/<str:token>/', VerifyEmailView.as_view(), name='verify_email'),
    path('password-reset/', PasswordResetRequestView.as_view(), name='password_reset'),
    path('reset-password-confirm/<int:user_id>/<str:token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('videos/', VideoListView.as_view(), name='video-list'),
    path('videos/<int:pk>/', VideoDetailView.as_view(), name='video-detail'),
] + debug_toolbar_urls()