from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm
from django.contrib.auth.models import User



def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Your account has arleady been created. Try to log in!')
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

# @login_required
# def send_friend_request(request, userID):
#     from_user = request.user
#     to_user = User.objects.get(id=userID)
#     friends_request, created = FriendRequest.objects.get_or_create(from_user = from_user, to_user = to_user)