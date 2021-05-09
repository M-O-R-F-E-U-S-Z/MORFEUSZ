from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.conf import settings


class FriendList(models.Model):

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="user")
    friends = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name="friends")

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


class FriendRequest(models.Model):
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="sender")
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="receiver")

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
    def decline(self):
        self.is_active = False
        self.save()

    def cancel(self):
        # Different to cancel only through notification
        self.is_active = False
        self.save()


# Create your models here.
# First

# class MyUser(User):
#     friends = models.ManyToManyField(User, blank=True)
#
#
# class FriendRequest(models.Model):
#     from_user = models.ForeignKey(User, related_name='from_user', on_delete=models.CASCADE)
#     to_user = models.ForeignKey(User, related_name='to_user', on_delete=models.CASCADE)

# class Friend(models.Model):
#     users = models.ManyToManyField(User)
#     current_user = models.ForeignKey(User, related_name="owner", null=True, on_delete=models.CASCADE)
#
#     @classmethod
#     def make_friend(cls, current_user, new_friend):
#         friend, created = cls.objects.get_or_create(
#             current_user=current_user
#         )
#         friend.users.add(new_friend)
#
#     @classmethod
#     def remove_friend(cls, current_user, new_friend):
#         friend, created = cls.objects.get_or_create(
#             current_user=current_user
#         )
#         friend.users.remove(new_friend)
#
#     def __str__(self):
#         return str(self.current_user)




