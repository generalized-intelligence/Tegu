import keras.backend as K 
K.set_image_data_format('channels_first')
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

from Network.Util.decrypt import decrypt_txt_file
import Network.activity_net.serval_to_content as serval_to_content

import Network.activity_net.video_hdf5_generator as video_hdf5_generator
import json

import Network.activity_net.predict_on_hdf5 as predict_on_hdf5
from Util.mylogger import MyLogger

__MODE__ = 'RELEASE' # 'RELEASE'


class ActivityNet_Model:  # backend of AI-builder.
    def __init__(self,input_shape=None, lr=0.0001,loss=None):
        '''
        Management of training and predict.
        Parameters are hyperparameters that allow adjustments.

        Args:
            input_shape -- The shape of each key frame to resized.
            lr -- Learning rate.
            loss -- Coustom loss function.
        '''
        self.input_shape = input_shape
        self.lr = lr
        self.loss = loss
        if loss==None:
            self.loss=weighted_mse

        

    def set_dataset(self,dataset,pretrained=None,eval=False,extra_params=None):  
        '''It is not precise to call this object 'data_generator'.It has 2 generators inside.So I usedata_loader instead.
        2 generators are:generate_train,generate_valid.'''
        self.dataset = dataset  # is the expanded form of "for train_video_idx in range(len(train_videos))".
        self.trainset_gen = self.dataset.generate_train()
        self.testset_gen = self.dataset.generate_valid()
        self.nb_output_type = self.dataset.nb_label
        self.model = c3d_localization_model(nb_output_type= self.nb_output_type)
        self.model.compile(
            loss=self.loss,
            optimizer=self.rmsprop,
            metrics=[weighted_mse,'accuracy'])
        
    def train(self, extra_params=None):
        video_count = self.dataset.video_count
        trian_history_list = []
        for i in range(video_count):
            trian_history = train_1_vid(extra_params)
            trian_history_list.append(trian_history)


    def train_1_vid(self,extra_params=None):
       ''' Call this function once ,you do train on 1 video only.
        Just repeat calling this function for nb_train_videos times to train on the whole batch for 1 time.
        Make your own function by calling this for N times if you DO need this.'''


        #self.callback_file = 'train_c3d/exp002/best_model_{experiment_id}.h5'.format(experiment_id = experiment_id)
        #checkpoint = ModelCheckpoint(self.callback_file, monitor='loss', verbose=1, save_best_only=True, mode='min')
        #callbacks_list = [checkpoint]

        # get data from generator.
        assert self.dataset is not None
        #train_video_idx,train_videos,anno_path,nb_label= next(self.trainset_gen)
        train_video_idx,train_videos,anno_txt,nb_label= next(self.trainset_gen)
        
        sample_path = train_videos[train_video_idx].split(',')[0]
        clips = h5py.File(sample_path,'r')
        video_name = train_videos[train_video_idx].split(',')[1][:-1]
        while video_name not in list(clips.keys()):  # skip error video keys.
            print((video_name,'not in ',list(clips.keys())))
            train_video_idx,train_videos,anno_txt,nb_label= next(self.trainset_gen)
        
            sample_path = train_videos[train_video_idx].split(',')[0]
            clips = h5py.File(sample_path,'r')
            video_name = train_videos[train_video_idx].split(',')[1]#[:-1]
        
        #train_set_gen = sample_generator(video_id = video_name, sample_path = sample_path, anno_path = anno_path,nb_label = nb_label)
        train_set_gen = sample_generator(video_id = video_name, sample_path = sample_path, anno_txt=anno_txt,nb_label = nb_label)

        
        print ('sample_path:',sample_path)
        
        nb_clips = clips[video_name].shape[0]

        #train one clip at a time, but lstm stateful = True allows each clips establish relatiionship with the clips before
        print('Video ID:',train_video_idx)
        # Train on a video.

        
        # self.model.save('Network\\activity_net\\temp_model.kerasmodel')
        # print('save done')
        #exit()#debug



        train_1vid_info = self.model.fit_generator(
        generator=train_set_gen,
        steps_per_epoch = nb_clips,
        max_queue_size = 1,
        verbose=1,
        nb_epoch=1,
        shuffle=False,
        callbacks=[])

        #reset the model states after training each video
        print('Reseting model states')
        self.model.reset_states()
        print('end 1 video')
        
        return train_1vid_info

    def test(self): 
        '''Just do test on 1 video.Same as train.'''
        val_video_idx,val_videos,anno_txt,nb_label= next(self.testset_gen)

        sample_path = val_videos[val_video_idx].split(',')[0]
        video_name = val_videos[val_video_idx].split(',')[1]#[:-1]
        #val_set_gen = sample_generator(video_id = video_name, sample_path = sample_path, anno_path = anno_path, nb_label = nb_label)
        val_set_gen = sample_generator(video_id = video_name,sample_path = sample_path,anno_txt=anno_txt,nb_label=nb_label)
        clips = h5py.File(sample_path,'r')
        nb_clips = clips[video_name].shape[0]

        #evaluate one clip at a time until all clips are evaluated
        print('Evaluating...')
        eval_1vid_result = self.model.evaluate_generator(generator=val_set_gen,steps=nb_clips)
        print('Reseting model states')

        self.model.reset_states()

        return eval_1vid_result

    def load_kerasmodel(self,model_path = 'Network\\activity_net\\temp_model.kerasmodel'):
        self.model = keras.models.load_model(model_path,compile=False)

    def predict(self,video_file_path, label_count, out_signal=None):
        '''Predict one video'''
        #step1:prepare a hdf5 file.
        dir_path,video_file_name = os.path.split(video_file_path)
        print('dir_path: ',dir_path)
        print('video_file_name', video_file_name)
        temp_video_hdf5_file_path = os.path.join('dir_path', 'temp.hdf5')
        # temp_video_hdf5_file_path = 'Network\\activity_net\\test_video_tmp.hdf5'  # this is not a input parameter but just a temp file path.
        
        print('Trying to predict....')
        # video_hdf5_generator.process_video_dir(dir_path,temp_video_hdf5_file_path,only_process_video_names_list=[video_file_name])
        if not os.path.exists(temp_video_hdf5_file_path):
            video_hdf5_generator.process_video_dir(dir_path,temp_video_hdf5_file_path,only_process_video_names_list=[video_file_name])
        
        assert os.path.exists(temp_video_hdf5_file_path)
        #step2:call the api.
        test_video_queue = ['{0},{1}'.format(temp_video_hdf5_file_path,video_file_name.split('.')[0])]#TODO:how does this file inside looks like?
        print('test_video_queue: ',test_video_queue)
        # def gen_label_lines():
        #     label_list = []
        #     for i in range(self.dataset.itemcount+1):
        #         label_list.append("{0}\t{1}".format(i,i))
        #     return label_list
        def gen_label_lines():
            label_list = []
            for i in range(label_count+1):
                label_list.append("{0}\t{1}".format(i,i))
            return label_list
        label_lines = gen_label_lines()

        return predict_on_hdf5.process_a_video(test_video_queue,5,0.5,self.model,label_lines)
        

        

class ActivityNet_Dataloader:
    def __init__(self,video_dir_path,train_serval_file_path,test_serval_file_path,hdf5_path, extra_params=None):
        '''
        Manager of SSD datasets.

        Args:
            video_dir_path -- Folder of videos.
            train_serval_file_path -- Annotation path of training set.
            test_serval_file_path -- Annotation path of testing set.
            hdf5_path -- Preprocessed h5 file.
            extra_params -- Custom parameter.
        '''
        self.train_serval_file_content,self.test_serval_file_content = None,None  # decoded and transformed into json. I don't care how this shit is generated.
        _, content = decrypt_txt_file(train_serval_file_path)
        self.video_count = len(content.split('\n')) - 2
        self.itemcount = len( content.split('\n')[1].split(',')  )
        
        serval_to_content.DATA_DIR = video_dir_path
        self.train_serval_file_content = serval_to_content.trans_to_json(
            decrypt_txt_file(train_serval_file_path)
            )  
        
        self.test_serval_file_content = serval_to_content.trans_to_json(
                decrypt_txt_file(test_serval_file_content)
        )


        self.test_serval_file_content = self.train_serval_file_content

        # self.store_weights_root = 'train_c3d/exp002/' # input 1
        # self.store_weights_file = 'lstm_activity_classification_{experiment_id}_e{epoch:03}.hdf5' # input 2


        #self.anno_path = anno
        #self.val_video_queue="test.txt"  # input 3
        #self.train_video_queue="test.txt" # input 4
        self.nb_label = 3 # input 5

        #"test.txt",#extra_params['val_video_queue'],extra_params['train_video_queue'],extra_params['nb_label']

        #self.train_videos = open(self.train_video_queue).readlines()
        #self.val_videos = open(self.val_video_queue).readlines()

        video_output_path = hdf5_path
        
        self.train_videos = list(map(lambda x:(video_output_path+','+x),list(json.loads(self.train_serval_file_content).keys())))  # input 3 here.
        self.val_videos = list(map(lambda x:(video_output_path+','+x),list(json.loads(self.test_serval_file_content).keys())))

        # self.train_videos = list(map(lambda x:('d:\\AirportDataset\\hdf5\\video_output.hdf5'+','+x),list(json.loads(self.train_serval_file_content).keys())))  # input 3 here.
        # self.val_videos = list(map(lambda x:('d:\\AirportDataset\\hdf5\\video_output.hdf5'+','+x),list(json.loads(self.test_serval_file_content).keys())))
        print (list(  (json.loads(self.train_serval_file_content)).keys()              )  )
        #print (self.train_videos)
        self.minibatch_count = (len(self.train_videos),len(self.val_videos))  #  This is the count of videos,not just c3d batches.
        # '''
        # self.nb_train_samples = 0
        # for i in range(len(self.train_videos)):
        #     sample_path = self.train_videos[i].split(',')[0]
        #     video_name = self.train_videos[i].split(',')[1][:-1]
        #     train_video_file = h5py.File(sample_path,'r')
        #     self.nb_train_samples += train_video_file[video_name].value.shape[0]

        # self.nb_val_samples = 0
        # for i in range(len(self.val_videos)):
        #     sample_path = self.val_videos[i].split(',')[0]
        #     video_name = self.val_videos[i].split(',')[1][:-1]
        #     val_video_file = h5py.File(sample_path,'r')
        #     self.nb_val_samples += val_video_file[video_name].value.shape[0]
        # '''

    def do_video_to_hdf5(self,video_dir_path,only_process_video_names_list=None):
        '''
        Extract video information as hdf5 file

        Args:
            video_dir_path -- Folder of videos.
            only_process_video_names_list -- If is not None, Specify a list of videos.
        '''
        print('Video convert to HDF5 start!')
        video_hdf5_generator.process_video_dir(video_dir,os.path.join(video_dir_path,'output_videos.hdf5'),only_process_video_names_list = only_process_video_names_list)
        print('Video converted to HDF5 file done!')

    def generate_train(self):
        '''training set generator.'''
        while True:  # Training process not stopped.
            for i in range(len(self.train_videos)): # for each video_id:
                #yield i,self.train_videos,self.anno_path,self.nb_label
                yield i,self.train_videos,self.train_serval_file_content,self.nb_label

    def generate_valid(self):  
        '''validation set generator.'''
        while True:
            for i in range((len(self.val_videos))):
                #yield i,self.val_videos,self.anno_path,self.nb_label
                yield i,self.val_videos,self.test_serval_file_content,self.nb_label
