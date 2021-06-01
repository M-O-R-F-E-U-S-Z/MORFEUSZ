from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, FriendRequestForm, UploadBackgroundForm, UploadProfileForm
from django.contrib.auth.models import User
from users.models import FriendRequest, FriendList
from django.http import HttpResponse
from morfeusz_app.models import Movie
from .models import Profile
from django.db.models import Max
import random


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


# def get_random_movie():
#     max_id = Movie.objects.all().aggregate(max_id=Max("id"))['max_id']
#     while True:
#         pk = random.randint(1, max_id)
#         movie = Movie.objects.filter(pk=pk).first()
#         if movie:
#             return movie

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
        background = profile.background_picture
        context['background'] = background
        profile_pic = profile.profile_picture
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
                    return HttpResponse('You are friends with that user')
                elif FriendRequest.objects.filter(sender=receiver, receiver=user):
                    return HttpResponse('This user send you a friend request, accept it instead of sending a new one!')
                else:
                    friend_request, created = FriendRequest.objects.get_or_create(
                        sender=user, receiver=receiver)
                    if created:
                        return HttpResponse('Friend request sent')
                    elif friend_request.is_active:
                        return HttpResponse('Friend request is already sent')
                    else:
                        # friend_request.is_active = True
                        friend_request.delete()
                        FriendRequest.objects.create(sender=user, receiver=receiver)
                        return HttpResponse('Friend request sent again')
            else:
                return HttpResponse('There is no such user')
    else:
        form = FriendRequestForm()
    return render(request, 'users/send_friend_request.html', {'form': form})


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


@login_required
def unfriend(request, friend_id):
    user = request.user
    friend = User.objects.get(id=friend_id)
    friend_list = FriendList.objects.get(user=user)
    if friend in friend_list.friends.all():
        friend_list.unfriend(friend)
        return HttpResponse('Friend deleted')
    else:
        return HttpResponse("It's not your friend")


@login_required
def upload_images(request):
    if request.method == "POST":
        b_form = UploadBackgroundForm(request.POST, request.FILES, instance=request.user.user_profile)
        p_form = UploadProfileForm(request.POST, request.FILES, instance=request.user.user_profile)
        if b_form.is_valid() and p_form.is_valid():
            b_form.save()
            p_form.save()
            return redirect('users:profile')
    else:
        b_form = UploadBackgroundForm(instance=request.user.user_profile)
        p_form = UploadProfileForm(instance=request.user.user_profile)
    context = {'b_form': b_form, "p_form": p_form}
    return render(request, 'users/upload_images.html', context)
