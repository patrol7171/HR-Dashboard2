from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser, Profile


class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm):
        model = CustomUser
        fields = ('userid', 'password', 'email', 'accesslevel', 'hrgroup', 'is_superuser', 'is_staff', 'is_active')


class CustomUserChangeForm(UserChangeForm):

    class Meta(UserChangeForm):
        model = CustomUser
        fields = ('userid', 'password', 'email', 'accesslevel', 'hrgroup', 'is_superuser', 'is_staff', 'is_active')
 

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']