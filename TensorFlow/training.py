import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow.keras.callbacks import TensorBoard
import random
import os
import cv2
import glob
import pickle
from tqdm import tqdm
import csv
import pandas as pd
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.utils.class_weight import compute_sample_weight, compute_class_weight
from collections import Counter
from sklearn.preprocessing import LabelEncoder

import data_manager

CLASSES = ['Action', 'Comedy', 'Drama', 'Horror', 'Romance']

def model(layer_sizes, conv_layers, dense_layers, epochs):

    if not os.path.exists('Models'):
        os.makedirs('Models')
    if not os.path.exists('Logs'):
        os.makedirs('Logs')

    X, Y = data_manager.load_data(mix=0)
    idx = []
    for i,y in enumerate(Y):
        if not any(genre in CLASSES for genre in y):
            idx.append(i)
    X = np.delete(X, idx, axis=0)
    Y = np.delete(Y, idx)
    X = X/255.0
    mlb = MultiLabelBinarizer(CLASSES)
    Y = mlb.fit_transform(Y)
    CLASSES_NUM = len(Y[0])
    
    for layer_size in layer_sizes:
        for conv_layer in conv_layers:
            for dense_layer in dense_layers:
                    
                NAME = '{}nodes-{}conv-{}dense'.format(layer_size, conv_layer, dense_layer)
                model = tf.keras.models.Sequential()

                if conv_layer>0:
                    model.add(tf.keras.layers.Conv2D(layer_size, (3, 3), input_shape=X.shape[1:], padding='same'))
                    model.add(tf.keras.layers.Activation('relu'))
                    model.add(tf.keras.layers.BatchNormalization())
                    model.add(tf.keras.layers.MaxPooling2D(pool_size=(2, 2)))
                    model.add(tf.keras.layers.Dropout(0.25))

                    for l in range(conv_layer-1):
                        model.add(tf.keras.layers.Conv2D(layer_size, (3, 3), padding='same'))
                        model.add(tf.keras.layers.Activation('relu'))
                        model.add(tf.keras.layers.BatchNormalization())
                        model.add(tf.keras.layers.MaxPooling2D(pool_size=(2, 2)))
                        model.add(tf.keras.layers.Dropout(0.25))

                model.add(tf.keras.layers.Flatten())
                for l in range(dense_layer):
                    model.add(tf.keras.layers.Dense(layer_size))
                    model.add(tf.keras.layers.Activation('relu'))
                    model.add(tf.keras.layers.BatchNormalization())

                    model.add(tf.keras.layers.Dropout(0.5))

                model.add(tf.keras.layers.Dense(CLASSES_NUM))
                model.add(tf.keras.layers.Activation('sigmoid'))

                tensorboard = TensorBoard(log_dir=os.path.join('Logs\\{}'.format(NAME)))

                adam = tf.keras.optimizers.Adam(lr=1e-4, beta_1=0.9, beta_2=0.999,
                                                epsilon=1e-07, amsgrad=False)

                model.compile(loss='binary_crossentropy',
                              optimizer=adam,
                              metrics=['accuracy'])

                model.fit(X, Y,
                          batch_size=32,
                          epochs=epochs,
                          validation_split=0.2,
                          callbacks=[tensorboard])

                tf.keras.models.save_model(model, 'Models/Model_{}.hp5'.format(NAME), save_format='h5')
