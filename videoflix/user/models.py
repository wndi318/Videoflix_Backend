from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
import secrets

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Der Benutzer muss eine E-Mail-Adresse haben.')
        email = self.normalize_email(email)
        extra_fields['username'] = email
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    is_verified = models.BooleanField(default=False)
    email_verification_token = models.CharField(max_length=50, blank=True, null=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    objects = CustomUserManager()
    
    def save(self, *args, **kwargs):
        if not self.pk and not self.email_verification_token:
            self.email_verification_token = self.generate_verification_token()
        super().save(*args, **kwargs)

    def generate_verification_token(self):
        token = secrets.token_urlsafe(20)
        return token
    
    def __str__(self):
        return self.email