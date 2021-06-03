from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from django.conf import settings

app_name = 'users'
urlpatterns = [
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('login/', auth_views.LoginView.as_view(
        template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(
        template_name='users/logout.html'), name='logout'),
    path('send_friend_request/', views.send_friend_request, name='send_friend_request'),
    path('accept_friend_request/<int:request_id>/',
         views.accept_friend_request, name='accept_friend_request'),
    path('decline_friend_request/<int:request_id>/',
         views.decline_friend_request, name='decline_friend_request'),
    path('cancel_friend_request/<int:request_id>/',
         views.cancel_friend_request, name='cancel_friend_request'),
    path('unfriend/<int:friend_id>/', views.unfriend, name='unfriend'),
    path('movie_qualification/', views.movie_qualification, name='movie_qualification'),
    path('movies_dont_like/', views.movies_dont_like, name='movies_dont_like'),
    path('movies_like_dont_watch/', views.movies_like_dont_watch, name='movies_like_dont_watch'),
    path('movies_like_watch/', views.movies_like_watch, name='movies_like_watch'),
    path('movies_watch/', views.movies_watch, name='movies_watch'),
    path('upload_images/', views.upload_images, name='upload_images')
]
# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)