import cv2
import os
import json
import numpy as np
import time
import h5py
import random

# This script aims at generating video clips in compressed numpy array from a given json_file
# any generated numpy array is of shape (3, 16, 160, 160) where 3 represents number of color
# channels, 16 represents number of frames in a given video clip and 160 represents image size

# to use this script, specify video root dir, json file, and resulted target folder where you want to
# store the generated files

def process_video_dir(video_dir,target_file,info_que=None,only_process_video_names_list = None):  # if videos_list is passed:only deal with these videos.

    #video_dir = '/GI/changsha/changsha_backup/ChangShaAirport2/'
    #target_file = '/GI/changsha1/videos_1080_2.hdf5'
   

    mode = 'r+' if os.path.exists(target_file) else 'w'
    output_file = h5py.File(target_file,mode)

    #f = open('./ylbl_2.txt').readlines()
    #videos = []
    #for i in f:
    #    videos.append(i.split('\n')[0])
    videos = []
    if not only_process_video_names_list:
        videos = os.listdir(video_dir)
    else:
        videos = only_process_video_names_list

    print('Number of Videos in json file is', len(videos))
    if info_que:
        print('1')
        info_que.put('Number of Videos in result file is: {}'.format(len(videos)))

    
    for idx, video_id in enumerate(videos):
        print(idx)
        if info_que:
            info_que.put('curent idx: {} video_name: {}'.format(idx,video_id))

        video_path = str(os.path.join(video_dir, video_id))
        video_id = video_id.split('.')[0]
        if os.path.exists(video_path):
            pass
        else:
            continue
        # if os.path.exists(target_video_folder):
        #     print('Path exists :', target_video_folder)
        #     continue
        # else:
        #     target_video_folder = '/home/gi/software/p3d/video2' + '/' + str(json_name)
        #     if os.path.exists(target_video_folder):
        #         continue
        #     else:
        #         os.mkdir(target_video_folder)
        #         target_video_path = target_video_folder + '/' + str(json_name) + '_' + str(0)
        #         print(target_video_path)


        # Video Capture --------------------------------
        video = cv2.VideoCapture(video_path)
        video_hz = video.get(5)
        video_length = int(video.get(7))
        print('video length is: {}'.format(video_length))
        # ----------------------------------------------
        if info_que:
            info_que.put('video length is: {}'.format(video_length))

        clip_array = np.zeros((16,112,112,3))
        for i in range(video_length):
            try:
                state, frame = video.read()
                print(frame.shape)
            except:
                
                print('reading frame error')
                continue

            if i % 16 == 0 and i is not 0:
                clip_array = clip_array.transpose(0,3,1,2)
                #clip_array = clip_array.transpose(1,0,2,3)
                clip_array = np.expand_dims(clip_array,axis=0)
                clip_array = clip_array.transpose(0,2,1,3,4)
                print(clip_array.shape)
                with h5py.File(target_file,'r+') as f:
                    if video_id in f.keys():
                        f[video_id].resize((f[video_id].shape[0]+clip_array.shape[0]),axis=0)          
                        f[video_id][-clip_array.shape[0]:]=clip_array
                        h5py.File.flush(f)
                    else:
                        f.create_dataset(video_id,data=clip_array,dtype='float32',maxshape=(None,3,16,112,112))
                        h5py.File.flush(f)
                print('Saved video: {}'.format(video_id))
                # if info_que:
                #     info_que.put('Saved video: {}'.format(video_id))
                
                if i % 160 == 0:
                    print('Current Frame and Time:', i, i / video_hz, '' 'Percentage : ',
                        i / float(video_length), 'Current clip label : ', idx)
                    out = 'Current Frame and Time:{} {} Percentage: {} Current clip label: {}'.format(i, i/video_hz, i/float(video_length), idx)
                    if info_que:
                        info_que.put(out)

                clip_array = np.zeros((16,112,112,3))

            
            print('goooooo::  {}::  {}'.format(video_length,i))  
            frame = cv2.resize(frame, (112, 112))
            print('okkkkkk')
            frame = np.array(frame,dtype=np.float32)
            clip_array[i%16,:, :, :] = frame


if __name__ == '__main__':
    process_video_dir(r'D:\AirportDataset',r'D:\AirportDataset\hdf5\video_output.hdf5')
    














