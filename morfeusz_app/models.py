from django.db import models
from django.contrib.auth.models import User
from imdb import IMDb
#import random
#import string
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' 
import tensorflow as tf
import cv2
import numpy as np
from django.conf import settings

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


# def generate_unique_code():
#     length = 6
#     while True:
#         new_code = ''.join(random.choise(string.ascii_uppercase, k=length))
#         if Group.objects.filter(code=new_code).exists():
#             break
#     return new_code

def cnn(img_path):
    categories = ['Action', 'Comedy', 'Drama', 'Horror', 'Romance']
    img_size = [128, 128]

    X = cv2.imread(img_path)
    X = cv2.resize(X, (img_size[0], img_size[1]))
    X = np.expand_dims(X, axis=0)
    
    pred = settings.ML_MODEL.predict(X)
    weights = dict(zip(categories, pred[0]))

    return weights


class Group(models.Model):

    # code = models.CharField(max_length=8, default="", unique=True)
    name = models.CharField(max_length=30,  default="")
    members = models.ManyToManyField(User, related_name="members")

    #opinion_wages = {
    #    'L': 1,
    #    'DL': -1.5,
    #    'WTS': 1,
    #    'DWTS': -1.5
    #}

    #opinion_hash_table = {
    #    #[wages score, num of rates]
    #    'Action': [0,0],
    #    "Comedy": [0,0],
    #    "Drama": [0,0],
    #    "Horror": [0,0],
    #    "Romance": [0,0],  
    #}


    def __str__(self):
        return self.name


    def add_member(self, account):
        if account not in self.members.all():
            self.members.add(account)


    def remove_member(self, account):
        if account in self.members.all():
            self.members.remove(account)
"""
    def movie_matcher(self):
        for user in self.members:
            self.update_opinion_ht(user, 'L')
            self.update_opinion_ht(user, 'DL')
            self.update_opinion_ht(user, 'WTS')
            self.update_opinion_ht(user, 'DWTS')

        wages = {
            'category': 0.5,
            'score': 0.4, 
            'ML': 0.1
        }

        max_recomendations = 10
        top_recomendations = []

        for movie in movies:

            category_points = 0
            for category in movie[0]:
                category_points += self.opinion_hash_table[category][0] / self.opinion_hash_table[category][1] + 0.5
            category_points /= len(movie[0])

            ML_points = 0
            for user in users:
                for pic in [profile_pic, bg_pic]:
                    ML_points += 0.5 * cnn(pic)

            result = category_points*wages['category'] + movie[1]*wages['score']#\
                    + ML_points*wages['ML']
            
            top_recomendations.sort
            if len(top_recomendations) < max_recomendations:
                top_recomendations.append([result, movie])
            elif result > top_recomendations[0][0]:
                top_recomendations[0] = [result, movie]


    def update_opinion_ht(self, user, opinion):
        for movie in user[opinion]:
            for category in movie[0]:
                    self.opinion_hash_table[category][0] += self.opinion_wages[opinion]
                    self.opinion_hash_table[category][1] += 1
"""
