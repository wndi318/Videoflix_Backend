"""
URL configuration for videoflix project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
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
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT) + debug_toolbar_urls()
