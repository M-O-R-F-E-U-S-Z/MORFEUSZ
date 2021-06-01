import numpy as np
import tensorflow as tf
import os
import cv2
import glob
import pickle
import logging

import data_manager

MODEL_EXTENSION = '.hp5'

def prediction(layer_size, conv_layer, dense_layer):

    X, Y = data_manager.load_data()               
    NAME = '{}nodes-{}conv-{}dense'.format(layer_size, conv_layer, dense_layer)
    model = tf.keras.models.load_model('Models/Model_{}{}'.format(NAME, MODEL_EXTENSION))
    pred = model.predict([X])

    for i in range(len(X)):
        logging.info(Y[i])
        logging.info(pred[i])
        x = np.fliplr(X[i].reshape(-1,3)).reshape(X[i].shape)
        plt.imshow(x)
        plt.show()
        
