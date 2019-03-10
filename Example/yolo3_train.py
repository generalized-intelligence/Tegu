import sys
sys.path.append('..')
from Network.YOLOv3.API import YOLOv3_Dataloader, YOLOv3_Model
import os
import cv2
import numpy as np
from Util.mylogger import MyLogger

import math

def yolo3_train():
    m = YOLOv3_Model(class_count=2,lr=0.0003)
    d = YOLOv3_Dataloader(data_path=r"dataset/path",anno_path=r"annotation/path",batch_size=32)
    m.set_dataset(d)
    for i in range(100):
        print('Epoch:',i)
        train_info = m.train()       
        print('Epoch:{}, history:{}'.format(i,train_info.history))

        if (i+1)%20==0 or i+1==epoch:
            save_path = "yolo3_model{}.h5".format(str(i).zfill(3))
            m.model.save(save_path)
            print('Saved')


if __name__ == '__main__':
    yolo3_train()