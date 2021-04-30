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
- creating and managing your account,
- adding friends, creating friends groups,
- searching movies
- adding films to favorites
- comparing and matching films you want to watch with films of your friends/groups

cat 2 (top priority)
- machine learning algorithm for predicting movie's characteristics from its cover,
- adding movies’ posters

cat 3 (low priority)
- chat,
- dark theme
	
Roadmap:

sprint 1: 
- research report: (P. Potępa)
  - data sources
  - how to get characteristic of the movie
  - machine learning on this dataset
- basic structure of project (everyone)
- user registration (A. Szemalikowska)
- connecting MySQL to Django (R. Damian)
- connecting to IMDb film database (K. Fułat)
- integration with heroku (everyone)

sprint 2: 
- Basic UI layout (K. Dziadkowiec)
- friends funcionality (A. Szemalikowska)
- adding films to favorites (K. Fułat)
- comparing and matching films between users/groups (R. Damian)
- poster database (P. Potępa)

sprint 3: 
- machine learning implementation (P. Potepa, R. Damian)
- writing tests (R. Damian, K. Fułat)

sprint 4: 
- styling (everyone)
- working on extra features (everyone)

Basic requirements:
- continuous integration with heroku
- at least one automatic unittest (it will be automatically tested on github)
- registration
- user is related to other users as friends
- research report:
  - data sources
  - how to get characteristic of the movie
  - machine learning on this dataset
- data source connected to the database (if it's too much we can drop it)
