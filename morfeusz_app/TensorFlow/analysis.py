import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow.keras.callbacks import TensorBoard
import random
import os
import cv2
import glob
import pickle
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.utils.class_weight import compute_sample_weight, compute_class_weight
from collections import Counter
from sklearn.preprocessing import LabelEncoder
import logging

import data_manager


def prediction(layer_size, conv_layer, dense_layer):

    X, Y = data_manager.load_data()               
    NAME = '{}nodes-{}conv-{}dense'.format(layer_size, conv_layer, dense_layer)
    model = tf.keras.models.load_model('Models/Model_{}.hp5'.format(NAME))
    pred = model.predict([X])

    for i in range(len(X)):
        logging.info(Y[i])
        logging.info(pred[i])
        x = np.fliplr(X[i].reshape(-1,3)).reshape(X[i].shape)
        plt.imshow(x)
        plt.show()
        
