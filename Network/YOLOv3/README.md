# YOLOv3

## Introduction

[YOLOv3](https://github.com/qqwweee/keras-yolo3) is a very famous image detection network.

## Some issues to know

Before using YOLO, make sure you download [the pre-training model](https://fanhuaai-my.sharepoint.cn/:u:/g/personal/dongshuo_giai_tech/EeuZ4yqPRalMj9TQeUCMSMEBNqCJou8JgSF-Z5fmeXz4cg?e=cPUqJ6) , and put it in the `model_data/` directory.

## Quick tutorial

1. Download [car detection dataset](https://fanhuaai-my.sharepoint.cn/:u:/g/personal/dongshuo_giai_tech/EYzwu6k3GMVDlcrlhe3R6WIBOqcBr5t_eTeX3Uz5uO-0sQ?e=vVkmXf) and unzip, the dataset contains:
```cmd
|CarDataset/
    |--trainset/  #Images to train the model.
        |--xxx.jpg
        ...
    |--testset/  #Images to test your model.
        |--xxx.jpg
        ...
    |car_annotation.serval  #The annotation file contains the annotations for the images in the trainset directory.
```
2. First import the API library of the YOLOv3 image detection model.
```python
from Network.YOLOv3.API import YOLOv3_Dataloader, YOLOv3_Model
```
3. Create **YOLOv3_Model** and **YOLOv3_Dataloader** instances.
```python
m = YOLOv3_Model(class_count=2,lr=0.0003)
d = YOLOv3_Dataloader(data_path=r"dataset/path",anno_path=r"annotation/path",batch_size=16)
```
4. Set the Dataset for **YOLOv3_Model**.
```python
m.set_dataset(d)
```
5. Start training, set the epoch to 100 rounds, and save every 20 rounds.
```python
epoch = 100
for i in range(epoch):
    train_info = m.train()
    print(train_info)   #{'loss':[3.3914230046448886], 'val_loss':[3.8560243606567384]}
    if (i+1)%20==0 or i+1==epoch:
        save_path = "yolo3_model{}.h5".format(str(i).zfill(3))
        m.model.save(save_path)
```
6. After training, use Tegu-core to predict image. First create **YOLOv3_Model** .
```python
m = YOLOv3_Model(class_count=2)
```
7. Start predicting image using the model trained in the first few step.
```python
m.predict(img_path=r"dataset/save/path/trainset/xxx.jpg", model_path=r"ssd_modelXXX.h5", anno_path=r"dataset/save/path/car_annotation.serval")
#[[label:int, class_name:str, score:double, (xmin, ymin), (xmax, ymax)]]
```
For more usage, see `Example/yolo3_train.py`.
