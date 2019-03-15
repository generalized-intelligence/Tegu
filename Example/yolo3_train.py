from Network.YOLOv3.API import YOLOv3_Dataloader, YOLOv3_Model
import os
import cv2
import numpy as np
from Util.mylogger import MyLogger

import math

def yolo3_train():
    m = YOLOv3_Model(class_count=2,lr=0.0003)
    d = YOLOv3_Dataloader(data_path=r"dataset/path",anno_path=r"annotation/file/path",batch_size=16)
    m.set_dataset(d)
    epoch = 100
    for i in range(epoch):
        print('Epoch:',i)
        train_info = m.train()       
        print('Epoch:{}, history:{}'.format(i,train_info.history))

        if (i)%20==0 or i+1==epoch:
            save_path = "yolo3_model{}.h5".format(str(i).zfill(3))
            m.model.save(save_path)
            m.predict(r"D:\ATegu\CarDataset\trainset\009600.JPG")
            print('Saved')

def yolo3_predict():
    m = YOLOv3_Model(class_count=2)
    print(m.predict(r"image/you/want/to/predict", model_path=r"model/path", anno_path=r"annotation/file/path"))

if __name__ == '__main__':
    yolo3_train()
    yolo3_predict()