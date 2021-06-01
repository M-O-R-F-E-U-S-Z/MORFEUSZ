from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class FriendRequestForm(forms.Form):
    receiver = forms.CharField(label="To whom do you want send a friend request?")


class UploadBackgroundForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['background_picture']


class UploadProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['profile_picture']