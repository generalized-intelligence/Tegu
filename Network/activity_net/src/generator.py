import h5py
import json
import numpy as np
import keras.models

def to_categorical(video_id,sample_idx,annos,nb_label):
    'convert multi-labeled annotation.json into hot-encoded vector,every 16-frame clip generates one hot_encoded vector'
    #for each 16-frame clip, generate a 16xnb_label array consisting of 1s and 0s for ground truth of each frame
    nb_frames = annos[video_id]['num_frames']
    output_array = np.zeros((16,nb_label))
    counter = 0
    
    #loop through 16 frames, and convert each frame index wrt clip to frame index wrt the whole video
    for frame_idx in range(sample_idx*16,sample_idx*16+16): 
        t = frame_idx / float(nb_frames) * annos[video_id]['duration']

        #loop through all annotations under the video_id,and if a label exists, convert 0 to 1
        for annotation in annos[video_id]['annotations']:
            label = int(annotation['label'])
            if t >= annotation['segment'][0] and t <= annotation['segment'][1]:
                #print('counter',counter,'label',label)
                output_array[counter,label] = 1. 
        counter += 1

    gt = np.zeros((1,nb_label))
    gt[0,0] = 1.
    #loop through each class, and if 8/16 frame is annotated as this class,then true, else consider as background
    for cls in range(1,nb_label):
        if (np.count_nonzero(output_array[:,cls])) >= 8:
            gt[0,cls] = 1.
            gt[0,0] = 0.
    return gt
  

def sample_generator(video_id,sample_path,anno_path=None,anno_txt = None ,nb_label=3):
    'generate a 16-frame clip and its hot-encoded vector'
    error_hdf5 = open('./error_hdf5.txt','a')
    videos = h5py.File(sample_path,'r') 
    annos = None
    if anno_txt is None and anno_path is not None:
        with open(anno_path) as f:
            annos = json.load(f)
    else:
      if anno_txt is not None:
        print (('anno_txt',anno_txt))
        annos = json.loads(anno_txt)
      else:
        pass
    nb_samples = videos[video_id].shape[0]
    while True: 
        for sample_idx in range(nb_samples):
                #try:
                X = np.reshape(videos[video_id][sample_idx,:,:,:,:],(1,3,16,112,112))
                if X.shape != (1,3,16,112,112):
                     print('Error: Sample shape is not (3,16,112,112)',X.shape)
                     continue
                if annos is not None:
                    Y = to_categorical(nb_label=nb_label,video_id = video_id,sample_idx = sample_idx, annos = annos)
                    Y = np.reshape(Y,(1,1,3))
                    #print video_id,sample_idx
                    yield X,Y
                else:
                    yield X,None
                    '''
             except:
                 videos = h5py.File('/GI/changsha1/videos_1080_2.hdf5','r')
                 X = np.reshape(videos['213langqiaojiwei_213langqiaojiwei_20171024213651'][0,:,:,:,:],(1,3,16,112,112))
             
                 Y = to_categorical(nb_label=nb_label,video_id = '213langqiaojiwei_213langqiaojiwei_20171024213651',sample_idx = 0, annos = annos)
                 Y = np.reshape(Y,(1,1,3))
                 #print('Error reading hdf5:',video_id,sample_idx)
                 error_hdf5.write(str(sample_path)+','+str(video_id)+','+str(sample_idx))
                 yield X,Y
            '''

