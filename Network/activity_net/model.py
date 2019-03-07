import argparse
import os
import sys
import keras
from keras.layers import LSTM, BatchNormalization, Dense, Dropout, Input, TimeDistributed,noise,regularizers
from keras.models import Model, Sequential
from keras.optimizers import RMSprop
from keras.layers.convolutional import Convolution3D, MaxPooling3D, ZeroPadding3D
from keras.layers.core import Dense, Dropout, Flatten,Reshape


import h5py
import pdb
import numpy as np

def c3d_localization_model(dropout_probability = 0.3,nb_output_type = 3):
    model = Sequential()
    model.add(Convolution3D(64, 3, 3, 3, activation='relu',
                            border_mode='same', name='conv1',
                            subsample=(1, 1, 1),
                            batch_input_shape=(1, 3, 16, 112, 112),
                            trainable=True))
    model.add(MaxPooling3D(pool_size=(1, 2, 2), strides=(1, 2, 2),
                           border_mode='valid', name='pool1'))
    # 2nd layer group
    model.add(Convolution3D(128, 3, 3, 3, activation='relu',
                            border_mode='same', name='conv2',
                            subsample=(1, 1, 1),
                            trainable=True))
    model.add(MaxPooling3D(pool_size=(2, 2, 2), strides=(2, 2, 2),
                           border_mode='valid', name='pool2'))
    # 3rd layer group
    model.add(Convolution3D(256, 3, 3, 3, activation='relu',
                            border_mode='same', name='conv3a',
                            subsample=(1, 1, 1),
                            trainable=True))
    model.add(Convolution3D(256, 3, 3, 3, activation='relu',
                            border_mode='same', name='conv3b',
                            subsample=(1, 1, 1),
                            trainable=True))
    model.add(MaxPooling3D(pool_size=(2, 2, 2), strides=(2, 2, 2),
                           border_mode='valid', name='pool3'))
    # 4th layer group
    model.add(Convolution3D(512, 3, 3, 3, activation='relu',
                            border_mode='same', name='conv4a',
                            subsample=(1, 1, 1),
                            trainable=True))
    model.add(Convolution3D(512, 3, 3, 3, activation='relu',
                            border_mode='same', name='conv4b',
                            subsample=(1, 1, 1),
                            trainable=True))
    model.add(MaxPooling3D(pool_size=(2, 2, 2), strides=(2, 2, 2),
                           border_mode='valid', name='pool4'))
    # 5th layer group
    model.add(Convolution3D(512, 3, 3, 3, activation='relu',
                            border_mode='same', name='conv5a',
                            subsample=(1, 1, 1),
                            trainable=True))
    model.add(Convolution3D(512, 3, 3, 3, activation='relu',
                            border_mode='same', name='conv5b',
                            subsample=(1, 1, 1),
                            trainable=True))
    model.add(ZeroPadding3D(padding=(0, 1, 1), name='zeropadding'))
    model.add(MaxPooling3D(pool_size=(2, 2, 2), strides=(2, 2, 2),
                           border_mode='valid', name='pool5'))
    model.add(Flatten(name='flatten'))
 
    #C3D FC layers - wanted
    model.add(Dense(4096,activation='relu',name='f6',trainable=True))

    #C3D FC layers - unwanted
    model.add(Dropout(.5,name='do1'))
    model.add(Dense(4096,activation='relu',name='fc7'))
    model.add(Dropout(.5,name='do2'))
    model.add(Dense(487,activation='softmax',name='fc8'))

    # Load weights
    if os.path.exists(r"Network\\activity_net\\converted.h5"):
        model.load_weights(r"Network\\activity_net\\converted.h5")
    else:
        model.load_weights(r"Network\\video0\\converted.h5")
    # model.load_weights(r"converted.h5")

    # Pop C3D FC layers
    for _ in range(4):
        model.pop()

    #reshape C3D output
    model.add(Reshape((1,4096)))

    #input of C3D
    inp = model.input  
    print (model.output_shape)
    # FC layers group
    input_normalized = BatchNormalization(name='normalization')(model.layers[-1].output)
    input_dropout = Dropout(rate=dropout_probability)(input_normalized)
    input_noised = noise.GaussianNoise(0.4)(input_dropout)
    lstms_inputs = [input_noised]
   
    #input_normalized = BatchNormalization(name='normalization')(input_features)
    #input_dropout = Dropout(rate=dropout_probability)(input_normalized)
    #input_noised = noise.GaussianNoise(0.4)(input_dropout)
    #lstms_inputs = [input_noised]
    #CHANGE hyperparameters in the for loop below:
    for i in range(1):
        previous_layer = lstms_inputs[-1]
        lstm = LSTM(
            150,
            batch_input_shape = (1,1,4096),
            return_sequences=True,
            stateful=True,
            name='lsmt{}'.format(i + 1))(previous_layer)
        lstms_inputs.append(lstm)
    output_dropout = Dropout(rate=dropout_probability)(lstms_inputs[-1])
    output_noised = noise.GaussianNoise(0.4)(output_dropout)
    #CHANGE first input of Dense to nb_classes
    output = TimeDistributed(
        Dense(nb_output_type, activation='sigmoid'), name='fc')(output_noised)
    model = Model(inputs=inp, outputs=output)
    return model
    
