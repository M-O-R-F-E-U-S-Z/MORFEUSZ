from django.test import TestCase
from .models import FriendList, FriendRequest
from django.contrib.auth.models import User

# Create your tests here.


class FriendListTest(TestCase):

    def setUp(self):
        self.user1 = User.objects.create_user('user1', 'test@test1.com', 'haslohaslo123')
        self.user2 = User.objects.create_user('user2', 'test@test2.com', 'haslohaslo123')
        self.friend_list1 = FriendList.objects.get(user=self.user1)
        self.friend_list2 = FriendList.objects.get(user=self.user2)

    def test_create_list(self):
        self.assertIsInstance(self.friend_list1, FriendList)

    def test_add_friend(self):
        self.friend_list1.add_friend(self.user2)
        self.assertIn(self.user2, self.friend_list1.friends.all())

    def test_remove_friend(self):
        self.friend_list1.remove_friend(self.user2)
        self.assertNotIn(self.user2, self.friend_list1.friends.all())

    def test_is_mutual_friend(self):
        self.friend_list1.add_friend(self.user2)
        self.friend_list2.add_friend(self.user1)
        self.assertTrue(self.friend_list1.is_mutual_friend(self.user2))
        self.assertTrue(self.friend_list2.is_mutual_friend(self.user1))
        self.friend_list1.remove_friend(self.user2)
        self.assertFalse(self.friend_list1.is_mutual_friend(self.user2))

    def test_unfriend(self):
        self.friend_list1.add_friend(self.user2)
        self.friend_list1.unfriend(self.user2)
        self.assertNotIn(self.user2, self.friend_list1.friends.all())
        self.assertNotIn(self.user1, self.friend_list2.friends.all())


class FriendRequestTest(TestCase):

    def setUp(self):
        self.user1 = User.objects.create_user('user1', 'test@test1.com', 'haslohaslo123')
        self.user2 = User.objects.create_user('user2', 'test@test2.com', 'haslohaslo123')
        self.request1 = FriendRequest.objects.create(sender=self.user1, receiver=self.user2)
        self.request2 = FriendRequest.objects.create(sender=self.user2, receiver=self.user1)
        self.friend_list1 = FriendList.objects.get(user=self.user1)
        self.friend_list2 = FriendList.objects.get(user=self.user2)

    def test_accept(self):
        self.request1.accept()
        self.assertIn(self.user1, self.friend_list2.friends.all())
        self.assertIn(self.user2, self.friend_list1.friends.all())
        self.assertFalse(self.request1.is_active)

    def test_deactivate(self):
        self.request2.deactivate()
        self.assertFalse(self.request2.is_active)