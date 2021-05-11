from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm
from django.contrib.auth.models import User
from users.models import FriendRequest
from django.http import HttpResponse
#import json


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
def send_friend_request(request, receiver_id):
    user = request.user
    receiver = User.objects.get(id=receiver_id)
    friend_request, created = FriendRequest.objects.get_or_create(sender=user, receiver=receiver)
    if created:
        return HttpResponse('Friend request sent')
    elif friend_request.is_active:
        return HttpResponse('Friend request already sent')
    else:
        return HttpResponse('Friend request sent')


@login_required
def accept_friend_request(request, request_id):
    friend_request = FriendRequest.objects.get(id=request_id)
    if friend_request.receiver == request.user:
        friend_request.accept()
        return HttpResponse('Friend request accepted')
    else:
        return HttpResponse("You can't accept request that is not sent to you.")


@login_required
def decline_friend_request(request, request_id):
    friend_request = FriendRequest.objects.get(id=request_id)
    if friend_request.receiver == request.user:
        friend_request.deactivate()
        return HttpResponse('Friend request declined')
    else:
        return HttpResponse("You can't decline request that is not sent to you.")


@login_required
def cancel_friend_request(request, request_id):
    friend_request = FriendRequest.objects.get(id=request_id)
    if friend_request.sender == request.user:
        friend_request.deactivate()
        return HttpResponse('Friend request canceled')
    else:
        return HttpResponse("You can't cancel request that is you didn't create.")