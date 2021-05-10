from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm
from django.contrib.auth.models import User
from users.models import FriendRequest
from django.http import HttpResponse
import json


def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Your account has already been created. Try to log in!')
            return redirect('morfeusz_app-home')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})


@login_required
def profile(request):
    return render(request, 'users/profile.html')


def login(request):
    return render(request, 'users/login.html')


@login_required
def logout(request):
    return render(request, 'users/logout.html')


@login_required
def send_friend_request(request):
    user = request.user
    payload = {}
    if request.method == "POST" and user.is_authenticated:
        user_id = request.POST.get("receiver_user_id")
        if user_id:
            receiver = User.objects.get(pk=user_id)
            try:
                # get all friend request
                friend_request = FriendRequest.objects.filter(sender=user, receiver=receiver)
                try:
                    for request in friend_request:
                        if request.is_active:
                            raise Exception("You already sent them a friend request.")
                    friend_request = FriendRequest(sender=user, receiver=receiver)
                    friend_request.save()
                    payload['response'] = "Friend request sent."
                except Exception as e:
                    payload['response'] = str(e)
            except FriendRequest.DoesNotExist:
                friend_request = FriendRequest(sender=user, receiver=receiver)
                friend_request.save()

                if payload['response'] is None:
                    payload['response'] = "Something went wrong"
        else:
            payload['response'] = "Unable to send a friend request."
    else:
        payload['response'] = "You are not authenticated"
    return HttpResponse(json.dumps(payload), content_type="application/")


