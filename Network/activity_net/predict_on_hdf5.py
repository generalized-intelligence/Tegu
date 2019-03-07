import argparse
import os
import sys
import keras
from keras.models import Model
from Network.activity_net.model import c3d_localization_model
from Network.activity_net.loss import weighted_mse
from Network.activity_net.src.generator import sample_generator
from Network.activity_net.src.data import import_labels
from Network.activity_net.src.processing_multiple_classes import activity_localization, get_classification, smoothing
from keras.optimizers import RMSprop
import json
import h5py
import numpy as np
from random import shuffle

model_to_test = None # input
labels_lines = None # input
annotation_json_str = None


def prepare_models_and_labels():
    global model_to_test,labels_lines,annotation_json_str
    model = model_to_test
    print('Importing labels')
    labels = labels_lines    # Load labels
    #with open('/GI/Documents/Nina/activitynet-2016-cvprw-shit-edition/langqiao_154_videos/labels.txt', 'r') as f:
    #    labels = import_labels(f)
    labels = import_labels(labels_lines)

    print('Importing annotations')
    #with open('/GI/Documents/Nina/activitynet-2016-cvprw-shit-edition/train_c3d/annotations_both_actions.json','r') as f:
    #    anno = json.load(f)
    #anno = json.loads(annotation_json_str)

    #return model,labels, anno
    return model,labels, None


def process_a_video(test_videos,smoothing_k,activity_threshold_1,model_to_test_in,labels_lines_in,annotation_json_str_in=None):
    global model_to_test,labels_lines,annotation_json_str
    labels_lines = labels_lines_in
    model_to_test = model_to_test_in
    annotation_json_str = annotation_json_str_in
    info = ''
    print ('labels_lines',labels_lines)
    info += 'labels_lines {}\n'.format(labels_lines)
    #model, labels, anno = prepare_models_and_labels()
    model,labels,_ = prepare_models_and_labels()

    print ('labels:',labels)
    info += 'labels:'
    info += str(labels)
    info += '\n'
    #test_videos = open(test_video_queue).readlines()
    
    shuffle(test_videos)
    test_video_num = len(test_videos)
    
    for test_video_idx in range(test_video_num):
        #anno_path = '/GI/Documents/Nina/activitynet-2016-cvprw-shit-edition/train_c3d/annotations_both_actions.json'
        fps = 25
        sample_path = test_videos[test_video_idx].split(',')[0]
        video_name = test_videos[test_video_idx].split(',')[1]#[:-1]  
        test_set_gen = sample_generator(video_id = video_name, sample_path = sample_path, anno_path = None,nb_label = 3)
        clips = h5py.File(sample_path,'r')
        nb_clips = clips[video_name].shape[0]

        print('Video_name:',video_name)
        info += video_name
        info += '\n'
        #print('Subset:',anno[video_name]['subset'])
        
        prediction = model.predict_generator(generator=test_set_gen,steps=nb_clips,verbose=1,max_queue_size = 1)
        # import pdb; pdb.set_trace()

        prediction = prediction.reshape(nb_clips, len(labels_lines))
        
        # Post processing the predited output
        print('Post-processing output...')
        labels_idx, scores = get_classification(prediction, k=5)

        prediction_smoothed = smoothing(prediction, k=smoothing_k)
        activities_idx, startings, endings, scores = activity_localization(prediction_smoothed,activity_threshold=.2)

        # TODO：Just do this on evaluate. Do not do this on test.
        '''
        print('\nAnnotation:')
        print('\tInterval\t\tActivity')
        for idx, annotation in enumerate(anno[video_name]['annotations']):
            start = annotation['segment'][0]
            end = annotation['segment'][1]
            label = annotation['label']
            print('{:.1f}s - {:.1f}s\t\t\t{}'.format(start,end,label))
        '''
        info += 'Detection:Score\tInterval\t\tActivity\n'
        print('\nDetection:')
        print('Score\tInterval\t\tActivity')
        for idx, s, e, score in list(zip(activities_idx, startings, endings, scores) ): 

            print ('items:',idx,s,e,score)
            info+='items:{} {} {} {}'.format(idx, s,e,score)
            print ('len(labels),idx',len(labels),idx)
            info += 'len(labels),idx {} {}'.format(len(labels), idx)
            start = s * float(16) / fps
            end = e * float(16) / fps
            label = labels[idx]
            print('{:.4f}\t{:.1f}s - {:.1f}s\t\t{}'.format(score, start, end, label))
            info += '{:.4f}\t{:.1f}s - {:.1f}s\t\t{}'.format(score, start, end, label)
        return info


if __name__ == '__main__':
    '''
    parser = argparse.ArgumentParser(
        description=
        'Run all pipeline. Given a video, classify it and temporal localize the activity on it'
    )

    parser.add_argument(
        '-tvq',
        type=str,
        dest='test_video_queue',
         default='/GI/Documents/Nina/activitynet-2016-cvprw-shit-edition/train_c3d/training_queue/train_video_queue.txt',
        help='Path to the txt that contains the path and video_id')
    parser.add_argument(
        '-k',
        type=int,
        dest='smoothing_k',
        default = 50,
        help='Smoothing factor at post-processing (default: %(default)s)')
    parser.add_argument(
        '-t1',
        type=float,
        dest='activity_threshold_1',
        default=.4,
        help='Activity threshold at post-processing (default: %(default)s)')
    parser.add_argument(
        '-t2',
        type=float,
        dest='activity_threshold_2',
        default=.4,
        help='Activity threshold at post-processing (default: %(default)s)')

    args = parser.parse_args()

    process_a_video(args.test_video_queue, args.smoothing_k,args.activity_threshold_1,args.activity_threshold_2)
    '''
    process_a_video('aaa.mp4',     5,    0.4,      0.2)
