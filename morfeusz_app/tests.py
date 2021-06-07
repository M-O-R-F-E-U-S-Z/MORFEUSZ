import os
import sys
from django.conf import settings
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'morfeusz.settings')
settings.configure()
from django.test import TestCase
from models import Group
from django.contrib.auth.models import User

# Create your tests here.

class GroupTest(TestCase):

    def setUp(self):
        self.group1 = Group.objects.create(name='group1')
        self.user1 = User.objects.create_user('user1', 'test@test1.com', 'haslohaslo123')

    def test_add_member(self):
        self.group1.add_member(self.user1)
        self.assertIn(self.user1, self.group1.members.all())

    def test_remove_member(self):
        self.group1.remove_member(self.user1)
        self.assertNotIn(self.user1, self.group1.members.all())
