from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UpdateMLPoints, UserRegisterForm, FriendRequestForm, UploadBackgroundForm, UploadProfileForm
from django.contrib.auth.models import User
from users.models import FriendRequest, FriendList
from django.http import HttpResponse
from morfeusz_app.models import Movie
from .models import Profile
from django.db.models import Max
import random
import cv2
import numpy as np
from django.conf import settings
import tensorflow as tf
import urllib

def cnn(img):
    genres = ['Action', 'Comedy', 'Drama', 'Horror', 'Romance']
    img_size = [128, 128]
    ML_model = tf.keras.models.load_model(settings.MODEL_PATH)
    req = urllib.request.urlopen(img)
    arr = np.asarray(bytearray(req.read()), dtype=np.uint8)
    X = cv2.imdecode(arr, -1)
    X = cv2.resize(X, (img_size[0], img_size[1]))
    X = np.expand_dims(X, axis=0)
    pred = ML_model.predict(X)
    weights = dict(zip(genres, pred[0]))
    return weights



def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            user = User.objects.filter(username=username).first()
            profile = Profile(user_profile=user)
            profile.save()
            messages.success(request, f'Your account has been created. Try to log in!')
            return redirect('morfeusz_app-home')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})

@login_required
def movie_qualification(request):
    user = request.user
    movies_pk = [mv.pk for mv in Movie.objects.all()]
    user_movies_pk = user.user_profile.all_movies_pk()
    movies_pk = list(set(movies_pk)-set(user_movies_pk))
    if not movies_pk == []:
        movie_pk = random.choice(movies_pk)
        movie = Movie.objects.filter(pk=movie_pk).first()
        request.session['movie_pk'] = movie_pk
        context = {'movie': movie}
        return render(request, 'users/movie_qualification.html', context)
    else:
        return HttpResponse("No more movies to qualification.")

@login_required
def movies_dont_like(request):
    user = request.user
    movie_pk = request.session.get('movie_pk', None)
    movie = Movie.objects.filter(pk=movie_pk).first()
    profile = user.user_profile
    profile.movies_dont_like.add(movie)
    profile.save()
    return redirect('users:movie_qualification')

@login_required
def movies_like_dont_watch(request):
    user = request.user
    movie_pk = request.session.get('movie_pk', None)
    movie = Movie.objects.filter(pk=movie_pk).first()
    profile = user.user_profile
    profile.movies_like_dont_watch.add(movie)
    profile.save()
    return redirect('users:movie_qualification')

@login_required
def movies_like_watch(request):
    user = request.user
    movie_pk = request.session.get('movie_pk', None)
    movie = Movie.objects.filter(pk=movie_pk).first()
    profile = user.user_profile
    profile.movies_like_watch.add(movie)
    profile.save()
    return redirect('users:movie_qualification')


@login_required
def movies_watch(request):
    user = request.user
    movie_pk = request.session.get('movie_pk', None)
    movie = Movie.objects.filter(pk=movie_pk).first()
    profile = user.user_profile
    profile.movies_watch.add(movie)
    profile.save()
    return redirect('users:movie_qualification')

@login_required
def profile(request):
    context = {}
    friend_requests = FriendRequest.objects.all()
    request_to = []
    request_from = []
    user = request.user
    friends_list = FriendList.objects.all()
    friend_list = None
    for friend in friends_list:
        if friend.user == user:
            friend_list = friend

    for fr_req in friend_requests:
        if fr_req.sender == user and fr_req.is_active:
            request_to.append(fr_req)
        elif fr_req.receiver == user and fr_req.is_active:
            request_from.append(fr_req)
    context['request_to'] = request_to
    context['request_from'] = request_from
    context['friend_list'] = friend_list
    if Profile.objects.filter(user_profile=user).exists():
        profile = user.user_profile
        background = profile.background_picture.url
        context['background'] = background
        profile_pic = profile.profile_picture.url
        context['profile_pic'] = profile_pic
    return render(request, 'users/profile.html', context)

def login(request):
    return render(request, 'users/login.html')

@login_required
def logout(request):
    return render(request, 'users/logout.html')

@login_required
def send_friend_request(request):
    user = request.user
    if request.method == "POST":
        form = FriendRequestForm(request.POST)
        if form.is_valid():
            receiver_username = form.cleaned_data.get("receiver")
            if User.objects.filter(username=receiver_username).exists():
                receiver = User.objects.get(username=receiver_username)
                if FriendList.objects.get(user=user).is_mutual_friend(receiver):
                    messages.info(request, f'You are friends with that user')
                    return redirect('users:profile')
                else:
                    friend_request, created = FriendRequest.objects.get_or_create(
                        sender=user, receiver=receiver)
                    if created:
                        messages.success(request, f'Friend request sent')
                        return redirect('users:profile')
                    elif friend_request.is_active:
                        messages.info(request, f'Friend request is already sent')
                        return redirect('users:profile')
                    else:
                        friend_request.delete()
                        FriendRequest.objects.create(sender=user, receiver=receiver)
                        messages.success(request, f'Friend request sent again')
                        return redirect('users:profile')
            else:
                messages.info(request, f'There is no such user')
                return redirect('users:profile')
    else:
        form = FriendRequestForm()
    return render(request, 'users/send_friend_request.html', {'form': form})

@login_required
def accept_friend_request(request, request_id):
    friend_request = FriendRequest.objects.get(id=request_id)
    if friend_request.receiver == request.user:
        friend_request.accept()
        if FriendRequest.objects.filter(sender=friend_request.receiver, receiver=friend_request.sender):
            mutual_request = FriendRequest.objects.get(sender=friend_request.receiver, receiver=friend_request.sender)
            mutual_request.deactivate()
        messages.success(request, f'Friend request accepted')
        return redirect('users:profile')
    else:
        messages.info(request, f"You can't accept request that is not sent to you.")
        return redirect('users:profile')

@login_required
def decline_friend_request(request, request_id):
    friend_request = FriendRequest.objects.get(id=request_id)
    if friend_request.receiver == request.user:
        friend_request.deactivate()
        messages.success(request, f'Friend request declined')
        return redirect('users:profile')
    else:
        messages.info(request, f"You can't decline request that is not sent to you.")
        return redirect('users:profile')

@login_required
def cancel_friend_request(request, request_id):
    friend_request = FriendRequest.objects.get(id=request_id)
    if friend_request.sender == request.user:
        friend_request.deactivate()
        messages.success(request, f'Friend request canceled')
        return redirect('users:profile')
    else:
        messages.info(request, f"You can't cancel request that is not sent to you.")
        return redirect('users:profile')

@login_required
def unfriend(request, friend_id):
    user = request.user
    friend = User.objects.get(id=friend_id)
    friend_list = FriendList.objects.get(user=user)
    if friend in friend_list.friends.all():
        friend_list.unfriend(friend)
        messages.success(request, f'Friend deleted')
        return redirect('users:profile')
    else:
        messages.info(request, f"It's not your friend")
        return redirect('users:profile')

@login_required
def upload_images(request):
    if request.method == "POST":
        user = request.user
        p_form = UploadProfileForm(request.POST, request.FILES, instance=user.user_profile)
        if  p_form.is_valid():
            p_form.save()
            user.ML_points = cnn(user.user_profile)
            return redirect('users:profile')
    else:
        p_form = UploadProfileForm(instance=request.user.user_profile)
    context = {"p_form": p_form}
    return render(request, 'users/upload_images.html', context)
