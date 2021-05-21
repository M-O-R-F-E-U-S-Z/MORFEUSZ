from django.db import models
from django.contrib.auth.models import User
from imdb import IMDb

ia = IMDb()


class Movie(models.Model):
    # STATUS_CHOICES = [
    #     ('N', 'Do not want to watch'),
    #     ('LN', 'Like and do not want to watch'),
    #     ('LY', 'Like and want to watch'),
    #     ('Y', 'Want to watch')
    # ]
    # users = models.ManyToManyField(User, related_name='movies')
    # user = models.ForeignKey(User,
    # on_delete=models.CASCADE, related_name='movies', null=True)
    movie_imdb_id = models.CharField(max_length=7, default='0000000')
    # status = models.CharField(choices=STATUS_CHOICES,
    #                           default='Y', max_length=255)
    title = models.CharField(default='', max_length=255)

    class Meta:
        ordering = ['movie_imdb_id']

    def set_title(self):
        self.title = ia.get_movie(self.movie_imdb_id)['title']

    def __str__(self):
        # title = ia.get_movie(self.movie_imdb_id)['title']
        return self.title