from django.db import models
from django.contrib.auth.models import User
from imdb import IMDb

ia = IMDb()


class Movie(models.Model):
    imdb_id = models.CharField(max_length=7, default='0000000')
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
