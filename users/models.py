from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    user_profile = models.OneToOneField(User, on_delete=models.CASCADE, related_name="user_profile")
    profile_picture = models.ImageField(upload_to='profile_pictures/')
    background_picture = models.ImageField(upload_to='background_pictures/')

    # films_dont_like = models.ManyToManyField(Film, on_delete=models.CASCADE)
    # films_like_dont_watch = models.ManyToManyField(Film, on_delete=models.CASCADE)
    # films_like_watch = models.ManyToManyField(Film, on_delete=models.CASCADE)
    # films_watch = models.ManyToManyField(Film, on_delete=models.CASCADE)

    def __str__(self):
        return self.user_profile.username


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
        Profile.objects.create(user=instance)


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







