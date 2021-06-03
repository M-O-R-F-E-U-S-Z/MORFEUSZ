from django.contrib.auth.models import User
from morfeusz_app.models import Movie
from imdb import IMDb

ia = IMDb()

initial_movies = ia.get_top250_movies()
print(Movie.objects.all())
Movie.objects.all().delete()

for new_movie in initial_movies:
   if not Movie.objects.filter(imdb_id=str(new_movie.movieID)).exists():
        movie = Movie(imdb_id=str(new_movie.movieID), title=movie['title'])
        movie.set_genre()
        movie.set_cover_url()
        movie.save()
        print(movie)

print(Movie.objects.all())
