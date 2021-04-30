Project: MORFEUSZ
(Movies Open Reliable Finder Extra User-friendly Search-engine Zero)

Participants:
Rafał Damian (tl)
Alicja Szemalikowska
Patrycja Potępa
Karol Fułat 
Krzysztof Dziadkowiec

Short description of the idea:
Tinder for movies. App for deciding what movies to watch with Your friends, based on Your preferences.

Technology stack:
Back-end: Django, MySQL, Heroku
Front-end: ReactJS, TailwindCSS

Features
cat 1 (core features)
creating and managing your account,
adding friends, creating friends groups,
searching movies
adding films to favorites
comparing and matching films you want to watch with films of your friends/groups

cat 2 (top priority)
machine learning algorithm for predicting movie's characteristics from its cover,
adding movies’ posters

cat 3 (low priority)
chat,
dark theme
	
Roadmap:
sprint 1: 26.04 - 02.05
basic structure of project
connecting MySQL to Django
connecting to IMDb film database
sprint 2: 03.05 - 09.05
Basic UI layout
sprint 3: 10.05 - 16.05
machine learning implementation
writing tests
sprint 4: 17.05 - 23.05
styling
working on extra features


- continuous integration with heroku
- at least one automatic unittest (it will be automatically tested on github)
- registration
- user is related to other users as friends
- research report:
  - data sources
  - how to get characteristic of the movie
  - machine learning on this dataset
- data source connected to the database (if it's too much we can drop it)
