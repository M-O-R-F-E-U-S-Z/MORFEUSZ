#from users.views import movies_dont_like, movies_like_dont_watch, movies_like_watch, movies_watch
from django.db import models
from django.contrib.auth.models import User
from imdb import IMDb
#import random
#import string
import os
import urllib
from numpy.lib.function_base import append
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' 
import cv2
import numpy as np
from django.conf import settings
import json

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
        self.genre = json.dumps(ia.get_movie(self.imdb_id)['genres'])

    def set_cover_url(self):
        self.cover_url = ia.get_movie(self.imdb_id)['cover url']
        
    def set_rating(self):
        self.rating = ia.get_movie(self.imdb_id)['rating']
    
    def get_genre(self):
        return json.loads(self.genre)

    def __str__(self):
        return self.title


# def generate_unique_code():
#     length = 6
#     while True:
#         new_code = ''.join(random.choise(string.ascii_uppercase, k=length))
#         if Group.objects.filter(code=new_code).exists():
#             break
#     return new_code

def cnn(img):
    genres = ['Action', 'Comedy', 'Drama', 'Horror', 'Romance']
    img_size = [128, 128]
    #X = np.asarray(bytearray(img.read()), dtype="uint8")
    #X = cv2.imdecode(X, cv2.IMREAD_COLOR)
    #X = cv2.imread(img)
    req = urllib.request.urlopen(img)
    arr = np.asarray(bytearray(req.read()), dtype=np.uint8)
    X = cv2.imdecode(arr, -1)
    X = cv2.resize(X, (img_size[0], img_size[1]))
    X = np.expand_dims(X, axis=0)
    dupa
    pred = settings.ML_MODEL.predict(X)
    weights = dict(zip(genres, pred[0]))

    return weights

################################
from users.models import Profile
################################

class Group(models.Model):
    
    INIT_GENRE_RATING = 0.5
    OPINION_WAGES = {
            'L': 1,
            'DL': -1,
            'WTW': 1,
            'DWTW': -1
        }
    FINAL_WAGES = {
            'genre': 0.6,
            'rating': 0.3, 
            'ML': 0.1
        }
    MAX_RECOMENDATIONS = 10

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

    def movie_matcher(self):
        users_opinion = []
        users = []
        users_ML = []
        for member in self.members.all():
            user = Profile.objects.get(user_profile=member)
            users.append(user)
            users_ML.append(cnn(user.profile_picture.url))
            users_opinion.append(  {'L': list(user.movies_like_watch.all()),
                                    'DL': list(user.movies_dont_like.all()),
                                    'WTW': list(user.movies_like_dont_watch.all()),
                                    'DWTW': list(user.movies_watch.all())} )


        genres = {'Action': [0,0,self.INIT_GENRE_RATING], 'Comedy': [0,0,self.INIT_GENRE_RATING],
                  'Drama': [0,0,self.INIT_GENRE_RATING], 'Horror': [0,0,self.INIT_GENRE_RATING],
                  'Romance': [0,0,self.INIT_GENRE_RATING]} #{'GENRE': [sum of wages score(A), num of ratings(B), A/B] 
        
        for user in users_opinion:
            for key, value in user.items():
                for movie in value:
                    for genre in movie.get_genre():
                        if genre in genres:
                                genres[genre][0] += self.OPINION_WAGES[key]
                                genres[genre][1] += 1
                        else:
                                genres[genre] = [self.OPINION_WAGES[key], 1, self.INIT_GENRE_RATING]
            for genre in genres:
                if genres[genre][1] > 0:
                    genres[genre][2] += genres[genre][0] / genres[genre][1]
                genres[genre][0] = 0
                genres[genre][1] = 0
        
        for genre in genres:
            genres[genre][2] /= len(users)
            if genres[genre][2] > 1:
                genres[genre][2] = 1
            elif genres[genre][2] < 0:
                genres[genre][2] = 0
        
        top_recomendations = []

        for movie in Movie.objects.all():

            genre_points = 0
            for genre in movie.get_genre():
                if genre in genres:
                    genre_points += genres[genre][2]
                else:
                    genre_points += self.INIT_GENRE_RATING
            genre_points /= len(movie.get_genre())
                
            ML_ht = {'Action': 0, 'Comedy': 0, 'Drama': 0, 'Horror': 0, 'Romance': 0}
            ML_points = 0
            genres_in_ML = 0
            for genre in movie.get_genre():
                if genre in ML_ht:
                    genres_in_ML += 1
                    for i in range(len(users_ML)):
                        ML_ht[genre] += users_ML[i][genre]
                    ML_points += ML_ht[genre] / len(users)
            if ML_points:
                ML_points /= genres_in_ML
                
            result = genre_points*self.FINAL_WAGES['genre'] + (float(movie.rating)/10)*self.FINAL_WAGES['rating']\
                    + ML_points*self.FINAL_WAGES['ML']
            
            if len(top_recomendations) < self.MAX_RECOMENDATIONS:
                top_recomendations.append([result, movie.title, movie.cover_url])
            elif result > top_recomendations[0][0]:
                top_recomendations[0] = [result, movie.title, movie]
            top_recomendations =  sorted(top_recomendations)
        
        return sorted(top_recomendations, reverse=True)
        
