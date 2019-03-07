#encoding=utf-8
import json
import os
import sys
from Network.activity_net.decrypt import decrypt_txt_file
import cv2
import numpy as np

DATA_DIR = r"data/dir"
SERVAL_PATH = r"annotation/path.serval"
URL_PREFIX = r"http://fake_site/"


def frames_and_fps(video_path):
    video = cv2.VideoCapture(video_path)
    if video:
        n = video.get(7)
        f = video.get(5)
        video.release()
        return n, f
    else:
        print ('read error!!')

def anno_result(line, fps):
    anno_list = []
    line = line.split(',')
    

    for i in range(int(len(line)/3)):
        anno = {}
        seg=[]
        seg.append(float(line[i*3 + 1])/fps)
        seg.append(float(line[i*3 + 2])/fps)
        anno["segment"] = seg
        anno["label"] = str(int(line[i*3 + 0]))
        anno_list.append(anno)
    return anno_list
        
def video_info(line, subset="training"):
    anno = {}
    video_name = line.split(':')[0]
    anno["subset"] = subset
    num_frames, fps = frames_and_fps(os.path.join(DATA_DIR,video_name))
    anno["num_frames"] = int(num_frames)
    anno["url"] = URL_PREFIX + video_name[:-4]
    duration = num_frames/fps
    anno["duration"] = duration
    anno["resolution"] = "1920x1080"
    anno["annotations"] = anno_result(line.split(':')[1], fps)
    return anno

def get_dict(content, trainset_ratio):
    content = content.split('\n')
  
    idx_list = np.arange(2,len(content))
    np.random.shuffle(idx_list)
    l = np.zeros(len(idx_list))
    for i in range(int(len(idx_list)*trainset_ratio)):
        l[idx_list[i]-2] = 1

    result = {}
    for i in range(2, len(content)):
        video_name = content[i].split(':')[0]
        if(l[i-2] == 0):
            result[video_name[:-4]] = video_info(content[i], subset="testing")
        else:
            result[video_name[:-4]] = video_info(content[i], subset="training")    
    return result 


def trans_to_json(content, trainset_ratio = 1.0, to_file = True,file_path = 'result.json'):
    print (('source content:',content))
    result = get_dict(content, trainset_ratio)
    if(to_file):
        with open(file_path,'w') as f:
            json.dump(result, f, indent=4, separators=(',', ': '))
        f.close()
    return json.dumps(result, indent=4, separators=(',', ': '))
    


if __name__ == '__main__':
    _, content = decrypt_txt_file(SERVAL_PATH)
    trans_to_json(content)