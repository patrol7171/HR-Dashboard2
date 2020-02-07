from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser, Profile


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ['userid', 'password', 'email', 'accesslevel', 'hrgroup', 'is_superuser', 'is_staff', 'is_active', ]


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Profile)