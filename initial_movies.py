from django.contrib.auth.models import User
from morfeusz_app.models import Movie
from users.models import Profile
from imdb import IMDb

ia = IMDb()

initial_movies_id = [
    "0068646",
    "0468569",
    "0167260",
    "0110912",
    "0060196",
    "0080684",
    "0073486",
    "0047478",
    "0114369",
    "0245429",
    "0816692",
    "6751668",
    "0088763",
    "2582802",
    "2674426"
]

print(Movie.objects.all())
# Movie.objects.all().delete()

for mv_id in initial_movies_id:
    if not Movie.objects.filter(imdb_id=mv_id).exists():
        movie = Movie(imdb_id=mv_id)
        movie.set_title()
        movie.set_genre()
        movie.set_cover_url()
        movie.save()
        print(movie)
print(Movie.objects.all())
