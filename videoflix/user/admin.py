from django.contrib import admin
from .models import CustomUser
from .forms import UserCreationForm
from django.contrib.auth.admin import UserAdmin

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    add_form = UserCreationForm
    fieldsets = (
        *UserAdmin.fieldsets,
        (
             'Additional Info',
            {
                'fields': (
                    'is_verified',
                    'email_verification_token',
                )
            }
        ),
    )
