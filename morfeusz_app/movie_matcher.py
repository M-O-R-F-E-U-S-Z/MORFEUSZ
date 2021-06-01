import random


categories = ['comedy', 'animation', 'horror', 'triller', 'documentary',
              'action', 'romance', 'western', 'mystery', 'drama', 'anime']
#random imdb movies gen:
def generate_movie():
    movie = [[], random.random()] #[category, score from 0 to 1]
    for i in range(random.randrange(1, 5)):
        if (category := random.choice(categories)) not in movie[0]:
            movie[0].append(category)
    return movie

def update_hash_table(user, opinion):
    for movie in user[opinion]:
        for category in movie[0]:
                opinion_hash_table[category][0] += opinion_wages[opinion]
                opinion_hash_table[category][1] += 1

#wages for L/DL/WTS/DWTS:
opinion_wages = {
    'L': 1,
    'DL': -1.5,
    'WTS': 1,
    'DWTS': -1.5
}

opinion_hash_table = {
    #[wages score, num of rates]
    "comedy": [0,0],
    "animation": [0,0],
    "horror": [0,0],
    "triller": [0,0],
    "documentary": [0,0],
    "action": [0,0],
    "romance": [0,0],
    "western": [0,0],
    "mystery": [0,0],
    "drama": [0,0],
    "anime": [0,0]
}

if __name__ == "__main__":

    n_movies = 1000
    movies = [generate_movie() for i in range(n_movies)]

    n_users = 5
    n_opinions = 35
    users = [{'L': [], 'DL': [], 'WTS': [], 'DWTS': []} for i in range(n_users)]

    for user in users:
        for i in range(n_opinions):
            opinion = random.choice(['L', 'DL', 'WTS', 'DWTS'])
            movie = random.choice(movies) 
            user[opinion].append(movie)

    #######################################################
    # F I N A L  M O V I E S  R E C O M E N D A T I O N S #
    #######################################################

    for user in users:
        update_hash_table(user, 'L')
        update_hash_table(user, 'DL')
        update_hash_table(user, 'WTS')
        update_hash_table(user, 'DWTS')

    #changing opinion ht to single values per key
    for key, value in opinion_hash_table.items():
        opinion_hash_table[key] = value[0] / value[1] + 0.5

    wages ={
        'category': 0.6, #-0.1
        'score': 0.4, 
        #'ML': 0.1
    }

    max_recomendations = 10
    top_recomendations = []

    for movie in movies:

        category_points = 0
        for category in movie[0]:
            category_points += opinion_hash_table[category]
        category_points /= len(movie[0])

        result = category_points*wages['category'] + movie[1]*wages['score']#\
                #+ random.random()*wages['ML']
        
        top_recomendations.sort
        if len(top_recomendations) < max_recomendations:
            top_recomendations.append([result, movie])
        elif result > top_recomendations[0][0]:
            top_recomendations[0] = [result, movie]

    for key, value in opinion_hash_table.items():
        print(key, value)
    
    for movie in sorted(top_recomendations, reverse=True):
        print(movie)