from django.contrib.auth.models import User
from morfeusz_app.models import Movie
from users.models import Profile
from imdb import IMDb

ia = IMDb()

print(Movie.objects.all())
print(Movie.objects.all().count())
# print(User.objects.all())

# user = User.objects.all().first()
# profile = Profile(user_profile=user)
# profile.save()
print(User.objects.all())
user = User.objects.filter(username='test_user_1').first()
profile = user.user_profile
# profile.movies_like_watch.all().delete()
# profile.movies_dont_like.clear()
# profile.movies_like_dont_watch.clear()
# profile.movies_like_watch.clear()
# profile.movies_watch.clear()
print(profile.movies_dont_like.all())
print(profile.movies_like_dont_watch.all())
print(profile.movies_like_watch.all())
print(profile.movies_watch.all())
print(profile.all_movies_pk())
# print(Movie.objects.all().filter(title='Pulp Fiction').first().pk)
# print(Movie.objects.filter(pk=23))

# top = ia.get_top250_movies()
# for movie in top[0:50]:
#     print('{} {}'.format(movie['title'], movie.movieID))
# print(type(popular[0]))
# print(type(popular))

# # user2 = User(username="CD")
# # user2.save()
#
# # movie1 = Movie(movie_imdb_id='0074226')
# # movie1.set_title()
# # movie1.save()
#
# print(User.objects.all())
# # user1 = User.objects.get(username="KF")
# # user2 = User.objects.get(username="AB")
# # print(user1.movies)
# #
# print(Movie.objects.all())
# user1 = User.objects.get(username="AB")
# user2 = User.objects.get(username="CD")
# # profile1 = Profile(user_profile=user2)
# # profile1.save()
# profile1 = Profile.objects.all().first()
# profile2 = Profile.objects.get(user_profile=user2)
#
# movie1 = Movie.objects.all().first()
# movie2 = Movie.objects.get(title="The Untouchables")
# print(movie1.movie_imdb_id)
# print(movie2.movie_imdb_id)
# # profile1.movies_N.add(movie2)
# profile2.movies_N.add(movie2)
# print(profile1.movies_N.all())
# print(user1.user_profile.movies_N.all())
# print(user2.user_profile.movies_N.all())
# print(movie1.movies.all())
# print(movie2.movies.all())
# print(Movie.objects.all())
