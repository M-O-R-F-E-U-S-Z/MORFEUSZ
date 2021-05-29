from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from morfeusz_app.models import Movie
from django.conf import settings
import random
import string


class Profile(models.Model):
    user_profile = models.OneToOneField(User, on_delete=models.CASCADE, related_name="user_profile")
    movies_dont_like = models.ManyToManyField(Movie, related_name="linked_profiles_dont_like")
    movies_like_dont_watch = models.ManyToManyField(
        Movie, related_name="linked_profiles_like_dont_watch")
    movies_like_watch = models.ManyToManyField(Movie, related_name="linked_profiles_like_watch")
    movies_watch = models.ManyToManyField(Movie, related_name="linked_profiles_watch")

    def all_movies_pk(self):
        movies_pk = []
        for mv in self.movies_dont_like.all():
            movies_pk.append(mv.pk)
        for mv in self.movies_like_dont_watch.all():
            movies_pk.append(mv.pk)
        for mv in self.movies_like_watch.all():
            movies_pk.append(mv.pk)
        for mv in self.movies_watch.all():
            movies_pk.append(mv.pk)
        return movies_pk

    profile_picture = models.ImageField(upload_to='profile_pictures/', default='profile_pictures/default_profile.jpg')
    background_picture = models.ImageField(upload_to='background_pictures/', default='background_pictures/default_background.jpg')


class FriendList(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="user")
    friends = models.ManyToManyField(User, blank=True, related_name="friends")

    def __str__(self):
        return self.user.username

    def add_friend(self, account):
        if account not in self.friends.all():
            self.friends.add(account)

    def remove_friend(self, account):
        if account in self.friends.all():
            self.friends.remove(account)

    def unfriend(self, removee):
        remover_friends_list = self

        # Remove friend from remover friend list
        remover_friends_list.remove_friend(removee)

        # Remove friend from removee friend list
        friends_list = FriendList.objects.get(user=removee)
        friends_list.remove_friend(self.user)

    def is_mutual_friend(self, friend):
        if friend in self.friends.all():
            return True
        return False


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        FriendList.objects.create(user=instance)


class FriendRequest(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sender")
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="receiver")

    is_active = models.BooleanField(blank=True, null=False, default=True)

    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.sender.username

    def accept(self):
        receiver_friend_list = FriendList.objects.get(user=self.receiver)
        if receiver_friend_list:
            receiver_friend_list.add_friend(self.sender)
            sender_friend_list = FriendList.objects.get(user=self.sender)
            if sender_friend_list:
                sender_friend_list.add_friend(self.receiver)
                self.is_active = False
                self.save()

    def deactivate(self):
        self.is_active = False
        self.save()


def generate_unique_code():
    length = 6
    while True:
        new_code = ''.join(random.choises(string.ascii_uppercase, k=length))
        if Group.objects.filter(code=new_code).exists():
            break
    return new_code


class Group(models.Model):

    code = models.CharField(max_length=8, default="", unique=True)
    name = models.CharField(max_length=30,  default="")
    members = models.ManyToManyField(User, related_name="members")

    def __str__(self):
        return self.members.username

    def add_member(self, account):
        if account not in self.members.all():
            self.members.add(account)

    def remove_member(self, account):
        if account in self.members.all():
            self.members.remove(account)
