import numpy as np
import pandas as pd
import random
import os
import cv2
import glob
import pickle
from tqdm import tqdm

def create_data():
    IMG_SIZE = [182, 268]
    if not os.path.exists('Pickle/'):
        os.makedirs('Pickle/')

    df = pd.read_csv('Archive/MovieGenre.csv', encoding='ISO-8859-1')
    paths = glob.glob('Posters/*.jpg')
    X = []
    Y = []
    
    for path in tqdm(paths):
        try:
            start = path.rfind('\\')+1
            end = len(path)-4
            name = path[start:end]
            image = cv2.imread(path)
            image = cv2.resize(image, (IMG_SIZE[0], IMG_SIZE[1]))
            genres = tuple((df[df["imdbId"] == int(name)]["Genre"].values[0]).split("|"))
            X.append(image)
            Y.append(genres)
        except:
            pass
        break

    X = np.asarray(X)

    pickle_out = open('Pickle/X.pickle','wb')
    pickle.dump(X, pickle_out, protocol=4)
    pickle_out.close()
    
    pickle_out = open('Pickle/Y.pickle','wb')
    pickle.dump(Y, pickle_out)
    pickle_out.close()


def load_data(mix=False):
    pickle_in = open('Pickle/X.pickle','rb')
    X = pickle.load(pickle_in)
    X = np.array(X)

    pickle_in = open('Pickle/Y.pickle','rb')
    Y = pickle.load(pickle_in)
    Y = np.array(Y)

    if mix:
        perm = np.random.permutation(len(X))
        X = X[perm]
        Y = Y[perm]

    return [X, Y]
