from django.db import models
from django.contrib.auth.models import User
from imdb import IMDb
#import random
#import string
import os
#os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' 
#import tensorflow as tf
#import cv2
import numpy as np
from django.conf import settings

ia = IMDb()


class Movie(models.Model):
    imdb_id = models.CharField(max_length=8, default='0000000')
    title = models.CharField(default='', max_length=255)
    genre = models.CharField(default='', max_length=255)
    cover_url = models.CharField(default='', max_length=255)
    rating = models.CharField(default='', max_length=255)

    class Meta:
        ordering = ['imdb_id']

    def set_title(self):
        self.title = ia.get_movie(self.imdb_id)['title']

    def set_genre(self):
        self.genre = ia.get_movie(self.imdb_id)['genres']

    def set_cover_url(self):
        self.cover_url = ia.get_movie(self.imdb_id)['cover url']
        
    def set_rating(self):
        self.rating = ia.get_movie(self.imdb_id)['rating']

    def __str__(self):
        return self.title


# def generate_unique_code():
#     length = 6
#     while True:
#         new_code = ''.join(random.choise(string.ascii_uppercase, k=length))
#         if Group.objects.filter(code=new_code).exists():
#             break
#     return new_code
'''
def cnn(img_path):
    categories = ['Action', 'Comedy', 'Drama', 'Horror', 'Romance']
    img_size = [128, 128]

    X = cv2.imread(img_path)
    X = cv2.resize(X, (img_size[0], img_size[1]))
    X = np.expand_dims(X, axis=0)
    
    #pred = settings.ML_MODEL.predict(X)
    weights = dict(zip(categories, pred[0]))

    return weights
'''

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


