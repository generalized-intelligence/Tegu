![Tegu Logo](https://s2.ax1x.com/2019/01/30/kl6rzF.jpg)
# Tegu

[![Join the chat at https://gitter.im/Tegutalk/community](https://badges.gitter.im/Tegutalk/community.svg)](https://gitter.im/Tegutalk/community?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)

## A Machine Learning Toolbox for Non-ML Programmer
## 为非机器学习工程师设计的机器学习工具

Tegu is a rapid development toolkit for non-ML programmers who need to use machine learning for some aspect of their work. From our development experience, most machine learning demands can be solved by very simple solutions, but most existing solutions are too heavy. For example, if a drone engineer needs to implement object recognition, it is not efficient for him to learning machine learning from scratch. Tegu is a light toolkit for Non-ML programmers to develop machine learning solutions. Tegu GUI supports Windows and Linux, providing the most common machine learning implementations. 

Also, for professional machine learning engineers, most of the work (such as parameter tuning) should be simplified. Tegu is a good set of tool to simplify the workflow.

---


Tegu 是一个为日常工作中需要用到机器学习的非专业机器学习工程师设计的开源快速开发工具。在平时的工作中我们注意到，大部分每天日常的机器学习需求可以用很简单的方式解决，但现有的方案都太重了。比如说，一个无人机工程师需要用一次目标识别，那完全没有必要从头开始学习机器学习。Tegu 是一个轻量级的工具，方便非机器学习工程师开发机器学习。支持 Windows 与 Linux 环境下的 GUI 操作，内置了诸多机器学习常见需求。

另外，即使是专业的机器学习工程师，也有很多常见操作应该是可以被简化的（比如调参）。Tegu 对此也会有所裨益。

## Quick Start

1. Install [Python3](https://www.python.org) and [pip3](https://pip.pypa.io/en/stable/installing)
2. Install [CUDA](https://developer.nvidia.com/cuda-downloads) and [cuDNN](https://developer.nvidia.com/cudnn)
3. If you would like to use the Facial Recognition feature, please compile and install [OpenCV](https://opencv.org/). Please make sure the dnn module is installed.
4. Use the following command to install requirements:

```sh
pip3 install -r requirements.txt
```

5. Once all requirements are installed, use the following command to launch Tegu:
``` sh
python3 tegu.py
```
For Image Recognition and Video Classification, we have developed a set of tools to process and clean up the datasets. You may use [Tegu Image Annotation](http://www.giai.tech) and [Tegu Video Annotation](http://www.giai.tech) to process your dataset.

---

1. 首先请安装 [Python3](https://www.python.org) 以及 [pip3](https://pip.pypa.io/en/stable/installing)。
2. 请安装 [CUDA](https://developer.nvidia.com/cuda-downloads) 和 [cuDNN](https://developer.nvidia.com/cudnn)。
3. 如果需要使用人脸检测功能， 请编译安装 [OpenCV](https://opencv.org/), 并确保安装其 dnn 模块。
4. 使用如下命令安装所需的 Python 框架:

```sh
pip3 install -r requirements.txt
```

5. 安装好所需框架以后，使用以下命令运行 Tegu:
``` sh
python3 tegu.py
```
对于图像检测和视频分类任务，我们使用自己的格式处理数据集，您可以使用 [Tegu 图像标注软件](http://www.giai.tech)，和 [Tegu 视频标注软件](http://www.giai.tech) 来制作数据集。

## File Structure

* GUI/: User Interface, written with [PyQt5](https://www.riverbankcomputing.com/software/pyqt/download5)
* Network/: Neural Networks, called by scripts in GUI/
* hook/: hook file used to make Windows .exe file
* Resource/: Elements used to make GUI
* Util/: Utility used in the project

---

* GUI/: 项目的ui部分，使用 [PyQt5](https://www.riverbankcomputing.com/software/pyqt/download5) 编写。
* Network/: 项目所用到的网络部分， 被外部 GUI 脚本引用。
* hook/: 将项目打包成 Windows 的 .exe 可执行文件所用到的 hook 文件。
* Resource/: GUI 需要的元素。
* Util/: 项目使用的一些工具脚本。

## Existing Features

* Video Classification (Long Video Classification)
* Image Recognition
* Facial Recognition (build feature library, and recognize)
* License Plate Recognition

HTTP API is available for Image Recognition, Facial Recognition and License Plate Recognition

---

* 视频分类（长视频分类）
* 图像检测
* 人脸识别（建立特征库，并识别人脸）
* 车牌识别

其中图像检测，人脸识别，车牌识别，都提供 HTTP API 可在使用时调用。

## User Manual

See [User Manual](http://www.giai.tech)

---

参见 [说明文档](http://www.giai.tech)

## Relevant Projects

For Image Recognition and Video Classification, we have developed a set of tools to process and clean up the datasets. You may use [Tegu Image Annotation](http://www.giai.tech) and [Tegu Video Annotation](http://www.giai.tech) to process your dataset.

---

对于图像检测和视频分类的数据处理及标注，我们提供了 [Tegu 图像标注软件](http://www.giai.tech)，和 [Tegu 视频标注软件](http://www.giai.tech) 。

## Neural Networks Used

* [YOLOv3](https://github.com/qqwweee/keras-yolo3)
* [SSD300](https://github.com/pierluigiferrari/ssd_keras)
* [ActivityNet](https://github.com/imatge-upc/activitynet-2016-cvprw)
* [MTCNN_face_detection](https://github.com/kpzhang93/MTCNN_face_detection_alignment)
* [facenet](https://github.com/davidsandberg/facenet)
* [HyperLPR](https://github.com/zeusees/HyperLPR)

## TODO

* Optimization of interprocess communication
* Adding common neural networks, such as passenger detection, vehicle detection, and cat/dog detection
* Abnormality Detection in Restricted Zone (Training Free)
* Chinese NLP
* Hand Gesture Recognition, Pose Detection based on Feature Point Paring, Facial Feature Point Detection (Training Free)
* Image Segmentation
* General OCR
* Video Tracking (Work-In-Progress)

---

* 修改进程通信模块
* 建立行人，车辆，猫狗等常见检测模型
* 禁入区等功能（免训练）
* 中文语音识别
* 手势识别，人体姿态特征点检测，人脸特征点检测（免训练）
* 图像分割，要有相应的常见模型
* 通用OCR。
* 视频追踪（Work-In-Progress）

# Meta

Project initialized by Generalized Intelligence

泛化智能 Generalized Intelligence 出品。

Distributed under the BSD 3-Clause license. See LICENSE for more information.

# Contribute

Please follow CONTRIBUTING.md

请参阅 CONTRIBUTING.md
