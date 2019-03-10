# SSD300

## Introduction

[SSD300](https://github.com/pierluigiferrari/ssd_keras) is a very famous image detection network.

## Some issues to know

Before using SSD, make sure you download [the pre-training model](https://fanhuaai-my.sharepoint.cn/:u:/g/personal/dongshuo_giai_tech/Ea35CHckxTBDj6QCwhgIAfkBEKlgPcbPVHDDCfP9O85m9Q?e=LgIK7g) , and put it in this directory.

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
2. First import the API library of the SSD300 image detection model.
```python
from Network.SSD300.API import SSD_Model, SSD_DataLoaders
```
3. Create **SSD_Model** and **SSD_Dataloader** instances.
```python
m = SSD_Model(class_count=2, base_lr=0.0004)
d = SSD_DataLoader(anno_path=r"dataset/save/path/car_annotation.serval", data_path=r"dataset/save/path/trainset",batch_size=16)
```
4. Set the Dataset for **SSD_Model**.
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
        save_path = "ssd_model{}.h5".format(str(i).zfill(3))
        m.model.save(save_path)
```
For more usage, see `Example/ssd_train.py`.