from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class FriendRequestForm(forms.Form):
    users = User.objects.username()
    USER_LIST = [f"username: {user}" for user in users]
    receiver = forms.CharField(label="To whom do you want send a friend request?")
    pass

