from django.db import models
from django.contrib.auth.models import User
from imdb import IMDb
import random
import string

ia = IMDb()


class Movie(models.Model):
    imdb_id = models.CharField(max_length=8, default='0000000')
    title = models.CharField(default='', max_length=255)
    genre = models.CharField(default='', max_length=255)
    cover_url = models.CharField(default='', max_length=255)

    class Meta:
        ordering = ['imdb_id']

    def set_title(self):
        self.title = ia.get_movie(self.imdb_id)['title']

    def set_genre(self):
        self.genre = ia.get_movie(self.imdb_id)['genres'][0]

    def set_cover_url(self):
        self.cover_url = ia.get_movie(self.imdb_id)['cover url']

    def __str__(self):
        return self.title


# def generate_unique_code():
#     length = 6
#     while True:
#         new_code = ''.join(random.choise(string.ascii_uppercase, k=length))
#         if Group.objects.filter(code=new_code).exists():
#             break
#     return new_code


class Group(models.Model):

    # code = models.CharField(max_length=8, default="", unique=True)
    name = models.CharField(max_length=30,  default="")
    members = models.ManyToManyField(User, related_name="members")

    def __str__(self):
        return self.name

    def add_member(self, account):
        if account not in self.members.all():
            self.members.add(account)

    def remove_member(self, account):
        if account in self.members.all():
            self.members.remove(account)


