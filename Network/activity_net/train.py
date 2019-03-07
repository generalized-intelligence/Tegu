import argparse
import os
import sys
import keras
from keras.layers import LSTM, BatchNormalization, Dense, Dropout, Input, TimeDistributed,noise,regularizers
from keras.models import Model
from keras.optimizers import RMSprop
from Network.activity_net.model import c3d_localization_model
from Network.activity_net.loss import weighted_mse
from Network.activity_net.src.generator import sample_generator
from keras.callbacks import ModelCheckpoint

import h5py
import pdb
import numpy as np
    
def train(val_video_queue,train_video_queue,nb_label,anno_path,experiment_id, batch_size, epochs, lr):

    train_videos = open(train_video_queue).readlines()
    val_videos = open(val_video_queue).readlines()

    nb_train_samples = 0
    for i in range(len(train_videos)):
        sample_path = train_videos[i].split(',')[0]
        video_name = train_videos[i].split(',')[1][:-1]
        train_video_file = h5py.File(sample_path,'r')
        nb_train_samples += train_video_file[video_name].value.shape[0]

    nb_val_samples = 0
    for i in range(len(val_videos)):
        sample_path = val_videos[i].split(',')[0]
        video_name = val_videos[i].split(',')[1][:-1]
        val_video_file = h5py.File(sample_path,'r')
        nb_val_samples += val_video_file[video_name].value.shape[0]

    print('Experiment ID {}'.format(experiment_id))
    print('batch_size: {}'.format(batch_size))
    print('epochs: {}'.format(epochs))
    print('learning rate: {}'.format(lr))
    print('number of training videos:{}'.format(len(train_videos)))
    print('number of training clips:{}'.format(nb_train_samples))

    ######CHANGE root#########
    store_weights_root = 'train_c3d/exp002/'
    store_weights_file = 'lstm_activity_classification_{experiment_id}_e{epoch:03}.hdf5'
    callback_file = 'train_c3d/exp002/best_model_{experiment_id}.h5'.format(experiment_id = experiment_id)
    ##########################

    print('Compiling model')
    model = c3d_localization_model()
    model.summary()
    
    rmsprop = RMSprop(lr=lr)
    model.compile(
        loss=weighted_mse,
        optimizer=rmsprop,
        metrics=[weighted_mse,'accuracy'])
    print('Model compiled')

    checkpoint = ModelCheckpoint(callback_file, monitor='loss', verbose=1, save_best_only=True, mode='min')
    callbacks_list = [checkpoint]

    for epoch_nb in range(1, epochs + 1):
        print('Epoch {}/{}'.format(epoch_nb, epochs))
        
        for train_video_idx in range(len(train_videos)):
        #for train_video_idx in range(164,165):
            #the generator generates one clip at a time
            sample_path = train_videos[train_video_idx].split(',')[0]
            video_name = train_videos[train_video_idx].split(',')[1][:-1]  
            train_set_gen = sample_generator(video_id = video_name, sample_path = sample_path, anno_path = anno_path,nb_label = nb_label)
            clips = h5py.File(sample_path,'r')
            nb_clips = clips[video_name].shape[0]
 
            #train one clip at a time, but lstm stateful = True allows each clips establish relatiionship with the clips before
            print('Video ID:',train_video_idx)
            model.fit_generator(
            generator=train_set_gen,
            steps_per_epoch = nb_clips,
            max_queue_size = 1,
            verbose=1,
            nb_epoch=1,
            shuffle=False,
            callbacks=callbacks_list)
        
            #reset the model states after training each video
            print('Reseting model states')
            model.reset_states()

            if (train_video_idx%50) ==0:
                print('Saving snapshot within epoch')
                save_name = 'experiment_{experiment_id}_epoch{epoch_nb}_video_idx{train_video_idx}.hdf5'.format(experiment_id=experiment_id,epoch_nb=epoch_nb,train_video_idx=train_video_idx)
                save_path = os.path.join(store_weights_root, save_name)
                model.save_weights(save_path)
    
  
        for val_video_idx in range(len(val_videos)):
            #the generator generates one clip at a time
            sample_path = val_videos[val_video_idx].split(',')[0]
            video_name = val_videos[val_video_idx].split(',')[1][:-1]   
            val_set_gen = sample_generator(video_id = video_name, sample_path = sample_path, anno_path = anno_path, nb_label = nb_label)
            clips = h5py.File(sample_path,'r')
            nb_clips = clips[video_name].shape[0]

            #evaluate one clip at a time until all clips are evaluated
            print('Evaluating...')
            model.evaluate_generator(generator=val_set_gen,steps=nb_clips)


        if (epoch_nb % 1) == 0:
            print('Saving snapshot...')
            save_name = store_weights_file.format(
                experiment_id=experiment_id, epoch=i)
            save_path = os.path.join(store_weights_root, save_name)
            model.save_weights(save_path)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Train the RNN ')
   
    parser.add_argument(
        '--valq',
        dest='val_video_queue',
        default=r"test.txt",
        help='A text file that documents validation video input sequence and the path of hdf5 which the videos clips are stored')

    parser.add_argument(
        '--trq',
        dest='train_video_queue',
        default=r"test.txt",
        help='A text file that documents training video input sequence and the path of hdf5 which the videos clips are stored')

    parser.add_argument(
        '--nb_label',
        dest='nb_label',
        default=3,
        help='Number of class plus background')


    parser.add_argument(
        '--anno',
        dest='anno_path',
        default=r"annotations_both_actions.json",
        help='A json file that stores all annotations')

    parser.add_argument(
        '--id',
        dest='experiment_id',
        default=0,
        help='Experiment ID to track and not overwrite resulting models')

    parser.add_argument(
        '-b',
        '--batch-size',
        type=int,
        dest='batch_size',
        default=1,
        help=
        'batch size used to create the stateful dataset (default: %(default)s)')

    parser.add_argument(
        '-e',
        '--epochs',
        type=int,
        dest='epochs',
        default=4000,
        help='number of epochs to last the training (default: %(default)s)')
    parser.add_argument(
        '-l',
        '--learning-rate',
        type=float,
        dest='learning_rate',
        default=1e-5,
        help='learning rate for training (default: %(default)s)')

    args = parser.parse_args()
    
    train(args.val_video_queue,args.train_video_queue,args.nb_label,args.anno_path,args.experiment_id,args.batch_size, args.epochs, args.learning_rate)
