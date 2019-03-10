![Tegu Logo](https://s2.ax1x.com/2019/01/30/kl6rzF.jpg)
# Tegu

[![Join the chat at https://gitter.im/Tegutalk/community](https://badges.gitter.im/Tegutalk/community.svg)](https://gitter.im/Tegutalk/community?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)

## Use Machine Learning Right Now In Your Project
## 即刻在你的项目中使用机器学习

Tegu-core is the core component of Tegu, which provides an encapsulation of some state-of-the-art deep learning models of computer vision, and its APIs are called by the Tegu GUI components. You can use Tegu-core to provide some deep learning functions in your own Python projects with only a few codes.

Tegu-core 是 Tegu 的核心组件，提供了对一些当前最佳实践（State of the Art）的计算机视觉深度学习模型的封装，与Tegu GUI配合使用。若您需要在Python项目中引入深度学习功能，只需要很少的代码，您就可以将Tegu-core与您的项目一起配合使用。

---

## 30s to start training car detection model
For deep learning tasks, Tegu uses the **Network_Model** class to manage training tasks, and uses the **Network_Dataloader** class to manage data sets.

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
For more usage, see `Example`.

## Quick Start

1. Install [Python3](https://www.python.org) and [pip3](https://pip.pypa.io/en/stable/installing)
2. Install [CUDA](https://developer.nvidia.com/cuda-downloads) and [cuDNN](https://developer.nvidia.com/cudnn)
3. If you would like to use the Facial Recognition feature, please compile and install [OpenCV](https://opencv.org/). Please make sure the DNN module is installed.
4. Use the following command to install requirements:

```sh
pip3 install -r requirements.txt
```

5. For the usage of Tegu-core API, see `Example` Folder.

For Image Recognition and Video Classification, we have developed a set of tools to process and clean up the datasets. You may use [Tegu Image Annotation](http://www.giai.tech) and [Tegu Video Annotation](http://www.giai.tech) to process your dataset.

## File Structure

* Network/: Neural Networks, called by scripts in GUI/
* Example/: Samples for how to use Tegu-core. 
* Util/: Utility used in the project

## Existing Features

* Video Classification (Long Video Classification)
* Image Recognition
* Facial Recognition (build feature library, and recognize)
* License Plate Recognition

HTTP API is available for Image Recognition, Facial Recognition and License Plate Recognition

## Relevant Projects

For Image Recognition and Video Classification, we have developed a set of tools to process and clean up the datasets. You may use [Tegu Image Annotation](http://www.giai.tech) and [Tegu Video Annotation](http://www.giai.tech) to process your dataset.

## Existing Neural Networks

* [YOLOv3](https://github.com/qqwweee/keras-yolo3)
* [SSD300](https://github.com/pierluigiferrari/ssd_keras)
* [ActivityNet](https://github.com/imatge-upc/activitynet-2016-cvprw)
* [MTCNN_face_detection](https://github.com/kpzhang93/MTCNN_face_detection_alignment)
* [facenet](https://github.com/davidsandberg/facenet)

## TODO

* Optimization of interprocess communication
* Adding common neural networks, such as passenger detection, vehicle detection, and cat/dog detection
* Abnormality Detection in Restricted Zone (Training Free)
* Hand Gesture Recognition, Pose Detection based on Feature Point Paring, Facial Feature Point Detection (Training Free)
* Image Segmentation
* General OCR
* Video Tracking (Work-In-Progress)

# Meta

Project initialized by Generalized Intelligence
Distributed under the BSD 3-Clause license. See LICENSE for more information.

# Contribute

Please follow CONTRIBUTING.md

---

## 30秒开始训练车辆检测模型
对于深度学习任务，Tegu 使用 **网络名_Model** 类来管理训练任务，使用 **网络名_Dataloader** 类来管理数据集。

1. 下载 [车辆检测数据集](https://fanhuaai-my.sharepoint.cn/:u:/g/personal/dongshuo_giai_tech/EYzwu6k3GMVDlcrlhe3R6WIBOqcBr5t_eTeX3Uz5uO-0sQ?e=vVkmXf) 并解压缩。
2. 首先 import SSD300 图像检测模型的 API 库。
```python
from Network.SSD300.API import SSD_Model, SSD_DataLoaders
```
3. 创建 **SSD_Model** 和 **SSD_Dataloader** 实例。
```python
m = SSD_Model(class_count=2, base_lr=0.0004)
d = SSD_DataLoader(anno_path=r"dataset/save/path/car_annotation.serval", data_path=r"dataset/save/path/trainset",batch_size=16)
```
4. 为 **SSD_Model** 设置 Dataset。
```python
m.set_dataset(d)
```
5. 开始训练，设置 epoch 为 100 轮，并且每 20 轮保存一次。
```python
epoch = 100
for i in range(epoch):
    train_info = m.train()
    print(train_info)   #{'loss':[3.3914230046448886],'val_loss':[3.8560243606567384]}
    if (i+1)%20==0 or i+1==epoch:
        save_path = "ssd_model{}.h5".format(str(i).zfill(3))
        m.model.save(save_path)
```
查看更多应用，请参见 `Example`。

## 快速开始
1. 首先请安装 [Python3](https://www.python.org) 以及 [pip3](https://pip.pypa.io/en/stable/installing)。
2. 请安装 [CUDA](https://developer.nvidia.com/cuda-downloads) 和 [cuDNN](https://developer.nvidia.com/cudnn)。
3. 如果需要使用人脸检测功能， 请编译安装 [OpenCV](https://opencv.org/), 并确保安装其 DNN 模块。
4. 使用如下命令安装所需的 Python 框架:

```sh
pip3 install -r requirements.txt
```
5. Tegu-core 模型API的用法，可以参照`Example`文件夹中的示例代码。

对于图像检测和视频分类任务，我们使用自己的格式处理数据集，您可以使用 [Tegu 图像标注软件](http://www.giai.tech)，和 [Tegu 视频标注软件](http://www.giai.tech) 来制作数据集。

## 文件结构

* Network/: 项目所用到的网络部分，可供外部的Python文件调用。
* Example/：项目的示例代码。
* Util/: 项目使用的一些工具脚本。

## 现有功能

* 视频分类（长视频分类）
* 图像检测
* 人脸识别（建立特征库，并识别人脸）
* 车牌识别

## 相关项目

对于图像检测和视频分类的数据处理及标注，我们提供了 [Tegu 图像标注软件](http://www.giai.tech)，和 [Tegu 视频标注软件](http://www.giai.tech) 

## 已有网络

* [YOLOv3](https://github.com/qqwweee/keras-yolo3)
* [SSD300](https://github.com/pierluigiferrari/ssd_keras)
* [ActivityNet](https://github.com/imatge-upc/activitynet-2016-cvprw)
* [MTCNN_face_detection](https://github.com/kpzhang93/MTCNN_face_detection_alignment)
* [facenet](https://github.com/davidsandberg/facenet)

## 待办事项

* 修改进程通信模块
* 建立行人，车辆，猫狗等常见检测模型
* 禁入区等功能（免训练）
* 手势识别，人体姿态特征点检测，人脸特征点检测（免训练）
* 图像分割，要有相应的常见模型
* 通用OCR。
* 视频追踪（Work-In-Progress）

# 版权信息

泛化智能 Generalized Intelligence 出品。
本项目通过 BSD 3-Clause 协议发布，详情见 LICENSE。 

# 贡献

请参阅 CONTRIBUTING.md
